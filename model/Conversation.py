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
                title = f"conv-1"
            else:
                title = f"conv-{int(last_conv['conversation_id']) + 1}"
        
        cursor = self.connection.cursor(dictionary=True)
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
        cursor = self.connection.cursor(dictionary=True)
        if status == 'all':
            select_query = f"SELECT * FROM Conversations WHERE user_id = {user_id} ORDER BY started_at ASC"
        elif status == 'active':
            select_query = f"SELECT * FROM Conversations WHERE user_id = {user_id} AND ended_at IS NULL ORDER BY started_at ASC"
        elif status == 'archived':
            select_query = f"SELECT * FROM Conversations WHERE user_id = {user_id} AND ended_at IS NOT NULL ORDER BY started_at ASC"
        cursor.execute(select_query)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    # Get Lastest Data Conversation
    def get_latest_conversation(self, user_id, status='any'):
        cursor = self.connection.cursor(dictionary=True)
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
        cursor = self.connection.cursor(dictionary=True)
        select_query = f"SELECT * FROM Conversations WHERE user_id = {user_id} AND conversation_id = {conversation_id} ORDER BY started_at DESC LIMIT 1"
        cursor.execute(select_query)
        row = cursor.fetchone()
        cursor.close()
        return row
        
    def edit_conversation(self, conversation_id, user_id, title):
        cursor = self.connection.cursor(dictionary=True)
        update_query = """
            UPDATE Conversations
            SET user_id = %s, title = %s
            WHERE conversation_id = %s
        """
        cursor.execute(update_query, (user_id, title, conversation_id))
        self.connection.commit()
        cursor.close()
        return True
    
    def start_conversation(self, conversation_id, user_id):
        cursor = self.connection.cursor(dictionary=True)
        update_query = """
            UPDATE Conversations
            SET ended_at = NULL
            WHERE conversation_id = %s 
            AND user_id = %s
        """
        cursor.execute(update_query, (conversation_id, user_id))
        self.connection.commit()
        cursor.close()
    
    def end_conversation(self, conversation_id, user_id):
        cursor = self.connection.cursor(dictionary=True)
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
        cursor = self.connection.cursor(dictionary=True)
        delete_query = "DELETE FROM Conversations WHERE conversation_id = %s AND user_id = %s"
        cursor.execute(delete_query, (conversation_id, user_id))
        self.connection.commit()
        cursor.close()
        return True
    
    def get_archived_conversations(self, user_id):
        cursor = self.connection.cursor()
        query = f"SELECT COUNT(*) FROM Conversations WHERE user_id = {user_id} AND ended_at IS NOT NULL"
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else 0
        
    def end_all_conversation(self, user_id):
        cursor = self.connection.cursor(dictionary=True)
        query = """
            UPDATE Conversations
            SET ended_at = %s
            WHERE user_id = %s 
        """
        cursor.execute(query, (datetime.datetime.now(), user_id))
        self.connection.commit()
        cursor.close()
        
    def delete_all_conversation(self, user_id):
        cursor = self.connection.cursor(dictionary=True)
        query = "DELETE FROM Conversations WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        self.connection.commit()
        cursor.close()

