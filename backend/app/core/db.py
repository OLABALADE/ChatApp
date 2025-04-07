from psycopg2 import pool
from app.core.config import settings

db_pool = None


def init_db_pool():
    global db_pool
    try:
        db_pool = pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            host=settings.DATABASE_HOST,
            port=settings.DATABASE_PORT,
            database=settings.DATABASE_NAME,
            user=settings.DATABASE_USER,
            password=settings.DATABASE_PASSWORD,
        )
        print("Database pool initialized successfully")
    except Exception as e:
        print(f"Error initializing database pool: {e}")
        raise


def get_db_connection():
    if db_pool is None:
        init_db_pool()
    try:
        conn = db_pool.getconn()
        return conn
    except Exception as e:
        print(f"Error getting connection: {e}")
        raise


def release_db_connection(conn):
    if db_pool and conn:
        db_pool.putconn(conn)


def close_db_pool():
    if db_pool:
        db_pool.closeall()
        print("Database pool closed")


def get_db():
    conn = get_db_connection()
    try:
        yield conn
    finally:
        release_db_connection(conn)
