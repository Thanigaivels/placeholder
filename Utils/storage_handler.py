import sys
import traceback

import psycopg2
from psycopg2 import *

db_params = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': 'root',
    'port': '5432'
}

connection, cursor = None, None

def get_connection():
    try:
        connection = psycopg2.connect(**db_params)
        return connection
    except Exception as error:
        print("Error initiating DB connection:", error)

def execute_query(query, row_count=100):
    global connection, cursor
    try:
        connection = get_connection()
        cursor = connection.cursor()
        print("Connection established with DB.")
        cursor.execute(query)
        result = cursor.fetchmany(row_count)
        return result
    except Exception as e:
        print("Error: ")
        print(e)
    finally:
        cursor.close()
        connection.close()
        print("Connection closed.")


def insert_scraped_data(records):
    global connection, cursor
    connection = get_connection()
    try:
        cursor = connection.cursor()
        args_str = ','.join(cursor.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", i).decode('utf-8') for i in records)
        cursor.execute("""INSERT INTO "public"."postData" ("source", "sourceID", "link", "linkAttributes", "caption",
         "title", "uploadType", "scrappedTime", "createdTime", "ownerInfo", "jobStatus") VALUES """ + args_str +
                       """ON CONFLICT ("sourceID") DO NOTHING""")
        connection.commit()
        print("Write to DB is successful")
    except psycopg2.Error as e:
        print(f"""{traceback.format_exc()}\n::\n{e}""")
    except Exception as e:
        print("Error when writing to DB(Not a psycopg2 error)\n ", e)
    finally:
        cursor.close()
        connection.close()
