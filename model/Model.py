import mysql.connector
from mysql.connector import errorcode
import datetime
from model.Database import Database

class Model(Database):
    def create_model(self, name, model_type, path_model, path_data):
        cursor = self.connection.cursor(dictionary=True)
        query = """
        INSERT INTO Models (name, type, path_model, path_data)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (name, model_type, path_model, path_data))
        self.connection.commit()
        model_id = cursor.lastrowid
        cursor.close()
        return model_id

    def get_model(self, model_id):
        # cursor = self.connection.cursor(dictionary=True)
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT * FROM Models WHERE model_id = %s"
        cursor.execute(query, (model_id,))
        model = cursor.fetchone()
        cursor.close()
        return model
    
    def get_all_models(self):
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT * FROM Models"
        cursor.execute(query)
        models = cursor.fetchall()
        cursor.close()
        return models
    

    def get_latest_model(self):
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT * FROM Models ORDER BY model_id DESC LIMIT 1"
        cursor.execute(query)
        latest_model = cursor.fetchone()
        cursor.close()
        return latest_model

    def update_model(self, model_id, name=None, model_type=None, path_model=None, path_data=None):
        cursor = self.connection.cursor(dictionary=True)
        query = "UPDATE Models SET "
        updates = []
        params = []

        if name:
            updates.append("name = %s")
            params.append(name)
        if model_type:
            updates.append("type = %s")
            params.append(model_type)
        if path_model:
            updates.append("path_model = %s")
            params.append(path_model)
        if path_data:
            updates.append("path_data = %s")
            params.append(path_data)

        query += ", ".join(updates) + " WHERE model_id = %s"
        params.append(model_id)

        cursor.execute(query, tuple(params))
        self.connection.commit()
        cursor.close()

    def delete_model(self, model_id):
        cursor = self.connection.cursor(dictionary=True)
        query = "DELETE FROM Models WHERE model_id = %s"
        cursor.execute(query, (model_id,))
        self.connection.commit()
        cursor.close()
