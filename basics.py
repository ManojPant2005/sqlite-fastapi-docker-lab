import sqlite3
conn = sqlite3.connect(":memory:") # in-memory DB, disappears when you close
cur = conn.cursor()

