#!/usr/bin/env python3
"""
Task 0: Logging database queries using a decorator
"""

import sqlite3
import functools
from datetime import datetime


def log_queries(func):
    """
    Decorator that logs SQL queries before executing the function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the SQL query from function args/kwargs
        query = None

        # If the function receives query as positional or keyword arg
        if args:
            query = args[0]
        elif "query" in kwargs:
            query = kwargs["query"]

        # Log the query with timestamp
        if query:
            print(f"[{datetime.now()}] Executing SQL query: {query}")

        # Call the actual function
        return func(*args, **kwargs)

    return wrapper


@log_queries
def fetch_all_users(query):
    """
    Fetch all users from the database using the provided SQL query.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


if __name__ == "__main__":
    # Example usage
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)
