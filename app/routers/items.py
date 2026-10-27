from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from mysql.connector import Error
from app.database.connection import get_db_cursor

router = APIRouter(prefix="/items", tags=["Items"])

# Schema for creating an item
class ItemCreate(BaseModel):
    name: str
    description: str
    price: float

# Schema for updating an item
class ItemUpdate(BaseModel):
    name: str
    description: str
    price: float

@router.get("/")
def get_all_items(cursor=Depends(get_db_cursor)):
    """READ: Fetch all items from the database."""
    try:
        cursor.execute("SELECT * FROM items;")
        items = cursor.fetchall()
        return {"status": "success", "data": items}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database query error: {str(e)}")

@router.get("/{item_id}")
def get_item_by_id(item_id: int, cursor=Depends(get_db_cursor)):
    """READ: Fetch a single item by ID."""
    try:
        cursor.execute("SELECT * FROM items WHERE id = %s;", (item_id,))
        item = cursor.fetchone()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"status": "success", "data": item}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database query error: {str(e)}")

@router.post("/")
def create_item(item: ItemCreate, cursor=Depends(get_db_cursor)):
    """CREATE: Insert a new item into the database."""
    try:
        query = "INSERT INTO items (name, description, price) VALUES (%s, %s, %s)"
        cursor.execute(query, (item.name, item.description, item.price))
        return {"status": "success", "message": f"Item '{item.name}' created successfully."}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database insert error: {str(e)}")

@router.put("/{item_id}")
def update_item(item_id: int, item: ItemUpdate, cursor=Depends(get_db_cursor)):
    """UPDATE: Modify an existing item by its ID."""
    try:
        # Check if item exists first
        cursor.execute("SELECT * FROM items WHERE id = %s;", (item_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Item not found")

        query = "UPDATE items SET name = %s, description = %s, price = %s WHERE id = %s"
        cursor.execute(query, (item.name, item.description, item.price, item_id))
        return {"status": "success", "message": f"Item ID {item_id} updated successfully."}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database update error: {str(e)}")

@router.delete("/{item_id}")
def delete_item(item_id: int, cursor=Depends(get_db_cursor)):
    """DELETE: Remove an item from the database by its ID."""
    try:
        # Check if item exists first
        cursor.execute("SELECT * FROM items WHERE id = %s;", (item_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Item not found")

        cursor.execute("DELETE FROM items WHERE id = %s;", (item_id,))
        return {"status": "success", "message": f"Item ID {item_id} deleted successfully."}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database delete error: {str(e)}")