from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import get_db, create_table
import sqlite3

# Initialize the database table when the application starts
create_table()

app = FastAPI()


class Item(BaseModel):
    name: str
    quantity: int
    price: float


# Endpoint to get all items
@app.get("/items/")
def get_all_items():
    conn = get_db()
    cursor = conn.cursor()
    items = cursor.execute("SELECT * FROM items").fetchall()
    conn.close()
    return [dict(item) for item in items]


# Endpoint to create a new item
@app.post("/items/")
def create_item(item: Item):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO items (name, quantity, price) VALUES (?, ?, ?)",
            (item.name, item.quantity, item.price),
        )
        conn.commit()
        return {"message": "Item created successfully", "item": item}
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400, detail="Item with this name already exists"
        )
    finally:
        conn.close()


# Endpoint to get a single item by ID
@app.get("/items/{item_id}")
def get_item(item_id: int):
    conn = get_db()
    cursor = conn.cursor()
    item = cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
    conn.close()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return dict(item)


# Endpoint to delete an item by ID
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    conn = get_db()
    cursor = conn.cursor()
    item = cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
    if item is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Item not found")
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return {"message": "Item deleted successfully"}
