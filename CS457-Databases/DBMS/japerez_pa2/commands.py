"""
Author: Javier Perez
Date: 10/31/22
Description:
    This file defines the classes: CLI, CommandManager
    The CLI in this case will be the only object that we explicitly call in the
    main and serves as the users guide and interface when interacting with the
    database management system(DBMS).
    The database manager in this case will be the only object that we explicitly
    call in the main and serves as the users guide and access point into the
"""


class CLI:
    """
        Class Name: CLI
        Constructor:
            params: dbms (DatabaseManager - Object defined in database_classes.py)
        Description:
            - Defines and stores the methods/data necessary to prompt the user for input,
            process that input to test for its syntactical properties, and communicate that
            input to the database manager dbms.
            - Is called in the main function and can process user input from the command line, but
            also process a file filled with commands.
            - The command manager object cmd_manager is called to execute a processed commands
            contents and contains various helper functions for formatting commands.
    """
    def __init__(self, dbms):
        self.cmds = []
        self.is_batch = False
        self.cmd_manager = CommandManager(dbms)

    def prompt(self) -> [str]:
        cli_args = input("# ")
        cmd_list = []
        while True:
            if cli_args.lower() == ".exit":
                cmd_list = cli_args.lower()
                break
            if ';' in cli_args:
                if cli_args.strip(';'):
                    cmd_list.append(self.cmd_manager.format_cmd(cli_args))
                break
            else:
                cmd_list.append(self.cmd_manager.format_cmd(cli_args))
                cli_args = input("  ")
        self.cmds = cmd_list
        return self.cmds

    def batch_input(self, file_names):
        # Assume commands are syntactically correct, not grammatically
        # (i.e. starts with a valid command, ends with a semicolon s.t. semicolon is command delimiter
        batch_cmds = {}
        self.is_batch = True
        for file in file_names:
            with open(file, "r") as f:
                cmds = f.readlines()
                batch_cmds[file] = []
                cmd_list = []
                for cmd in cmds:
                    if cmd.lower() == ".exit\n":
                        batch_cmds[file].append(".exit")
                    if ';' in cmd:
                        cmd_list.append(self.cmd_manager.format_cmd(cmd))
                        batch_cmds[file].append(cmd_list)
                        cmd_list = []
                    elif cmd[:2] != '--' and cmd != '\n':
                        cmd_list.append(self.cmd_manager.format_cmd(cmd))
        self.cmds = batch_cmds

    def process_cmds(self):
        if self.is_batch:
            for file in self.cmds:
                for cmds in self.cmds[file]:
                    if cmds == ".exit":
                        print("All done.")
                        return
                    if len(cmds) == 1:
                        self.cmd_manager.parse_cmd(cmds[0])
                    else:
                        self.cmd_manager.parse_cmd(cmds)
        else:
            for cmd in self.cmds:
                self.cmd_manager.parse_cmd(cmd)

    def exit_cmd(self):
        if ".exit" in self.cmds:
            print("All done.")
            return True
        return False


class CommandManager:
    """
        Class Name: CommandManager
        Constructor:
            params: dbms (DatabaseManager - Object defined in database_classes.py)
        Description:
            - Defines and stores the methods/data necessary to execute commands processed
            by the CLI by passing the appropriate arguments to their respective methods
            according to its definition in the database_classes.py file.
            - Is called only by the CLI class and each command has various troubleshooting
            methods available.
            - The valid_cmds dictionary contains the commands we want to consider as
            not being case-sensitive.
        * Below is a visual guide that I used to implement the parsing algorithm for each
        command based on that database functions definition.
    """

    """
    Command structures:
        Database & Table
            Create:
                - create database database_name;
                - create table table_name values(options*);
            Drop:
                - drop (database | table) title;
            Use:
                - use title;
        Table
            Alter:
                - alter table table_name (table_values*);
            Select:
                - select variables* from table_name (where | lambda);
            Insert:
                - insert into table_name values(options*);
            Update:
                - update title_name set() where();
            Delete:
                - delete from database_name (where);
        Other
            Where:
                - where var_name (= | > | < | >= | <= | !=) value
            Set:
                - set var_name = value
    """

    def __init__(self, dbms):
        self.dbms = dbms
        self.troubleshooting = False
        self.valid_cmds = ("create", "drop", "use", "alter", "select",
                           "insert", "update", "delete", "where", "set",
                           "exit", "database", "table", "values", "from")

    def parse_cmd(self, cmd: [str]):
        cmd_name, args = "", []
        if type(cmd[0]) != str:
            cmd_name = cmd[0][0]
            cmd[0] = cmd[0][1:]
            args = cmd
        else:
            cmd_name = cmd[0]
            args = cmd[1:]
        if self.troubleshooting:
            print("\t", cmd_name, args)
        match cmd_name:
            case "create":
                self.create_cmd(args)
            case "drop":
                self.drop_cmd(args)
            case "use":
                self.use_cmd(args[0])
            case "alter":
                self.alter_cmd(args)
            case "select":
                self.select_cmd(args)
            case "insert":
                # insert cmd -> insert into table_name values(*);
                # want to only pass key arguments (i.e. skip 'into')
                self.insert_cmd(args[1:])
            case "update":
                self.update_cmd(args)
            case "delete":
                self.delete_cmd(args)
            case _:
                print("!Error: Command not recognized")
        if self.troubleshooting:
            print()

    def format_cmd(self, cmds):
        updated_cmds = []
        strip_chars1 = '\'(\n;,'
        strip_chars2 = '\'()\n;,'
        split_cmds = cmds.split()
        for i, cmd in enumerate(split_cmds):
            if 'values' in cmd:
                args = cmd.split("(")
                split_cmds[i] = args[0]
                split_cmds.insert(i + 1, args[1])
        for cmd in split_cmds:
            if "(" in cmd and "))" in cmd:
                cmd = cmd.replace("))", ")")
                stripped_cmd = cmd.strip(strip_chars1)
            else:
                stripped_cmd = cmd.strip(strip_chars2)
            if stripped_cmd.lower() in self.valid_cmds:
                lowered_cmds = stripped_cmd.lower()
            else:
                lowered_cmds = stripped_cmd
            updated_cmds.append(lowered_cmds)
        return updated_cmds

    def create_cmd(self, args: [str]):
        type_arg = args[0]
        name_arg = args[1]
        values = args[2:]
        if self.troubleshooting:
            print("\tCreate:", type_arg, name_arg, values)
        match type_arg:
            case "database":
                self.dbms.create_database(name_arg)
            case "table":
                self.dbms.curr_db.create_table(name_arg, values)
            case _:
                print(name_arg)

    def drop_cmd(self, args: [str]):
        type_arg = args[0]
        name_arg = args[1]
        if self.troubleshooting:
            print("\tDrop:", type_arg, name_arg)
        match type_arg:
            case "database":
                self.dbms.drop_database(name_arg)
            case "table":
                self.dbms.curr_db.drop_table(name_arg)

    def use_cmd(self, arg: str):
        if self.troubleshooting:
            print("\tUse:", arg)
        self.dbms.set_curr_db(arg)

    def alter_cmd(self, args: [str]):
        type_arg = args[0]
        name_arg = args[1]
        function_arg = args[2]
        values = args[3:]
        if self.troubleshooting:
            print("\tAlter:", type_arg, name_arg, function_arg, values)
        match type_arg:
            case "table":
                self.dbms.curr_db.alter_table(name_arg, values)
            case _:
                print("!Error: cannot alter ", type_arg, "'s")

    def select_cmd(self, args: [str]):
        if type(args[0]) == str:
            from_index = args.index("from")
            values_arg = args[:from_index]
            from_src = args[from_index + 1]
            if self.troubleshooting:
                print("\tSelect:", values_arg, from_src)
            if values_arg[0] == "*":
                self.dbms.curr_db.query_table(from_src, values_arg[0])
            else:
                self.dbms.curr_db.query_table(from_src, values_arg)
        else:
            if self.troubleshooting:
                print("\tSelect:", args)
            select_var = args[0]
            table_name = args[1][1]
            where_args = args[2][1:]
            self.dbms.curr_db.query_table(table_name, select_var, where_args)

    def insert_cmd(self, args: [str]):
        table_name = args[0]
        values_index = args.index('values')
        values = args[values_index + 1:]
        if self.troubleshooting:
            print("\tInsert:", table_name, values)
        self.dbms.curr_db.insert_table(table_name, values)

    def update_cmd(self, args: [str]):
        # format: update table_name set(var_name, new_value) where(var_name, var_value)
        # args: [[table_name] [[set var_name new_value] [where var_name var_value]]
        if self.troubleshooting:
            print("\tUpdate:", args)
        table_name = args[0][0]
        set_args = args[1][1:]
        where_args = args[2][1:]
        self.dbms.curr_db.update_table(table_name, set_args, where_args)

    def delete_cmd(self, args: [str]):
        if self.troubleshooting:
            print("\tDelete", args)
        table_name = args[0][1]
        where_args = args[1][1:]
        self.dbms.curr_db.delete_table_records(table_name, where_args)
