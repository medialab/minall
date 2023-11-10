import sqlite3
from pathlib import Path
from sqlite3 import Connection


class SQLiteWrapper:
    def __init__(self, connection: Connection) -> None:
        self.connection = connection
        self.cursor = self.connection.cursor()

    def __call__(self, query: str, values: list[tuple] | None = None) -> None:
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


def connect_to_database(database: str | None) -> Connection:
    # Establish the SQLite database connection
    if database:
        [p.mkdir(exist_ok=True) for p in Path(database).parents]
        connection = sqlite3.connect(database)
    else:
        connection = sqlite3.connect(":memory:")
    return connection
