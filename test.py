import sqlite3

# 1. Use a FILE so you can see it. :memory: will disappear every time.
conn = sqlite3.connect("mydata.db") 
cur = conn.cursor()

# 2. Put all SQL inside one string and use executescript
sql_script = """
DROP TABLE IF EXISTS users;
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
"""

cur.executescript(sql_script)
conn.commit() # IMPORTANT - without this, tables won't save

# 3. Check if it worked
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cur.fetchall()) # Should print [('users',), ('orders',)]

conn.close()