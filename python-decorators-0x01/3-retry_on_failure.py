#!/usr/bin/env python3
"""
Task 3: Retry Database Queries with a Decorator
"""

import time
import sqlite3
import functools


def with_db_connection(func):
    """
    Decorator that automatically opens and closes
    a SQLite database connection.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")  # open connection
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()  # always close
        return result
    return wrapper


def retry_on_failure(retries=3, delay=2):
    """
    Decorator factory to retry a function if it fails.
    :param retries: number of retry attempts
    :param delay: delay (in seconds) between retries
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"Attempt {attempt} failed: {e}")
                    if attempt < retries:
                        print(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
            # After all retries fail
            print("All retry attempts failed.")
            raise last_exception
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """
    Fetch all users from the users table with retry logic.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


if __name__ == "__main__":
    try:
        users = fetch_users_with_retry()
        print(users)
    except Exception as e:
        print(f"Final failure: {e}")
