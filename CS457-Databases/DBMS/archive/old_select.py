def select_values(self, select_values, conditions, table_join=None, attr_join=None):
    if select_values[0] == "*" and not conditions:
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
        select_ids, where_args = select_values, conditions
        where_var, where_op, where_val = where_args
        where_col = 0
        where_var = where_var.split('.')[1]
        where_val = where_val.split('.')[1]

        if table_join:
            rows = table_join
        else:
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