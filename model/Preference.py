import mysql.connector
from mysql.connector import errorcode
import datetime
from model.Database import Database

class Preference(Database):
    def create_preference(self, user_id, language_id, model_id):
        cursor = self.connection.cursor(dictionary=True)
        query = """
        INSERT INTO Preferences (user_id, language_id, model_id)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (user_id, language_id, model_id))
        self.connection.commit()
        cursor.close()
        return True

    def get_preference(self, preference_id):
        # cursor = self.connection.cursor(dictionary=True)
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT * FROM Preferences WHERE preference_id = %s"
        cursor.execute(query, (preference_id,))
        preference = cursor.fetchone()
        cursor.close()
        return preference
    
    def get_preferences_by_user_id(self, user_id):
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT * FROM Preferences WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        preferences = cursor.fetchone()
        cursor.close()
        return preferences

    def update_preference(self, preference_id, user_id=None, language_id=None, model_id=None):
        cursor = self.connection.cursor(dictionary=True)
        query = "UPDATE Preferences SET "
        updates = []
        params = []

        if user_id:
            updates.append("user_id = %s")
            params.append(user_id)
        if language_id:
            updates.append("language_id = %s")
            params.append(language_id)
        if model_id:
            updates.append("model_id = %s")
            params.append(model_id)

        query += ", ".join(updates) + " WHERE preference_id = %s"
        params.append(preference_id)

        cursor.execute(query, tuple(params))
        self.connection.commit()
        cursor.close()
        return True


    def delete_preference(self, preference_id):
        cursor = self.connection.cursor(dictionary=True)
        query = "DELETE FROM Preferences WHERE preference_id = %s"
        cursor.execute(query, (preference_id,))
        self.connection.commit()
        cursor.close()
