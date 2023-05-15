"""
Author: Javier Perez
Date: 12/15/22
Description:
    This file defines the classes: CLI, CommandManager
    The CLI in this case will be the only object that we explicitly call in the
    main and serves as the users guide and interface when interacting with the
    database management system(DBMS).
    The database manager in this case will be the only object that we explicitly
    call in the main and serves as the users guide and access point into the
"""

import os


def is_command(line):
    return line and line[:2] != "--"


class CLI:
    def __init__(self, dbms):
        self.cmds = ""
        self.cmd_manager = CommandManager(dbms)

    def prompt(self):
        cli_args = input("# ")
        curr_cmd = []
        while True:
            if ';' in cli_args or '.exit' in cli_args:
                curr_cmd.append(cli_args)
                break
            curr_cmd.append(cli_args)
            cli_args = input("  ")
        self.cmds = ' '.join(curr_cmd)
        self.parse_cmds()

    def batch_mode(self, batch_files):
        files_to_cmds = {}
        for file in batch_files:
            file_cmds = []
            with open(file, "r") as f:
                f_lines = f.readlines()
                curr_cmd = []
                for line in f_lines:
                    line = line.strip('\n')
                    if is_command(line) and (';' in line or '.exit' in line or '.EXIT' in line):
                        curr_cmd.append(line)
                        file_cmds.append(' '.join(curr_cmd))
                        curr_cmd = []
                    elif is_command(line):
                        curr_cmd.append(line)
            files_to_cmds[file] = file_cmds
        self.parse_cmds(files_to_cmds)

    def parse_cmds(self, batch_files=None):
        if batch_files:
            for file in batch_files:
                for cmd in batch_files[file]:
                    self.cmd_manager.process_cmd(cmd)
        else:
            self.cmd_manager.process_cmd(self.cmds)

    def is_exit(self):
        return self.cmd_manager.exit_flag


def format_values(values):
    for i, value in enumerate(values):
        if "))" in value or 'varchar' in value:
            value = value.replace("))", "")
            value = value.strip('(,')
        else:
            value = value.strip('(,)')
        values[i] = value


def format_args(args):
    for i, arg in enumerate(args):
        args[i] = arg.strip(",\'")


def remove_comments(command):
    if "--" in command:
        comment_start = command.index("--")
        command = command[:comment_start]
    return command


class CommandManager:
    def __init__(self, dbms):
        self.primary_cmds = ("create", "drop", "use", "select", "alter",
                             "insert", "update", "delete", "exit", "from")
        self.dbms = dbms
        self.exit_flag = 0
        self.TS = 0

    def troubleshoot(self, *args):
        if self.TS:
            for arg in args:
                print(arg)

    def process_cmd(self, command):
        """
            Assumption: command is just a string containing one complete command
            Complete meaning it starts with a primary cmd and ends with ';'
        """
        command = remove_comments(command)
        commands = command.strip(';').split()
        primary_cmd, args = commands[0].lower(), commands[1:]
        if primary_cmd.lower() == '.exit':
            primary_cmd = '.exit'
        if self.TS:
            print("processing:", command)
            print("primary command:", primary_cmd)
        match primary_cmd:
            case "create":
                self.create_cmd(args)
            case "drop":
                self.drop_cmd(args)
            case "use":
                self.use_cmd(args)
            case "select":
                self.select_cmd(args)
            case "alter":
                self.alter_cmd(args)
            case "insert":
                self.insert_cmd(args)
            case "update":
                self.update_cmd(args)
            case "delete":
                self.delete_cmd(args)
            case "begin":
                self.begin_cmd()
            case "commit":
                self.commit_cmd()
            case ".exit":
                self.exit_cmd()
            case _:
                print("!Error: Command", primary_cmd, "not recognized")

    def create_cmd(self, args):
        self.troubleshoot(args)
        create_type, create_name = "", ""
        try:
            create_type, create_name = args[0].lower(), args[1]
        except IndexError as _:
            print("!Error: Missing creation type and/or creation name")
            return

        match create_type:
            case "database":
                self.dbms.create_database(create_name)
            case "table":
                format_check = create_name.split('(')
                create_name = format_check[0].lower()
                values = args[2:]
                if len(format_check) > 1:
                    values = ['(' + format_check[1]] + values
                format_values(values)
                self.dbms.curr_db.create_table(create_name, values)
            case _:
                print("!Error: Must specify either table or database creation.")

    def drop_cmd(self, args):
        try:
            drop_type = args[0].lower()
            drop_name = args[1]
        except IndexError as _:
            print("!Error: Missing Database/Table specifier or Title")
            return
        match drop_type:
            case "database":
                self.dbms.drop_database(drop_name)
            case "table":
                self.dbms.curr_db.drop_table(drop_name.lower())

    def use_cmd(self, args):
        db_name = args[0]
        self.dbms.set_curr_db(db_name)

    def select_cmd(self, args):
        args = [arg.lower() if arg.lower() in self.primary_cmds else arg for arg in args]
        from_index = args.index('from')
        if 'on' in args:
            condition_index = args.index('on')
        elif 'where' in args:
            condition_index = args.index('where')
        else:
            condition_index = len(args)
        select_vals = args[:from_index]
        format_args(select_vals)
        from_vals = args[from_index + 1:condition_index]
        condition_vals = args[condition_index + 1:]
        if len(from_vals) == 1:
            self.dbms.curr_db.query_table(from_vals[0].lower(), select_vals, condition_vals)
        else:
            self.dbms.curr_db.query_table(from_vals, select_vals, condition_vals)

    def alter_cmd(self, args):
        alter_type = args[0].lower()
        alter_name = args[1].lower()
        alter_values = args[3:]
        match alter_type:
            case "table":
                self.dbms.curr_db.alter_table(alter_name, alter_values)
            case _:
                print("!Error: Cannot alter", alter_type + "'s")

    def insert_cmd(self, args):
        table_name, values = args[1].lower(), args[2:]
        if len(values) > 1:
            # values(x, y, z) or values (x,y,z) or values (x, y, z)
            if "values(" in values[0]:
                for i, value in enumerate(values):
                    values[i] = value.replace("values(", '').strip(',\')')
            else:
                values = ''.join(values[1:])
                values = values.split(',')
                for i, value in enumerate(values):
                    values[i] = value.strip('()\'')
        else:
            # values(x,y,z)
            values = values[0].split(',')
            for i, value in enumerate(values):
                values[i] = value.replace("values(", '').strip(')\'')
        self.dbms.curr_db.insert_table(table_name, values)

    def update_cmd(self, args):
        table_name = args[0].lower()
        set_args = args[2:5]
        format_args(set_args)
        where_args = args[6:]
        format_args(where_args)
        self.dbms.curr_db.update_table(table_name, set_args, where_args)

    def delete_cmd(self, args):
        table_name = args[1].lower()
        where_args = args[3:]
        format_args(where_args)
        self.dbms.curr_db.delete_table_records(table_name, where_args)

    def begin_cmd(self):
        self.dbms.curr_db.set_transaction(True)

    def commit_cmd(self):
        self.dbms.curr_db.set_transaction(False)

    def exit_cmd(self):
        print("All done.")
        self.exit_flag = 1
