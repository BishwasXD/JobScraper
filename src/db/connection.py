import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

DATABASE = os.getenv('DATABASE')
USER = os.getenv('DB_USER')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
PASSWORD = os.getenv('PASSWORD')


def connect_db():
    try:
        connection = psycopg2.connect(
            database=DATABASE,
            user=USER,
            host=HOST,
            password=PASSWORD,
            port=PORT
        )

        print('CONNECTION WITH DATABASE ESTABLISHED')
        return connection
    except Exception as e:
        print('EXCEPTION OCCURED WHILE CONNECTING TO DB, EXCEPTION: ', e)
        return False
