import mysql.connector
from mysql.connector import errorcode
import datetime
from model.Database import Database


class Conversation(Database):
    # New Conversation
    def create_conversation(self, user_id, title=None):
        if title == None:
            last_conv = self.get_latest_conversation(user_id)
            if last_conv == None:
                title = f"conversation-1"
            else:
                title = f"conversation-{int(last_conv[0]) + 1}"
        
        cursor = self.connection.cursor()
        new_conversation_query = """
            INSERT INTO Conversations (user_id, title, started_at)
            VALUES (%s, %s, %s)
        """
        cursor.execute(new_conversation_query, (user_id, title, datetime.datetime.now()))
        self.connection.commit()
        cursor.close()
        return True
    
    # Get All Data Conversations
    def get_all_conversation(self, status, user_id):
        cursor = self.connection.cursor()
        if status == 'all':
            select_query = f"SELECT * FROM Conversations WHERE user_id = {user_id}  ORDER BY started_at ASC"
        elif status == 'active':
            select_query = f"SELECT * FROM Conversations WHERE user_id = {user_id} AND ended_at IS NULL ORDER BY started_at ASC"
        cursor.execute(select_query)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    # Get Lastest Data Conversation
    def get_latest_conversation(self, user_id, status='any'):
        cursor = self.connection.cursor()
        if status == 'any':
            select_query = f"SELECT * FROM Conversations WHERE user_id = {user_id} ORDER BY started_at DESC LIMIT 1"
        elif status == 'active':
            select_query = f"SELECT * FROM Conversations WHERE user_id = {user_id} AND ended_at IS NULL ORDER BY started_at DESC LIMIT 1"
        cursor.execute(select_query)
        row = cursor.fetchone()
        cursor.close()
        return row

    # Get One Data Conversation
    def get_conversation(self, conversation_id, user_id):
        cursor = self.connection.cursor()
        select_query = f"SELECT * FROM Conversations WHERE user_id = {user_id} AND conversation_id = {conversation_id} ORDER BY started_at DESC LIMIT 1"
        cursor.execute(select_query)
        row = cursor.fetchone()
        cursor.close()
        return row
        
    def edit_conversation(self, conversation_id, user_id, title):
        cursor = self.connection.cursor()
        update_query = """
            UPDATE Conversations
            SET user_id = %s, title = %s
            WHERE conversation_id = %s
        """
        cursor.execute(update_query, (user_id, title, conversation_id))
        self.connection.commit()
        cursor.close()
        return True
    
    def end_conversation(self, conversation_id, user_id):
        cursor = self.connection.cursor()
        update_query = """
            UPDATE Conversations
            SET ended_at = %s
            WHERE conversation_id = %s 
            AND user_id = %s
        """
        cursor.execute(update_query, (datetime.datetime.now(), conversation_id, user_id))
        self.connection.commit()
        cursor.close()
    
    def delete_conversation(self, conversation_id, user_id):
        cursor = self.connection.cursor()
        delete_query = "DELETE FROM Conversations WHERE conversation_id = %s AND user_id = %s"
        cursor.execute(delete_query, (conversation_id, user_id))
        self.connection.commit()
        cursor.close()
        return True
        
    

