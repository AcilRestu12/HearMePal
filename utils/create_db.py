import mysql.connector
from mysql.connector import errorcode
import datetime

DB_NAME = 'db_hearmepal'

def create_db(db_name):
    db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
    )

    cursor = db.cursor()
    
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print("Database created successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

# Fungsi untuk membuat koneksi ke database
def create_connection(db_name):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database=db_name
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Fungsi untuk membuat tabel
def create_tables(connection):
    cursor = connection.cursor()

    # Query untuk membuat tabel Users
    create_users_table = """
    CREATE TABLE IF NOT EXISTS Users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );
    """

    # Query untuk membuat tabel Profiles
    create_profiles_table = """
    CREATE TABLE IF NOT EXISTS Profiles (
        profile_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        full_name VARCHAR(100) NOT NULL,
        age INT,
        gender VARCHAR(10),
        bio TEXT,
        profile_pic VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
    );
    """

    # Query untuk membuat tabel Conversations
    create_conversations_table = """
    CREATE TABLE IF NOT EXISTS Conversations (
        conversation_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ended_at TIMESTAMP NULL DEFAULT NULL,
        FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
    );
    """

    # Query untuk membuat tabel Messages
    create_messages_table = """
    CREATE TABLE IF NOT EXISTS Messages (
        message_id INT AUTO_INCREMENT PRIMARY KEY,
        conversation_id INT NOT NULL,
        sender ENUM('user', 'bot') NOT NULL,
        content TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (conversation_id) REFERENCES Conversations(conversation_id) ON DELETE CASCADE
    );
    """

    # Query untuk membuat tabel Feedback
    create_feedback_table = """
    CREATE TABLE IF NOT EXISTS Feedback (
        feedback_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        conversation_id INT NOT NULL,
        rating INT CHECK (rating >= 1 AND rating <= 5),
        comments TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
        FOREIGN KEY (conversation_id) REFERENCES Conversations(conversation_id) ON DELETE CASCADE
    );
    """

    # Eksekusi query untuk membuat tabel
    try:
        cursor.execute(create_users_table)
        cursor.execute(create_profiles_table)
        cursor.execute(create_conversations_table)
        cursor.execute(create_messages_table)
        cursor.execute(create_feedback_table)
        print("Tables created successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

# Fungsi untuk membuat entri baru di tabel Conversations
def create_conversation(connection, user_id):
    cursor = connection.cursor()
    insert_query = """
        INSERT INTO Conversations (user_id, started_at)
        VALUES (%s, %s)
    """
    cursor.execute(insert_query, (user_id, datetime.datetime.now()))
    connection.commit()
    cursor.close()

# Fungsi untuk membuat entri baru di tabel Conversations
def create_user(connection, username, password, email):
    cursor = connection.cursor()
    insert_query = """
        INSERT INTO Users (username, password, email)
        VALUES (%s, %s, %s)
    """
    cursor.execute(insert_query, (username, password, email))
    connection.commit()
    user_id = cursor.lastrowid
    cursor.close()
    return user_id


# Fungsi utama
def main():
    create_db(DB_NAME)
    connection = create_connection(DB_NAME)
    if connection:
        create_tables(connection)
        user_id = create_user(connection, 'admin', 'qwerty', 'admin@mail.com')
        create_conversation(connection, user_id)
        connection.close()

if __name__ == "__main__":
    main()
