#!/usr/bin/env python3
"""
Task 4: Cache Database Queries with a Decorator
"""

import sqlite3
import functools

# Global dictionary to store cached results
query_cache = {}


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
            conn.close()  # always close connection
        return result
    return wrapper


def cache_query(func):
    """
    Decorator that caches query results based on the SQL query string.
    If the query has been executed before, return the cached result.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Extract the query string from either args or kwargs
        query = kwargs.get("query") if "query" in kwargs else args[0]

        if query in query_cache:
            print(f"[CACHE HIT] Returning cached result for query: {query}")
            return query_cache[query]

        # Execute the actual function and cache its result
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        print(f"[CACHE MISS] Caching result for query: {query}")
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """
    Fetch users with caching.
    Only executes query if not cached yet.
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


if __name__ == "__main__":
    # First call: goes to DB and caches result
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(users)

    # Second call: returns cached result
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(users_again)
