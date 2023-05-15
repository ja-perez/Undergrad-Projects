"""
Author: Javier Perez
Date: 10/10/22
Description:
    This file defines the classes: Table, Database, Database Manager
    The database manager in this case will be the only object that we explicitly
    call in the main and serves as the users guide and access point into the
     database management system(DBMS).
"""

import os
import shutil


class Table:
    """
        Class Name: Table
        Constructor:
            params: name (str), path(str)
        Description:
            - Defines and stores the methods/data necessary to create, delete, update, and
            display tuples of information from a given database.
            - Is called only by the Database class and each table object is associated with
            a text file within the database class.
            - The tables metadata and information is stored within this text file with the
            attributes dictionary storing a high-level description for the metadata and the
            information to be stored with each entry.
    """

    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.attribute_types = {"int": int, "float": float, "char(": str, "varchar(": str}
        self.attributes = {}  # {Column: [Attribute Name(str), Attribute Type(str)

    def create_table(self):
        try:
            table = open(self.path, "x")
            table.close()
            success = "Table " + self.name + " created."
            print(success)
            return True
        except FileExistsError as _:
            error = "!Failed to create table " + self.name \
                    + " because it already exists."
            print(error)
            return False

    def add_values(self, values):
        values = values[0]
        value_name = [name for i, name in enumerate(values) if i % 2 == 0]
        value_type = [v_type for v_type in values if v_type not in value_name]
        for v_type in value_type:
            if "(" in v_type:
                v_type = v_type.split('(')[0] + '('
            if v_type not in self.attribute_types:
                type_error = "!Failed to alter table " + self.name + \
                             " because of an error related to the attribute " + v_type + "."
                print(type_error)
        temp = open('temp', 'w')
        with open(self.path, 'r') as table_rows:
            for row in table_rows:
                if self.attributes[0][0] in row:
                    for i, v_name in enumerate(value_name):
                        row = row.strip('\n') + v_name + ' '
                        self.attributes[max(self.attributes) + i + 1] = (v_name, value_type[i])
                    row += '\n'
                temp.write(row)
        temp.close()
        shutil.move('temp', self.path)
        success = "Table " + self.name + " modified."
        print(success)

    def set_values(self, values):
        values = values[0]
        # Assumptions for testing: Syntax for creating table is correct
        # Each value has an attribute name and type
        value_name = [name for i, name in enumerate(values) if i % 2 == 0]
        value_type = [v_type for v_type in values if v_type not in value_name]
        # Error checking for type string value
        for v_type in value_type:
            if "(" in v_type:
                v_type = v_type.split('(')[0] + '('
            if v_type not in self.attribute_types:
                type_error = "!Failed to create table " + self.name + " because of an error" \
                                                                      " related to the attribute " + v_type + "."
                print(type_error)
                return False
        file = open(self.path, "a")
        for i, v_name in enumerate(value_name):
            file.write(v_name + ' ')
            self.attributes[i] = (v_name, value_type[i])
        file.write('\n')
        file.close()
        return True

    def select_values(self, identifier):
        if identifier[0] == "*":
            # Print all headers and associated values
            table_rows = open(self.path, "r")
            for row in table_rows:
                columns = row.split()
                print(' | '.join([entry + ' ' + self.attributes[i][1] for i, entry in enumerate(columns)]))
            table_rows.close()
        else:
            pass


class Database:
    """
        Class Name: Database
        Constructor:
            params: db_name (str)
        Description:
            - Defines and stores the methods/data necessary to create, delete, update, and
            query a databases tables.
            - Is called only by the Database Manager class and is associated with a directory
            that is created within the working directory that the program was called from.
            - Keeps a dictionary variables, Tables, with the keys being the Tables Name and
            the value being the particular Table object instance associated with that name.
    """

    def __init__(self, db_name):
        self.db_name = db_name
        self.db_path = "./" + db_name
        self.tables = {}

    def create_table(self, table_name, *values):
        table_path = self.db_path + '/' + table_name
        if '.' not in table_name:
            table_path += '.txt'
        temp = Table(table_name, table_path)
        if not temp.create_table():
            self.tables[table_name] = temp
        else:
            self.tables[table_name] = temp
            if not temp.set_values(values):
                self.tables.pop(table_name)

    def drop_table(self, table_name):
        try:
            os.remove(self.tables[table_name].path)
            self.tables.pop(table_name)
            success = "Table " + table_name + " deleted."
            print(success)
        except (KeyError, FileNotFoundError):
            error_msg = "!Failed to delete " + table_name + " because it does not exist."
            print(error_msg)

    def update_table(self, table_name, *values):
        self.tables[table_name].add_values(values)

    def query_table(self, table_name, *values):
        try:
            self.tables[table_name].select_values(values)
        except KeyError as _:
            error_msg = "!Failed to query table " + table_name + " because it does not exist."
            print(error_msg)

    def does_table_exist(self, table_name: str) -> bool:
        return table_name in self.tables

    def get_db_path(self) -> str:
        return self.db_path

    def get_table_path(self, table_name: str) -> str:
        return self.tables[table_name]


class DatabaseManager:
    """
        Class Name: DatabaseManager
        Constructor:
            params: None
        Description:
            - Defines and stores the methods/data necessary to create and delete databases
            within the working folder.
            - Is called by the main program and uses the curr_db variable to handle updates
            related to that specific database.
            - Maintains a dictionary variable, databases, with the key value pair
            { Database Name: Database Object }
            - Also sets determines if the parser is case-sensitive using the variable
            is_case_sensitive.
    """
    def __init__(self):
        self.curr_db = None
        self.databases = {}
        self.is_case_sensitive = 1

    def create_database(self, db_name):
        try:
            os.mkdir(db_name)
            self.databases[db_name] = Database(db_name)
            success = "Database " + db_name + " created."
            print(success)
        except FileExistsError as _:
            if db_name not in self.databases:
                self.databases[db_name] = Database(db_name)
            error_msg = "!Failed to create database " + db_name + " because it already exists."
            print(error_msg)

    def set_curr_db(self, dest_db: str):
        try:
            self.curr_db = self.databases[dest_db]
            success = "Using database " + dest_db
            print(success)
        except KeyError as _:
            error_msg = "!Failed to use database " + dest_db + " because it does not exist."
            print(error_msg)

    def drop_database(self, db_name):
        try:
            os.rmdir(db_name)
            self.databases.pop(db_name)
            success = "Database " + db_name + " deleted."
            print(success)
        except (KeyError, FileNotFoundError):
            error_msg = "!Failed to delete " + db_name + " because it does not exist."
            print(error_msg)
        except OSError:
            error_msg = "!Failed to delete " + db_name + " because it is not empty."
            print(error_msg)

    def get_curr_db_name(self):
        return self.curr_db.db_name

# Testing Classes and their methods
# test = DatabaseManager()
# test.create_database("t1")
# test.set_curr_db("t1")
# test.curr_db.create_table('test_table', ['a1', 'int', 'a2', 'varchar(20)'])
# test.curr_db.query_table('test_table', '*')
# test.curr_db.update_table('test_table', ['a3', 'float'])
# test.curr_db.query_table('test_table', '*')
# test.curr_db.drop_table('test_table')
# test.drop_database(test.get_curr_db_name())
