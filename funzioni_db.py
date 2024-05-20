import mysql.connector
from mysql.connector import Error


def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def create_database(connection, name):
    cursor = connection.cursor()
    try:
        query = f"CREATE DATABASE if not exists {name}"
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")


def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print(f"MySQL Database connection successful to {db_name}")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def execute_query_many(cursor, query):
    try:
        cursor.execute(query)
        #print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")
        raise ValueError(err)


def read_query(connection, query, /, *, dictionary=False):
    if dictionary:
        cursor = connection.cursor(dictionary=True)
    else:
        cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")


def execute_list_query(connection, sql, val):
    cursor = connection.cursor()
    try:
        cursor.executemany(sql, val)
        #connection.commit()
        #print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def execute_query_place(connection, query, place, commit=True, stampa=True):
    cursor = connection.cursor()
    try:
        cursor.execute(query, place)
        if commit:
            connection.commit()
        if stampa:
            print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")