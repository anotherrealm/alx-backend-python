#!/usr/bin/python3
import mysql.connector
import csv
import uuid


def connect_db():

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",       
            password="root"    
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None


def create_database(connection):
    """Create ALX_prodev DB if not exists."""
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    cursor.close()


def connect_to_prodev():
    """Connect directly to ALX_prodev DB."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None


def create_table(connection):
    """Create user_data table if not exists."""
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX(user_id)
        )
    """)
    connection.commit()
    print("Table user_data created successfully")
    cursor.close()


def insert_data(connection, csv_file):
    """Insert rows into user_data from CSV if not already present."""
    cursor = connection.cursor()

    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user_id = str(uuid.uuid4())
            name = row['name']
            email = row['email']
            age = int(row['age'])

            cursor.execute("""
                SELECT COUNT(*) FROM user_data WHERE email = %s
            """, (email,))
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, name, email, age))

    connection.commit()
    cursor.close()
