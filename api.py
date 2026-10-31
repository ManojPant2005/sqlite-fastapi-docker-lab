from fastapi import FastAPI
import sqlite3
app = FastAPI()
def get_conn():
    conn = sqlite3.connect("mydata.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

@app.get("/")
def home():
    return {"message": "SQLite API is running"}