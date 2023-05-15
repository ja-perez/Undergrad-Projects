"""
Author: Javier Perez
Date: 10/31/22
Description:
    This file defines the classes: Table, Database, Database Manager
    The database manager in this case will be the only object that we explicitly
    call in the main and serves as the outline for the object-oriented approach taken
    towards the implementation of the database management system(DBMS).
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
            - The tables metadata and information is stored within the text file associated
            with the path that is passed at instantiation, with the attributes dictionary
            storing a high-level description of the metadata and the information to be stored
            in each entry.
    """

    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.attribute_types = {"int": int, "float": float, "char(": str, "varchar(": str}
        self.attributes = {}  # {Column: [Attribute Name(str), Attribute Type(str)]}
        self.files_modified = 0

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
                        if '(' in value_type[i]:
                            value_type[i] += ')'
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
            if '(' in value_type[i]:
                value_type[i] += ')'
            self.attributes[i] = (v_name, value_type[i])
        file.write('\n')
        file.close()
        return True

    def select_values(self, identifiers):
        if identifiers[0] == "*":
            # Print all headers and associated values
            table_file = open(self.path, "r")
            table_rows = table_file.readlines()
            header = table_rows[0].split()
            table_entries = table_rows[1:]
            print('|'.join([attr + ' ' + self.attributes[i][1] for i, attr in enumerate(header)]))
            for entry in table_entries:
                print('|'.join(entry.split()))
            table_file.close()
        else:
            select_ids, where_args = identifiers[0], identifiers[1]
            where_var, where_op, where_val = where_args
            where_col = 0
            file = open(self.path, "r")
            rows = file.readlines()
            file.close()
            output_cols = [col for col in self.attributes if self.attributes[col][0] in select_ids]
            header = rows[0].split()
            header = [var for i, var in enumerate(header) if i in output_cols]
            print('|'.join([header[i] + ' ' + self.attributes[attr][1] for i, attr in enumerate(output_cols)]))
            entries = rows[1:]
            for col in self.attributes:
                if self.attributes[col][0] == where_var:
                    where_col = col
            for entry in entries:
                entry_data = entry.split()
                if self.where_condition(entry_data[where_col], where_op, where_val, where_col):
                    output = '|'.join([entry_data[i] for i in output_cols])
                    print(output)

    def insert_values(self, values):
        file = open(self.path, "a")
        for value in values:
            file.write(value + " ")
        file.write("\n")
        file.close()
        print("1 new record inserted.")

    def update_values(self, set_args, where_args):
        file = open(self.path, "r")
        rows = file.readlines()
        file.close()
        header = rows[0]
        entries = rows[1:]
        where_var, where_op, where_val, where_col = where_args[0], where_args[1], where_args[2], 0
        set_var, set_val, set_col = set_args[0], set_args[2], 0
        for col in self.attributes:
            if self.attributes[col][0] == set_var:
                set_col = col
            if self.attributes[col][0] == where_var:
                where_col = col
        file = open(self.path, "w")
        file.write(header)
        modified_flag = 0
        for entry in entries:
            entry_data = entry.split()
            if self.where_condition(entry_data[where_col], where_op, where_val, where_col):
                entry_data[set_col] = set_val
                modified_flag = 1
            entry = ' '.join(entry_data)
            file.write(entry + '\n')
        if modified_flag:
            self.files_modified += 1
            if self.files_modified == 1:
                print(self.files_modified, "record modified.")
            else:
                print(self.files_modified, "records modified.")
        file.close()

    def delete_values(self, where_args):
        file = open(self.path, "r")
        rows = file.readlines()
        file.close()
        header = rows[0]
        entries = rows[1:]
        where_var, where_op, where_val, where_col = where_args[0], where_args[1], where_args[2], 0
        for col in self.attributes:
            if self.attributes[col][0] == where_var:
                where_col = col
        file = open(self.path, "w")
        file.write(header)
        files_deleted = 0
        for entry in entries:
            entry_data = entry.split()
            if self.where_condition(entry_data[where_col], where_op, where_val, where_col):
                files_deleted += 1
            else:
                entry = ' '.join(entry_data)
                file.write(entry + '\n')
        if files_deleted == 1:
            print(files_deleted, "record deleted.")
        elif files_deleted > 0:
            print(files_deleted, "records deleted.")
        file.close()

    def where_condition(self, table_val, conditional_op, where_val, attribute_col):
        """
            Converts the str interpretation of the where conditions into
            a returnable bool operation.
        """
        val_type = self.attributes[attribute_col][1]
        if '(' in val_type:
            val_type = val_type.split("(")[0] + "("
        table_val, where_val = self.attribute_types[val_type](table_val), self.attribute_types[val_type](where_val)
        match conditional_op:
            case "=":
                return table_val == where_val
            case ">":
                return table_val > where_val
            case ">=":
                return table_val >= where_val
            case "<":
                return table_val < where_val
            case "<=":
                return table_val <= where_val
            case "!=":
                return table_val != where_val


class Database:
    """
        Class Name: Database
        Constructor:
            params: db_name (str)
        Description:
            - Defines and stores the methods/data necessary to create, delete, alter, and
            query a databases tables. Also defines get methods in order to insert, update,
            and delete tuples of information with those tables.
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

    def alter_table(self, table_name, *values):
        self.tables[table_name].add_values(values)

    def query_table(self, table_name, *values):
        try:
            self.tables[table_name].select_values(values)
        except KeyError as _:
            error_msg = "!Failed to query table " + table_name + " because it does not exist."
            print(error_msg)

    def insert_table(self, table_name, values):
        self.tables[table_name].insert_values(values)

    def update_table(self, table_name, set_values, where_values):
        self.tables[table_name].update_values(set_values, where_values)

    def delete_table_records(self, table_name, where_values):
        self.tables[table_name].delete_values(where_values)

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
            - Commands are not case-sensitive, however database names, table names,
            and variables are.
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
            success = "Using database " + dest_db + "."
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
