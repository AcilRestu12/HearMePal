import mysql.connector
from mysql.connector import errorcode
import datetime
from model.Database import Database


class Message(Database):
    
    # Fungsi untuk menyimpan pesan ke tabel Messages
    def insert_message(self, conversation_id, sender, content):
        cursor = self.connection.cursor(dictionary=True)
        insert_message_query = """
            INSERT INTO Messages (conversation_id, sender, content)
            VALUES (%s, %s, %s)
        """
        cursor.execute(insert_message_query, (conversation_id, sender, content))
        self.connection.commit()
        cursor.close()
        
    # Fungsi untuk memperbarui tabel Conversations dengan waktu berakhir
    def end_conversation(self, conversation_id):
        cursor = self.connection.cursor(dictionary=True)
        update_conversation_query = """
            UPDATE Conversations
            SET ended_at = %s
            WHERE conversation_id = %s
        """
        cursor.execute(update_conversation_query, (datetime.datetime.now(), conversation_id))
        self.connection.commit()
        cursor.close()
        
    # Fungsi untuk membaca semua data dari tabel Messages
    def get_all_messages(self, conversation_id):
        cursor = self.connection.cursor(dictionary=True)
        select_query = f"SELECT * FROM Messages WHERE conversation_id = {conversation_id} ORDER BY timestamp ASC"
        cursor.execute(select_query)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    # Fungsi untuk mendapatkan satu data terbaru dari tabel Messages
    def get_latest_message(self, conversation_id):
        cursor = self.connection.cursor(dictionary=True)
        select_query = f"SELECT * FROM Messages WHERE conversation_id = {conversation_id} ORDER BY timestamp DESC LIMIT 1"
        cursor.execute(select_query)
        row = cursor.fetchone()
        cursor.close()
        return row

