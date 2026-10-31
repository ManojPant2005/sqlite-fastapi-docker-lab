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

@app.get("/users")
def get_users():
    conn = get_conn()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return [dict(u) for u in users]

@app.get("/users-paged")
def get_users_paged(limit: int = 10, offset: int = 0):
    conn = get_conn()
    users = conn.execute("SELECT * FROM users LIMIT ? OFFSET ?", (limit, offset)).fetchall()
    conn.close()
    return [dict(u) for u in users]


@app.get("/search")
def search(q: str):
    conn = get_conn()
    rows = conn.execute("SELECT * FROM users WHERE name LIKE ?", (f"%{q}%",)).fetchall()
    conn.close()
    return [dict(r) for r in rows]