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
            (item.name, item.quantity, item.price)
        )
        conn.commit()
        return {"message": "Item created successfully", "item": item}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Item with this name already exists")
    finally:
        conn.close()