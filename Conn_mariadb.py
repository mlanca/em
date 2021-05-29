import mariadb
import sys
import configparser


class Conn_mariadb:
    connCount = 0

    def __init__(self, main_table):
        self.main_table = main_table

        Conn_mariadb.connCount += 1

    def conndb(self, close_conn=False):
        try:
            config = configparser.ConfigParser()
            config.read('env.ini')
            conn = mariadb.connect(
                user=config['DEFAULT']['USER'],
                password=config['DEFAULT']['PASSWORD'],
                host=config['DEFAULT']['HOST'],
                port=int(config['DEFAULT']['PORT']),
                database=config['DEFAULT']['DATABASE']
            )
            conn.autocommit = True
            return conn.cursor()
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        except mariadb.IntegrityError as e:
            print(f"MariaDB Platform: {e}")
            sys.exit(1)
        finally:
            if close_conn:
                conn.close()

    def count_Clients(self):
        try:
            cursor = Conn_mariadb.conndb(self)
            cursor.execute('SELECT COUNT(*) FROM ' + self.main_table)
            return cursor.fetchone()[0]
        except Exception as error:
            print(error)
            print(type(error))
            print("Unexpected error:", sys.exc_info()[0])
            raise

    def select_to_list(self):
        try:
            cursor = Conn_mariadb.conndb(self)
            cursor.execute('select email from ' + self.main_table)
            email_list = []
            for x in cursor:
                email_list.append(x[0])
            return email_list
        except Exception as error:
            print(error)
            print(type(error))
            print("Unexpected error:", sys.exc_info()[0])
            raise
        finally:
            if cursor:
                Conn_mariadb.conndb(True)

    def update_keyvalue(self, new_value, target_key):
        try:
            cursor = Conn_mariadb.conndb(self)
            statement = "UPDATE em_keyvalue SET val = %s WHERE target_key = %s"
            data = (new_value, target_key)
            cursor.execute(statement, data)
            return "Update submitted"
        except Exception as error:
            print(error)
            print(type(error))
            print("Unexpected error:", sys.exc_info()[0])
            raise
        finally:
            if cursor:
                Conn_mariadb.conndb(True)

    def add_client(self, fname, email, created):
        try:
            cursor = Conn_mariadb.conndb(self)
            search_data = Conn_mariadb.select_to_list(self)
            if email in search_data:
                return "Already there"

            statement = "INSERT INTO clients (fname,email,created) VALUES (%s, %s, %s)"
            data = (fname, email, created)
            cursor.execute(statement, data)
            return "Successfully added entry to database"
        except Exception as error:
            print(error)
            print(type(error))
            print("Unexpected error:", sys.exc_info()[0])
            raise
        finally:
            Conn_mariadb.conndb(True)

    @staticmethod
    def display_count():
        print("Total Connection Count %d" % Conn_mariadb.connCount)


if __name__ == '__main__':
    conn = Conn_mariadb('clients')
    res = conn.add_client('l', 'l')
    print(res)
