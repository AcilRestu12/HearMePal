import hashlib
import datetime
import mysql.connector
from mysql.connector import errorcode
from model.Database import Database

class User(Database):
    def hash_password(self, password):
        # Menggunakan hashing SHA-256 untuk menyimpan password dengan aman
        return hashlib.sha256(password.encode()).hexdigest()
    
    def is_username_taken(self, username):
        cursor = self.connection.cursor()
        query = "SELECT user_id FROM Users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    def is_email_taken(self, email):
        cursor = self.connection.cursor()
        query = "SELECT user_id FROM Users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        cursor.close()
        return result is not None
    
    def verify_password(self, password, hashed_password):
        return self.hash_password(password) == hashed_password
    
    def login(self, email, password):
        cursor = self.connection.cursor()
        query = "SELECT user_id, username, password FROM Users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            user_id, username, hashed_password = result
            if self.verify_password(password, hashed_password):
                print(f'\n {username} berhasil login')
                print(f'{type(result)} ')
                print(f'{result} \n\n')
                return result
            else:
                return "Incorrect password."
        else:
            return "Email not found."
    
    def register_user(self, username, email, full_name, password, confirm_password):
        if self.is_username_taken(username):
            return "Username already taken."
        
        if self.is_email_taken(email):
            return "Email already registered."

        if password != confirm_password:
            return "Password & confirm password do not match."

        hashed_password = self.hash_password(password)
        cursor = self.connection.cursor()
        query = """
            INSERT INTO Users (username, email, full_name, password)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (username, email, full_name, hashed_password))
        self.connection.commit()
        cursor.close()
        return True

    def get_user_by_id(self, user_id):
        cursor = self.connection.cursor()
        query = "SELECT user_id, username, email, created_at FROM Users WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def get_user_by_username(self, username):
        cursor = self.connection.cursor()
        query = "SELECT user_id, username, email, created_at FROM Users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def get_user_by_email(self, email):
        cursor = self.connection.cursor()
        query = "SELECT user_id, username, email, created_at FROM Users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def update_user_password(self, user_id, new_password):
        cursor = self.connection.cursor()
        query = "UPDATE Users SET password = %s, updated_at = CURRENT_TIMESTAMP WHERE user_id = %s"
        cursor.execute(query, (new_password, user_id))
        self.connection.commit()
        cursor.close()
        return "Password updated successfully"

    def update_user_details(self, user_id, new_username=None, new_fullname=None, new_email=None):
        cursor = self.connection.cursor()
        fields_to_update = []
        values = []

        if new_username:
            fields_to_update.append("username = %s")
            values.append(new_username)

        if new_fullname:
            fields_to_update.append("full_name = %s")
            values.append(new_fullname)

        if new_email:
            fields_to_update.append("email = %s")
            values.append(new_email)

        if fields_to_update:
            query = f"UPDATE Users SET {', '.join(fields_to_update)}, updated_at = CURRENT_TIMESTAMP WHERE user_id = %s"
            values.append(user_id)
            cursor.execute(query, tuple(values))
            self.connection.commit()

        cursor.close()
        return "User details updated successfully"

    def delete_user(self, user_id):
        cursor = self.connection.cursor()
        query = "DELETE FROM Users WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        self.connection.commit()
        cursor.close()
        return "User deleted successfully"
