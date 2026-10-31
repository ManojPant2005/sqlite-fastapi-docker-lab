# Learn SQLite - Hands-On with FastAPI & Docker

This repo is my quick hands-on learning for SQLite. I already know SQL, so I focused on practice, not theory.

## What is SQLite?

- File, not server: `mydata.db` is the whole DB. No user/password.
- Only 5 types: TEXT, INTEGER, REAL, BLOB, NULL
- No heavy ALTER - to change column, recreate table
- `INTEGER PRIMARY KEY` = auto-increment
- CLI helpers (only in sqlite3 terminal, not Python): `.tables`, `.schema table_name`, `.mode column`, `.headers on`

## Project Structure


Learn/SqlLite/
├── setup.py   -> Create fresh DB (run once)
├── work.py    -> Daily practice for UPDATE/DELETE/JOIN
├── api.py     -> FastAPI that uses mydata.db
├── mydata.db  -> SQLite file (you can copy/backup it)
└── README.md


## Step 1: Setup

setup.py creates 2 tables and sample data:

CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
  id INTEGER PRIMARY KEY,
  user_id INTEGER,
  amount REAL,
  status TEXT CHECK(status IN ('paid','pending','failed')),
  FOREIGN KEY(user_id) REFERENCES users(id)
);



python setup.py

It prints: Setup done - 3 users, 4 orders created

I checked in VS Code with Database Client extension - TABLES 2, 0 rows before insert, 3 rows after.

## Step 2: The Loop I Use

import sqlite3
conn = sqlite3.connect("mydata.db")
cur = conn.cursor()
cur.execute("PRAGMA foreign_keys = ON;")
# ... my queries ...
conn.commit()
conn.close()


## Step 3: Errors I Faced & Fixed

### 1. FOREIGN KEY constraint failed
When I did: DELETE FROM users WHERE name='Amit' -> failed because Amit had orders.

Fix - delete child first:
python
cur.execute("DELETE FROM orders WHERE user_id = (SELECT id FROM users WHERE name = ?)", ('Amit',))
cur.execute("DELETE FROM users WHERE name = ?", ('Amit',))
conn.commit()


### 2. UNIQUE constraint failed
I ran work.py twice and tried to insert Rahul again with same email.

Fix - use ON CONFLICT:

cur.execute("""
    INSERT INTO users (name, email) VALUES (?, ?)
    ON CONFLICT(email) DO NOTHING
""", ('Rahul', 'rahul@example.com'))


### 3. Forgot commit()
If you don't do conn.commit(), data won't save.

## Step 4: Practice Queries I Did

python
# All users
cur.execute("SELECT * FROM users")

# JOIN + GROUP BY
cur.execute("SELECT u.name, SUM(o.amount) FROM users u LEFT JOIN orders o ON u.id=o.user_id GROUP BY u.id")

# UPDATE
cur.execute("UPDATE users SET email=? WHERE name=?", ('sara.new@test.com', 'Sara'))

# JOIN for paid report
cur.execute("SELECT u.name, o.amount FROM users u JOIN orders o ON u.id=o.user_id WHERE o.status='paid'")


## Step 5: Use SQLite in API

Install:

pip install fastapi uvicorn


api.py:
python
from fastapi import FastAPI
import sqlite3

app = FastAPI()

def get_conn():
    conn = sqlite3.connect("mydata.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

@app.get("/users")
def get_users():
    conn = get_conn()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return [dict(u) for u in users]


Run:

python -m uvicorn api:app --reload


Test in browser:
- http://127.0.0.1:8000/users
- http://127.0.0.1:8000/docs -> Swagger UI to try APIs

## What I Learned

- Always do PRAGMA foreign_keys = ON
- Use ? placeholder, not f-strings
- mydata.db is just a file - easy to backup
- commit() is must

## Next

- [ ] Add POST/DELETE APIs
- [ ] Try Chinook sample DB
- [ ] Learn indexes

Created while learning hands-on in VS Code.
