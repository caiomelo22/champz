# database/db.py
import os
import mysql.connector
from contextlib import closing
from typing import List, Dict, Any, Optional

class Database:
    def __init__(self, host: str, user: str, password: str, database: str):
        self.host = os.getenv("DB_HOST")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_DATABASE")

    def execute_query(self, query: str, args: Optional[tuple] = None):
        with closing(mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
        )) as conn:
            with closing(conn.cursor()) as cursor:
                if args is None:
                    cursor.execute(query)
                else:
                    cursor.execute(query, args)
                conn.commit()

    def fetch_one(self, query: str, args: Optional[tuple] = None) -> Dict[str, Any]:
        with closing(mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
        )) as conn:
            with closing(conn.cursor()) as cursor:
                if args is None:
                    cursor.execute(query)
                else:
                    cursor.execute(query, args)
                return dict(zip(cursor.column_names, cursor.fetchone()))

    def fetch_all(self, query: str, args: Optional[tuple] = None) -> List[Dict[str, Any]]:
        with closing(mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
        )) as conn:
            with closing(conn.cursor()) as cursor:
                if args is None:
                    cursor.execute(query)
                else:
                    cursor.execute(query, args)
                return [dict(zip(cursor.column_names, row)) for row in cursor.fetchall()]
