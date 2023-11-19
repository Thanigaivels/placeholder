import psycopg2
from psycopg2 import *

db_params = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': 'root',
    'port': '5433'
}

def get_connection():
    try:
        connection = psycopg2.connect(**db_params)
        return connection
    except (Exception) as error:
        print("Error initiating DB connection:", error)

def execute_query(query, row_count=100):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        print("Connection established with DB.")
        cursor.execute(query)
        result = cursor.fetchmany(row_count)
        return result
    except (Exception) as e:
        print("Error: ")
        print(e)
    finally:
        print("Connection closed.")
        cursor.close()
        connection.close()
