import sys
import traceback

import psycopg2
from psycopg2 import *

db_params = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': 'root',
    'port': '5433'
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
        return True
    except psycopg2.Error as e:
        print(f"""{traceback.format_exc()}\n::\n{e}""")
    except Exception as e:
        print("Error when writing to DB(Not a psycopg2 error)\n ", e)
    finally:
        cursor.close()
        connection.close()

def fetch_post_data():
    global connection, cursor
    connection = get_connection()
    try:
        cursor = connection.cursor()
        print("Connection established with DB.")
        query = "SELECT \"autoID\",\r\n\tSOURCE,\r\n\t\"sourceID\",\r\n\tLINK,\r\n\t\"linkAttributes\",\r\n\tCAPTION,\r\n\tTITLE,\r\n\t\"uploadType\",\r\n\t\"scrappedTime\",\r\n\t\"createdTime\",\r\n\t\"ownerInfo\",\r\n\t\"jobStatus\"\r\nFROM PUBLIC.\"postData\" where \"jobStatus\" is null;"
        cursor.execute(query)
        result = cursor.fetchone()
        return result
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connection.close()

def update_job_status(id, status='Completed'):
    global connection, cursor
    connection = get_connection()
    try:
        cursor = connection.cursor()
        print("Gonna update job status.")
        query = "UPDATE PUBLIC.\"postData\"\r\nSET \"jobStatus\" = \'{0}\'\r\nWHERE \"autoID\" = {1} ;".format(status, id)
        cursor.execute(query)
        connection.commit()
        return True
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connection.close()