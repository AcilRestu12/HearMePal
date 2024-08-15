import mysql.connector
from mysql.connector import errorcode
import datetime
from model.Database import Database

class Language(Database):
    def create_language(self, name, code):
        cursor = self.connection.cursor(dictionary=True)
        query = """
        INSERT INTO Languages (name, code)
        VALUES (%s, %s)
        """
        cursor.execute(query, (name, code))
        self.connection.commit()
        language_id = cursor.lastrowid
        cursor.close()
        return language_id

    def get_language(self, language_id):
        # cursor = self.connection.cursor(dictionary=True)
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT * FROM Languages WHERE language_id = %s"
        cursor.execute(query, (language_id,))
        language = cursor.fetchone()
        cursor.close()
        return language
    
    def get_oldest_language(self):
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT * FROM Languages ORDER BY language_id ASC LIMIT 1"
        cursor.execute(query)
        oldest_lang = cursor.fetchone()
        cursor.close()
        return oldest_lang
    
    def get_all_languages(self):
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT * FROM Languages"
        cursor.execute(query)
        languages = cursor.fetchall()
        cursor.close()
        return languages


    def update_language(self, language_id, name=None, code=None):
        cursor = self.connection.cursor(dictionary=True)
        query = "UPDATE Languages SET "
        updates = []
        params = []

        if name:
            updates.append("name = %s")
            params.append(name)
        if code:
            updates.append("code = %s")
            params.append(code)

        query += ", ".join(updates) + " WHERE language_id = %s"
        params.append(language_id)

        cursor.execute(query, tuple(params))
        self.connection.commit()
        cursor.close()
        return True

    def delete_language(self, language_id):
        cursor = self.connection.cursor(dictionary=True)
        query = "DELETE FROM Languages WHERE language_id = %s"
        cursor.execute(query, (language_id,))
        self.connection.commit()
        cursor.close()
