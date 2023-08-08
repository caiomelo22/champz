# database/db.py
import os
from contextlib import closing
from typing import Any, Dict, List, Optional, Tuple

import mysql.connector
from dotenv import load_dotenv
from fastapi import HTTPException

# Load environment variables from .env file
load_dotenv()


class Database:
    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_DATABASE")

    def execute_query(self, query: str, args: Optional[tuple] = None) -> bool:
        try:
            with closing(
                mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                )
            ) as conn:
                with closing(conn.cursor()) as cursor:
                    if args is None:
                        cursor.execute(query)
                    else:
                        cursor.execute(query, args)
                    conn.commit()
        except Exception as e:
            raise HTTPException(
                status_code=500, detail="Error when executing query: {e}"
            )

    def execute_select_query(
        self, query: str, args: Optional[Tuple] = None
    ) -> List[Tuple]:
        with closing(
            mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )
        ) as conn:
            with closing(conn.cursor(dictionary=True)) as cursor:
                if args is None:
                    cursor.execute(query)
                else:
                    cursor.execute(query, args)

                # Fetch the results
                results = cursor.fetchall()

                return results

    def fetch_one(self, query: str, args: Optional[tuple] = None) -> Dict[str, Any]:
        with closing(
            mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )
        ) as conn:
            with closing(conn.cursor()) as cursor:
                if args is None:
                    cursor.execute(query)
                else:
                    cursor.execute(query, args)
                return dict(zip(cursor.column_names, cursor.fetchone()))

    def fetch_all(
        self, query: str, args: Optional[tuple] = None
    ) -> List[Dict[str, Any]]:
        with closing(
            mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )
        ) as conn:
            with closing(conn.cursor()) as cursor:
                if args is None:
                    cursor.execute(query)
                else:
                    cursor.execute(query, args)
                return [
                    dict(zip(cursor.column_names, row)) for row in cursor.fetchall()
                ]
