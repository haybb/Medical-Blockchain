from app import mysql, session


class Table:
    def __init__(self, table_name, *args):
        """
        Constructor of the Table class
        :param table_name: name of the table
        :param args: columns of our table
        """
        self.table = table_name
        self.columns = '(%s)' % ','.join(args)

        if is_new_table(table_name):
            cur = mysql.connection.cursor()
            cur.execute("CREATE TABLE %s%s" % (self.table, self.columns))
            cur.close()

    def get_all_values(self):
        """
        :return: all values from the table
        """
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM %s" % self.table)
        data = cur.fetchall()
        return data

    def get_one_value(self, search, value):
        """
        Get one value from the table based on a column's data
        :param search: value to search in the table
        :param value: value we are looking for
        :return: data of the value searched
        """
        data = {}
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM %s WHERE %s = \"%s\"" % (self.table, search, value))
        if result > 0:
            data = cur.fetchone()
        cur.close()
        return data

    def delete_one_value(self, search, value):
        """
        Delete a value from the table based on column's data
        :param search: value to search in the table
        :param value:  value we were searching
        :return: /
        """
        cur = mysql.connection.cursor()
        cur.execute("DELETE from %s where %s = \"%s\"" % (self.table, search, value))
        mysql.connection.commit()
        cur.close()

    def delete_all_values(self):
        """
        Delete all values from the table
        :return: /
        """
        self.drop()  # remove table and recreate
        self.__init__(self.table, *self.columnsList)

    def drop(self):
        """
        Remove table from mysql
        :return: /
        """
        cur = mysql.connection.cursor()
        cur.execute("DROP TABLE %s" % self.table)
        cur.close()

    def insert(self, *args):
        """
        Insert values into the table
        :param args: values to insert
        :return: /
        """
        data = ""
        for arg in args:  # convert data into string mysql format
            data += "\"%s\"," % (arg)

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO %s%s VALUES(%s)" % (self.table, self.columns, data[:len(data) - 1]))
        mysql.connection.commit()
        cur.close()


def is_new_table(table_name):
    """
    Verifies if it's a new table or not
    :param table_name: table to check its existence
    :return: True if it's a new table, False otherwise
    """
    cur = mysql.connection.cursor()

    try:
        result = cur.execute("SELECT * from %s" % table_name)
        cur.close()
    except:
        return True
    else:
        return False
