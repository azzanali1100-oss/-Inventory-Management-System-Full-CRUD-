from fastapi import APIRouter, Depends, HTTPException
import pyodbc
from app.database.connection import get_db_cursor

router = APIRouter(prefix="/db-test", tags=["Database Test"])

@router.get("/version")
def get_sql_version(cursor: pyodbc.Cursor = Depends(get_db_cursor)):
    try:
        cursor.execute("SELECT @@VERSION;")
        row = cursor.fetchone()
        return {"sql_server_version": row[0]}
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")