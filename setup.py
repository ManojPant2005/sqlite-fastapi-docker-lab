import sqlite3
conn = sqlite3.connect("mydata.db")
cur = conn.cursor()
cur.execute("PRAGMA foreign_keys = ON;")

cur.execute("DELETE FROM orders;")
cur.execute("DELETE FROM users;")

cur.executemany("INSERT INTO users (name, email) VALUES (?, ?)", [
    ('Manoj', 'manoj@test.com'),
    ('Sara', 'sara@test.com'),
    ('Amit', 'amit@test.com')
])
cur.executemany("INSERT INTO orders (user_id, amount, status) VALUES (?, ?, ?)", [
    (1, 250.5, 'paid'),
    (1, 99.0, 'pending'),
    (2, 1200.0, 'paid'),
    (3, 50.0, 'failed')
])
conn.commit()
conn.close()
print("Setup done - 3 users, 4 orders created")