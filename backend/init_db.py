import psycopg2
from app.core.db import get_db_connection, release_db_connection


def init_database():
    conn = get_db_connection()
    try:
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS chats (
                chat_id SERIAL PRIMARY KEY,
                chat_type VARCHAR(7) CHECK (chat_type IN ('private', 'group')) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                name VARCHAR(100)
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS chat_members (
                chat_member_id SERIAL PRIMARY KEY,
                chat_id INT REFERENCES chats(chat_id) ON DELETE CASCADE,
                user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (chat_id, user_id)
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                message_id SERIAL PRIMARY KEY,
                chat_id INT REFERENCES chats(chat_id) ON DELETE CASCADE,
                sender_id INT REFERENCES users(user_id) ON DELETE CASCADE,
                content TEXT NOT NULL,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_read BOOLEAN DEFAULT FALSE
            );
        """)

        conn.commit()
        print("Database tables initialized successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error initializing database: {e}")
        raise
    finally:
        cur.close()
        release_db_connection(conn)


if __name__ == "__main__":
    init_database()
