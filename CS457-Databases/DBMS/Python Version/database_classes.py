"""
Author: Javier Perez
Date: 12/15/22
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
        self.attr_to_col = {}  # {Attribute Name(str) : Column(int)}
        self.files_modified = 0
        self.lock_file = self.name + '_lock.txt'

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
            if '(' in value_type[i] and ')' not in value_type[i]:
                value_type[i] += ')'
            self.attributes[i] = (v_name, value_type[i])
        file.write('\n')
        file.close()
        return True

    def set_attributes(self, values):
        values = values[0]
        value_name = [name for i, name in enumerate(values) if i % 2 == 0]
        value_type = [v_type for v_type in values if v_type not in value_name]
        for i, v_name in enumerate(value_name):
            self.attributes[i] = (v_name, value_type[i])

    def get_values(self):
        values = []
        with open(self.path, "r") as f:
            f_lines = f.readlines()
            for line in f_lines:
                values.append(line.strip('\n '))
        return values

    def select_values(self, output_vals, condition, *is_join):
        with open(self.path, "r") as table:
            rows = table.readlines()
            for i, row in enumerate(rows):
                rows[i] = row.strip('\n ').split()
        output_cols = [i for i in self.attributes] if output_vals[0] == '*' else \
            [col for col in self.attributes if self.attributes[col][0] in output_vals]
        header = [' '.join(self.attributes[i]) for i, val in enumerate(rows[0]) if i in output_cols]

        if not condition:
            print('|'.join(header))
            for row in rows[1:]:
                print('|'.join(row))
        elif is_join:
            joined_table, joined_attributes, join_type = is_join[0], is_join[1], is_join[2]
            attributes = [joined_attributes[attr] for attr in joined_attributes]
            header = []
            for var in attributes:
                header.append(' '.join(var))
            print('|'.join(header))
            left_condition, operation, right_condition = condition
            left_condition = left_condition.split('.')[1]
            right_condition = right_condition.split('.')[1]
            left_col = [col for col in joined_attributes if joined_attributes[col][0] == left_condition][0]
            right_col = [col for col in joined_attributes if joined_attributes[col][0] == right_condition][0]
            output_cols = [i for i, _ in enumerate(header)] if '*' in output_vals[0] \
                else [i for i, val in enumerate(header) if val in output_vals]
            outputs = []
            for i, entry in enumerate(joined_table[1:]):
                entry = entry.split()
                if self.on_condition(entry[left_col], operation, entry[right_col], left_col, joined_attributes):
                    output = [val for i, val in enumerate(entry) if i in output_cols]
                    outputs.append('|'.join(output))
            for output in outputs:
                print(output)
            if join_type == "outer":
                unique_left = [(val.split()[0], val.split()[1]) for val in joined_table[1:]]
                unique_left = set(unique_left)
                unique_left = ['|'.join(val) + '||' for val in unique_left]
                outputs = ''.join(outputs)
                for ul in unique_left:
                    if ul[:-2] not in outputs:
                        print(ul)
        else:
            print('|'.join(header))
            left_cond, operation, right_cond = condition
            left_col = [col for col in self.attributes if self.attributes[col][0] == left_cond][0]
            for row in rows[1:]:
                if self.where_condition(row[left_col], operation, right_cond, left_col):
                    output = [val for i, val in enumerate(row) if i in output_cols]
                    print('|'.join(output))

    def insert_values(self, values):
        file = open(self.path, "a")
        for value in values:
            file.write(value + " ")
        file.write("\n")
        file.close()
        print("1 new record inserted.")

    def update_values(self, set_args, where_args):
        if not self.transaction_begin():
            return False

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
        file = open(self.lock_file, "w")
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
        return True

    def commit_updates(self):
        file = open(self.lock_file, "r")
        rows = file.readlines()
        file.close()
        header = rows[0]
        entries = rows[1:]
        file = open(self.path, "w")
        file.write(header)
        for entry in entries:
            file.write(entry)
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

    def on_condition(self, left_val, conditional_op, right_val, attribute_col, attributes):
        val_type = attributes[attribute_col][1]
        if '(' in val_type:
            val_type = val_type.split("(")[0] + "("
        table_val, where_val = self.attribute_types[val_type](left_val), self.attribute_types[val_type](right_val)
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

    def transaction_begin(self):
        if os.path.exists(self.lock_file):
            print("!Error: Table", self.name, 'is locked!')
            return False
        else:
            lock_file = open(self.lock_file, "a")
            lock_file.close()
            return True

    def transaction_end(self):
        self.commit_updates()
        os.remove(self.lock_file)

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
        self.is_transaction = False
        self.commits = []

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

    def find_tables(self):
        dir_tables = os.listdir(self.db_path)
        for table_path in dir_tables:
            table_ext = table_path.index('.')
            table_name = table_path[:table_ext]
            table_path = self.db_path + '/' + table_path
            temp = Table(table_name, table_path)
            self.tables[table_name] = temp
            vals = self.tables[table_name].get_values()
            value_names = vals[0].split()
            entries = vals[1:][0].split()
            table_values = []
            for i, entry in enumerate(entries):
                value_type = self.determine_type(entry, table_name)
                table_values.append(value_names[i])
                table_values.append(value_type)
            self.tables[table_name].set_attributes([table_values])

    def determine_type(self, entry, table_name):
        valid_types = self.tables[table_name].attribute_types
        check_order = ['int', 'float', 'char(']
        entry_type = ''
        for type_check in check_order:
            try:
                valid_types[type_check](entry)
                entry_type = type_check
                break
            except ValueError as _:
                pass
        if entry_type == 'char(' and len(entry) > 1:
            entry_type = 'varchar('
        return entry_type

    def drop_table(self, table_name):
        try:
            os.remove(self.tables[table_name].path)
            self.tables.pop(table_name)
            success = "Table " + table_name + " deleted."
            print(success)
        except (KeyError, FileNotFoundError):
            error_msg = "!Failed to delete " + table_name + " because it does not exist."
            print(error_msg)

    def alter_table(self, table_name, values):
        self.tables[table_name].add_values(values)

    def join_tables(self, table_1, table_2):
        table_1 = table_1.lower()
        table_2 = table_2.lower()
        try:
            data_1 = self.tables[table_1].get_values().copy()
            data_2 = self.tables[table_2].get_values().copy()
            data_1_header, data_1 = data_1[0], data_1[1:]
            data_2_header, data_2 = data_2[0], data_2[1:]
            new_table = [data_1_header + ' ' + data_2_header]
            for d1 in data_1:
                for d2 in data_2:
                    new_table.append(d1 + ' ' + d2)
            attr_1 = self.tables[table_1].attributes.copy()
            attr_2 = self.tables[table_2].attributes.copy()
            new_attributes = attr_1
            for col in attr_2:
                new_attributes[max(new_attributes) + 1] = attr_2[col]
            return new_table, new_attributes
        except KeyError as _:
            error_msg = "!Failed to join table " + table_1 + " and " + table_2 + " because one of them does not exist."
            print(error_msg)

    def query_table(self, table_name, select_values, conditions):
        try:
            if type(table_name) == list:
                table_1 = table_name[0].lower()
                join_type = 'outer' if 'outer' in table_name else 'inner'
                if 'join' in table_name:
                    join_index = table_name.index('join')
                    table_2 = table_name[join_index + 1].lower()
                else:
                    table_2 = table_name[2].lower()
                table_join, attr_join = self.join_tables(table_1, table_2)
                self.tables[table_1].select_values(select_values, conditions, table_join, attr_join, join_type)
            else:
                self.tables[table_name].select_values(select_values, conditions)
        except KeyError as _:
            error_msg = "!Failed to query table " + table_name + " because it does not exist."
            print(error_msg)

    def insert_table(self, table_name, values):
        self.tables[table_name].insert_values(values)

    def update_table(self, table_name, set_values, where_values):
        transaction_success = self.tables[table_name].update_values(set_values, where_values)
        if transaction_success:
            self.commits.append(table_name)

    def delete_table_records(self, table_name, where_values):
        self.tables[table_name].delete_values(where_values)

    def set_transaction(self, state):
        if state:
            print('Transaction starts.')
        else:
            self.set_commit()

    def set_commit(self):
        if self.commits:
            for file_name in self.commits:
                self.tables[file_name].transaction_end()
            print("Transaction committed.")
        else:
            print("Transaction abort.")

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
            - Commands are not case-sensitive, however database names,
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

    def update_databases(self, dest_db):
        self.databases[dest_db] = Database(dest_db)
        self.databases[dest_db].find_tables()

    def set_curr_db(self, dest_db: str):
        if os.path.exists(dest_db) and dest_db not in self.databases:
            self.update_databases(dest_db)
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
