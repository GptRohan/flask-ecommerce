import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database = "ecommerce_db"

    )

    return connection

get_db_connection()