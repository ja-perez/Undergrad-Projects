"""
Author: Javier Perez
Date: 10/10/22
Compilation: This program was written in pycharm using Python 3.10
and may be run on any linux machine with this version of python installed using
the command: python3 japerez_pa1.py
    - Optionally, the program may also parse a file containing a list of commands using:
    python3 japerez_pa1.py textfile_name
Description:
    - This file defines our database management systems(DMBS) main function,
    and its associated helper functions, along with the users command line interface(CLI).
    - The main creates and manages a DatabaseManager object from the database_classes file
    and uses its method in order to create, update, delete, and query databases and their
    respective tables.
    - Databases are organized as directories, and their tables are created as tables within
    their respective database directories. The Database Manager exists within the working
    directory in which the program is called.
"""

import sys
import database_classes as db_c


def is_input_valid(cmds: [str]) -> bool:
    valid_functions = ["CREATE", "DROP", "SELECT", "ALTER", "USE", ".EXIT", "CASE_SENSITIVE"]
    return (";" == cmds[-1][-1] or cmds[0] == ".EXIT") and cmds[0] in valid_functions


def remove_trailing_chars(cmd_list):
    remove_chars = ',();'
    for i, param in enumerate(cmd_list):
        if 'varchar' in param or 'char' in param:
            cmd_list[i] = param.strip(',(;') if param.count(')') == 1 else param.strip(',(;')[:-1]
        else:
            cmd_list[i] = param.strip(remove_chars)


def parse_cmd(usr_cmd: str, db_manager: db_c.DatabaseManager):
    usr_cmd = usr_cmd.split()
    cmd_function = usr_cmd[0]
    cmd_value = usr_cmd[1]
    cmd_target = usr_cmd[-1][:-1] if (cmd_function != "CREATE" and cmd_value != "TABLE") or len(usr_cmd) < 4 \
        else usr_cmd[3:]

    match cmd_function:
        case "CREATE":
            if cmd_value == "DATABASE":
                db_manager.create_database(cmd_target)
            elif cmd_value == "TABLE":
                table_name = usr_cmd[2]
                remove_trailing_chars(cmd_target)
                db_manager.curr_db.create_table(table_name, cmd_target)
        case "DROP":
            if cmd_value == "DATABASE":
                db_manager.drop_database(cmd_target)
            elif cmd_value == "TABLE":
                db_manager.curr_db.drop_table(cmd_target)
        case "SELECT":
            from_index = usr_cmd.index("FROM")
            cmd_target = usr_cmd[-1][:-1]
            cmd_value = usr_cmd[1:from_index]
            if "*" in cmd_value:
                db_manager.curr_db.query_table(cmd_target, cmd_value[0])
            else:
                db_manager.curr_db.query_table(cmd_target[0][:-1], cmd_value)
        case "ALTER":
            cmd_target = usr_cmd[2]
            cmd_value = usr_cmd[4:]
            remove_trailing_chars(cmd_value)
            db_manager.curr_db.update_table(cmd_target, cmd_value)
        case "USE":
            db_manager.set_curr_db(cmd_target)
        case "CASE_SENSITIVE":
            db_manager.is_case_sensitive = int(cmd_target)
        case ".EXIT":
            return usr_cmd


def prompt_user(dbms) -> str:
    usr_input = input('# ')
    usr_cmds = usr_input.split()
    if not dbms.is_case_sensitive:
        if len(usr_cmds) == 1:
            usr_cmds[0] = usr_cmds[0].upper()
            usr_input = usr_cmds[0]
        else:
            usr_cmds = [cmd.upper() for cmd in usr_cmds[:-1]]
            usr_cmds.append(usr_input.split()[-1])
            usr_input = ' '.join([cmd.upper() for cmd in usr_cmds[:-1]]) + " " + usr_cmds[-1]
    return usr_input if not usr_input or is_input_valid(usr_cmds) \
        else "error"


def main():
    test_file = sys.argv
    dbms = db_c.DatabaseManager()
    if not test_file[1:]:
        while True:
            usr_cmd = prompt_user(dbms)
            if "error" in usr_cmd:
                print("!Error: Command not recognized")
            elif ".EXIT" == usr_cmd:
                print("All done.")
                break
            elif usr_cmd:
                parse_cmd(usr_cmd, dbms)
    else:
        test_cmds = []
        with open('PA1_test.sql', 'r') as file:
            for line in file:
                if '--' not in line and line != '\n':
                    test_cmds.append(line[:-1])
        # Assume test commands are valid syntactically
        for cmd in test_cmds:
            if cmd == ".EXIT":
                print("All done.")
                break
            else:
                parse_cmd(cmd, dbms)


if __name__ == "__main__":
    main()
