# Learn SQLite - Hands-On with FastAPI & Docker

> My journey from knowing SQL to running a live SQLite API inside Docker - all hands-on in VS Code.

## Repo Name Suggestion

**Recommended Name:** `sqlite-fastapi-docker-lab`

**Other options:** `learn-sqlite-hands-on` / `sqlite-lite-starter`

**Description for GitHub:**
> A beginner-friendly, hands-on lab to learn SQLite quickly if you already know SQL. Covers SQLite basics, common errors (FOREIGN KEY, UNIQUE), Python sqlite3, FastAPI integration, and Dockerization with volume persistence. Built step-by-step in VS Code.

---

## What is SQLite?

- **File, not server:** `mydata.db` is the whole database. No username/password, just a file you can copy/backup/email.
- **Only 5 types:** TEXT, INTEGER, REAL, BLOB, NULL (Type Affinity - loose typing)
- **No heavy ALTER:** Can't easily DROP column, need to recreate table
- **INTEGER PRIMARY KEY = auto-increment:** Don't use AUTOINCREMENT keyword unless needed
- **CLI helpers (only in sqlite3 terminal, not Python):** `.tables`, `.schema table_name`, `.mode column`, `.headers on`

## Project Structure


Learn/SqlLite/
├── setup.py            -> Create fresh DB with sample data (run once)
├── work.py             -> Daily practice for UPDATE/DELETE/JOIN + error handling
├── api.py              -> FastAPI that uses mydata.db
├── requirements.txt    -> Python deps (fastapi, uvicorn)
├── Dockerfile          -> Recipe to build API image
├── docker-compose.yml  -> Easy run config with volume for SQLite
├── .dockerignore       -> Ignore __pycache__, venv etc in Docker build
├── mydata.db           -> SQLite file (persists data)
└── README.md           -> This file


## Step 1: Setup Database

setup.py creates 2 tables and sample data:

sql
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


Run:
bash
python setup.py
# Output: Setup done - 3 users, 4 orders created


Checked in VS Code with Database Client extension - TABLES 2, 0 rows before insert, 3 rows after.

## Step 2: The Loop I Use

python
import sqlite3
conn = sqlite3.connect("mydata.db")
cur = conn.cursor()
cur.execute("PRAGMA foreign_keys = ON;")
conn.commit()
conn.close()


## Step 3: Errors I Faced & Fixed

### 1. FOREIGN KEY constraint failed
DELETE FROM users WHERE name='Amit' failed because Amit had orders.

Fix - delete child first:
python
cur.execute("DELETE FROM orders WHERE user_id = (SELECT id FROM users WHERE name = ?)", ('Amit',))
cur.execute("DELETE FROM users WHERE name = ?", ('Amit',))
conn.commit()


### 2. UNIQUE constraint failed
Ran work.py twice and tried to insert Rahul again with same email.

Fix - use ON CONFLICT:
python
cur.execute("INSERT INTO users (name, email) VALUES (?, ?) ON CONFLICT(email) DO NOTHING", ('Rahul', 'rahul@example.com'))


### 3. Forgot commit()
Without conn.commit(), data won't save.

## Step 4: Practice Queries

python
# JOIN + GROUP BY
cur.execute("SELECT u.name, SUM(o.amount) FROM users u LEFT JOIN orders o ON u.id=o.user_id GROUP BY u.id")
# UPDATE
cur.execute("UPDATE users SET email=? WHERE name=?", ('sara.new@test.com', 'Sara'))


## Step 5: Use SQLite in API (FastAPI)

Install: pip install fastapi uvicorn

api.py uses get_conn() with PRAGMA foreign_keys and row_factory = Row

Run without Docker:
bash
python -m uvicorn api:app --reload


Test:
- http://127.0.0.1:8000/users
- http://127.0.0.1:8000/docs -> Swagger UI

## Step 6: Dockerize It

### Why Docker for this project?
- No need to install Python/pip on other laptops
- mydata.db file stays with app, easy to share
- Same environment everywhere

### Files

**requirements.txt**

fastapi==0.162.0
uvicorn==0.54.0


**Dockerfile**
dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


**docker-compose.yml**
yaml
services:
  api:
    build: .
    container_name: sqlite_api
    ports:
      - "8000:8000"
    volumes:
      - ./mydata.db:/app/mydata.db
      - ./api.py:/app/api.py


### How to Run with Docker

bash
docker --version
docker-compose up --build
# Open http://localhost:8000/users and /docs
docker-compose down


### Docker Errors I Faced & Fixed

1. failed to connect to docker API at npipe:////./pipe/dockerDesktopLinuxEngine
-> Docker Desktop app was not started. Fix: Open Docker Desktop and wait till Engine running (green).

2. "/requirements.txt": not found
-> My file was Requirements.txt (capital R) but Dockerfile had requirements.txt (small r). Linux inside Docker is case-sensitive.
Fix: ren Requirements.txt requirements.txt

### Docker Concepts Cleared

| Concept | What it is |
| Image | Snapshot with Python + FastAPI + my code |
| Container | Running instance of that image |
| Volume | ./mydata.db:/app/mydata.db - syncs file so data doesn't disappear |
| Dockerfile | Recipe HOW to build image |
| docker-compose.yml | Config HOW to run container |

## What I Learned

- Always PRAGMA foreign_keys = ON and conn.commit()
- Use ? placeholder, not f-strings
- For SQLite in Docker, volume is must or data is lost
- Case sensitivity matters in Docker
- Docker Desktop must be running before docker build

## API Endpoints

| Method | Endpoint | Description |
| GET | /users | All users |
| GET | /orders | All orders |
| GET | /report/paid | JOIN report |
| GET | /search?q=name | Search |
| POST | /users?name=&email= | Add user |

## Next

- [ ] Add PUT/DELETE APIs
- [ ] Try Chinook sample DB
- [ ] Push image to Docker Hub
- [ ] Add frontend as second service

Built hands-on in VS Code on Windows.
