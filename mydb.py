import mysql.connector

db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'Sh@300601',
)

cursor = db.cursor()

cursor.execute("create database elderco")
