import mysql.connector
from mysql.connector import errorcode

class Database():
    def __init__(self, host, user, password, db_name):
        self.connection = self.create_connection(host, user, password, db_name)
        
    # Fungsi untuk membuat koneksi ke database
    def create_connection(self, host, user, password, db_name):
        try:
            connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            return connection
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None