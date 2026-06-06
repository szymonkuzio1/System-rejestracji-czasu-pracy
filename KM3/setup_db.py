# pip install mysql-connector-python
import mysql.connector

db = "masi_projekt"

def create_db():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    cursor = mydb.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db}")
    print("utworzono baze danych")

