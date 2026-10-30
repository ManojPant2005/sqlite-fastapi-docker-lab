import sqlite3

conn = sqlite3.connect("mydata.db")
cur = conn.cursor()

# Enable foreign key check (SQLite keeps it OFF by default!)
cur.execute("PRAGMA foreign_keys = ON;")

# --- Insert sample data ---
cur.execute("DELETE FROM orders;")
cur.execute("DELETE FROM users;")

cur.executemany("INSERT INTO users (name, email) VALUES (?, ?)", [
    ('Manoj', 'manoj@test.com'),
    ('Sara', 'sara@test.com'),
    ('Amit', 'amit@test.com')
])


# Delete row from users table where name is 'Amit'
cur.execute("DELETE FROM users WHERE name = ?", ('Amit',))

cur.executemany("INSERT INTO orders (user_id, amount, status) VALUES (?, ?, ?)", [
    (1, 250.5, 'paid'),
    (1, 99.0, 'pending'),
    (2, 1200.0, 'paid'),
    (3, 50.0, 'failed')
])

conn.commit()

# --- YOUR 5 WORK QUERIES - practice these ---
print("1. All users:")
for row in cur.execute("SELECT * FROM users"): print(row)

print("\n2. Total spent per user (JOIN + GROUP BY):")
for row in cur.execute("""
  SELECT u.name, SUM(o.amount) as total 
  FROM users u LEFT JOIN orders o ON u.id = o.user_id 
  GROUP BY u.id
"""): print(row)

print("\n3. Only paid orders:")
for row in cur.execute("SELECT * FROM orders WHERE status='paid'"): print(row)

print("\n4. Search:")
for row in cur.execute("SELECT * FROM users WHERE name LIKE '%a%'"): print(row)

conn.close()