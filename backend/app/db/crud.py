# db/crud.py

from typing import List, Optional

from database.db import Database

database = Database()  # Initialize the custom database instance


# CRUD operations for items
def create_item(item_data: dict) -> int:
    query = "INSERT INTO items (name, description) VALUES (?, ?)"
    database.execute_query(query, (item_data["name"], item_data["description"]))
    return database.fetch_one("SELECT last_insert_rowid()")["last_insert_rowid()"]


def get_item(item_id: int) -> Optional[dict]:
    query = "SELECT * FROM items WHERE id = ?"
    return database.fetch_one(query, (item_id,))


def update_item(item_id: int, item_data: dict) -> bool:
    query = "UPDATE items SET name = ?, description = ? WHERE id = ?"
    database.execute_query(
        query, (item_data["name"], item_data["description"], item_id)
    )
    return database.fetch_one("SELECT changes()")["changes()"] > 0


def delete_item(item_id: int) -> bool:
    query = "DELETE FROM items WHERE id = ?"
    database.execute_query(query, (item_id,))
    return database.fetch_one("SELECT changes()")["changes()"] > 0


def get_all_items() -> List[dict]:
    query = "SELECT * FROM items"
    return database.fetch_all(query)
