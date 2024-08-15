import mysql.connector
from mysql.connector import errorcode
import datetime
import hashlib

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
        email VARCHAR(100) NOT NULL UNIQUE,
        full_name VARCHAR(100) NOT NULL,
        password VARCHAR(255) NOT NULL,
        role ENUM('user', 'admin') NOT NULL DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );
    """

    # Query untuk membuat tabel Profiles
    # create_profiles_table = """
    # CREATE TABLE IF NOT EXISTS Profiles (
    #     profile_id INT AUTO_INCREMENT PRIMARY KEY,
    #     user_id INT NOT NULL,
    #     full_name VARCHAR(100) NOT NULL,
    #     age INT,
    #     gender VARCHAR(10),
    #     bio TEXT,
    #     profile_pic VARCHAR(255),
    #     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    #     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    #     FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
    # );
    # """

    # Query untuk membuat tabel Conversations
    create_conversations_table = """
    CREATE TABLE IF NOT EXISTS Conversations (
        conversation_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        title VARCHAR(100) NOT NULL,
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
    
    # Query untuk membuat tabel Languages
    create_languages_table = """
    CREATE TABLE IF NOT EXISTS Languages (
        language_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50) NOT NULL UNIQUE,
        code VARCHAR(10) NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );
    """

    # Query untuk membuat tabel Models dengan kolom tambahan
    create_models_table = """
    CREATE TABLE IF NOT EXISTS Models (
        model_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL UNIQUE,
        type VARCHAR(100) NOT NULL,
        path_model VARCHAR(255) NOT NULL,
        path_data VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );
    """

    # Query untuk membuat tabel Preferences
    create_preferences_table = """
    CREATE TABLE IF NOT EXISTS Preferences (
        preference_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        language_id INT NOT NULL,
        model_id INT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
        FOREIGN KEY (language_id) REFERENCES Languages(language_id) ON DELETE CASCADE,
        FOREIGN KEY (model_id) REFERENCES Models(model_id) ON DELETE CASCADE
    );
    """

    # Eksekusi query untuk membuat tabel
    try:
        cursor.execute(create_users_table)
        print(f'------create_users_table done')
        # cursor.execute(create_profiles_table)
        cursor.execute(create_conversations_table)
        print(f'------create_conversations_table done')
        cursor.execute(create_messages_table)
        print(f'------create_messages_table done')
        cursor.execute(create_feedback_table)
        print(f'------create_feedback_table done')
        cursor.execute(create_languages_table)
        print(f'------create_languages_table done')
        cursor.execute(create_models_table)
        print(f'------create_models_table done')
        cursor.execute(create_preferences_table)
        print(f'------create_preferences_table done')
        print("\n Tables created successfully.\n\n")
    except mysql.connector.Error as err:
        print(f"\n Error: {err} \n\n")
    finally:
        cursor.close()

def hash_password(password):
    # Menggunakan hashing SHA-256 untuk menyimpan password dengan aman
    return hashlib.sha256(password.encode()).hexdigest()

# Fungsi untuk membuat entri baru di tabel Conversations
def create_conversation(connection, user_id, title):
    cursor = connection.cursor()
    insert_query = """
        INSERT INTO Conversations (user_id, title, started_at)
        VALUES (%s, %s, %s)
    """
    cursor.execute(insert_query, (user_id, title, datetime.datetime.now()))
    connection.commit()
    cursor.close()

# Fungsi untuk membuat entri baru di tabel Users
def create_user(connection, username, email, full_name, password, role='user'):
    cursor = connection.cursor()
    hashed_password = hash_password(password)
    insert_query = """
        INSERT INTO Users (username, email, full_name, password, role)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (username, email, full_name, hashed_password, role))
    connection.commit()
    user_id = cursor.lastrowid
    cursor.close()
    return user_id

# Fungsi untuk membuat entri baru di tabel Languages
def create_language(connection, name, code):
    cursor = connection.cursor()
    insert_query = """
        INSERT INTO Languages (name, code)
        VALUES (%s, %s)
    """
    cursor.execute(insert_query, (name, code))
    connection.commit()
    language_id = cursor.lastrowid
    cursor.close()
    return language_id

# Fungsi untuk membuat entri baru di tabel Models
def create_model(connection, name, type, path_model, path_data):
    cursor = connection.cursor()
    insert_query = """
        INSERT INTO Models (name, type, path_model, path_data)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(insert_query, (name, type, path_model, path_data))
    connection.commit()
    model_id = cursor.lastrowid
    cursor.close()
    return model_id

# Fungsi untuk membuat entri baru di tabel Preferences
def create_preference(connection, user_id, language_id, model_id):
    cursor = connection.cursor()
    insert_query = """
        INSERT INTO Preferences (user_id, language_id, model_id)
        VALUES (%s, %s, %s)
    """
    cursor.execute(insert_query, (user_id, language_id, model_id))
    connection.commit()
    preference_id = cursor.lastrowid
    cursor.close()


# Fungsi utama
def main():
    create_db(DB_NAME)
    connection = create_connection(DB_NAME)
    if connection:
        create_tables(connection)
        
        model_id = create_model(connection, 'HMP', 'NN-Pytorch', 'data/meta/data_nn.pth', 'data/intents_3.json')
        print(f'------create_model done')
        user_id = create_user(connection, 'admin', 'admin@mail.com', 'administrator', '123123123', 'admin')
        print(f'------create_user done')
        
        language_id = create_language(connection, 'English', 'en')
        print(f'------create_language 1 done')
        create_language(connection, 'Indonesia', 'id')
        print(f'------create_language 2 done')
        
        create_conversation(connection, user_id, 'conv-1')
        print(f'------create_conversation done')
        create_preference(connection, user_id, language_id, model_id)
        print(f'------create_preference done')
        connection.close()

if __name__ == "__main__":
    main()
