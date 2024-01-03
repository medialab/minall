# minall/utils/database.py

"""Utilities to manage SQLite database connection.

The module contains the following function and class:

- `connect_to_database(database)` - If provided with path, connects to embedded SQLite database; otherwise, connects to in-memory SQLite database.
- `SQLiteWrapper(connection)` - Stores connection and cursor, executes queries.
"""

import sqlite3
from pathlib import Path
from sqlite3 import Connection
from typing import List, Tuple


class SQLiteWrapper:
    """Class to store SQLite database connection and execute SQL queries.

    Examples:
        >>> wrapper = SQLiteWrapper(connection=connect_to_database())
        >>> _ = wrapper(query="create table test(name text)")
        >>> wrapper.select("select * from test")
        []

    """

    def __init__(self, connection: Connection) -> None:
        """Store database connection and create cursor.

        Examples:
            >>> wrapper = SQLiteWrapper(connection=connect_to_database())
            >>> type(wrapper.cursor)
            <class 'sqlite3.Cursor'>

        Args:
            connection (Connection): Connection to SQLite database.
        """
        self.connection = connection
        self.cursor = self.connection.cursor()

    def __call__(self, query: str, values: List[Tuple] | None = None) -> None:
        """Execute and commit SQL query.

        Examples:
            >>> wrapper = SQLiteWrapper(connection=connect_to_database())
            >>> _ = wrapper(query="create table test(name text)")
            >>> wrapper.select("select * from test")
            []

        Args:
            query (str): Query string, can contain SQL place holders for values (?).
            values (list[tuple] | None, optional): Values to be included in query. Defaults to None.

        Raises:
            Exception: `sqlite3` Exception caused either by falling to execute query with cursor or by failing to commit changes to connected database.
        """
        try:
            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            print("\n", query, "\n")
            print(values)
            raise e

    def select(self, query: str) -> List:
        """Return selection from SQLite database.

        Examples:
            >>> wrapper = SQLiteWrapper(connection=connect_to_database())
            >>> _ = wrapper(query="create table test(name text)")
            >>> wrapper.select("select * from test")
            []

        Args:
            query (str): SQL select query.

        Raises:
            Exception: `sqlite3` Exception caused either by falling to execute query with cursor or by failing to commit changes to connected database.

        Returns:
            List: Array of results from SQL query.
        """
        try:
            response = self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            print("\n", query, "\n")
            raise e
        else:
            return response.fetchall()


def connect_to_database(database: str | None = None) -> Connection:
    """Connect to SQLite database.

    Examples:
        >>> conn = connect_to_database()
        >>> type(conn)
        <class 'sqlite3.Connection'>
        >>> _ = conn.cursor().execute("create table test(name text)")
        >>> conn.cursor().execute("select * from test").fetchall()
        []

    Args:
        database (str | None, optional): If given, path to embedded SQLite database. Defaults to None.

    Returns:
        Connection: _description_
    """

    if database:
        [p.mkdir(exist_ok=True) for p in Path(database).parents]
        connection = sqlite3.connect(database)
    else:
        connection = sqlite3.connect(":memory:")
    return connection
