# Make your work.py safe to run multiple times (professional way

import sqlite3
conn = sqlite3.connect("mydata.db")
cur = conn.cursor()
cur.execute("PRAGMA foreign_keys = ON;")

# Delete Amit only if he exists (safe to run many times)
cur.execute("DELETE FROM orders WHERE user_id = (SELECT id FROM users WHERE name = ?)", ('Amit',))
cur.execute("DELETE FROM users WHERE name = ?", ('Amit',))
conn.commit()

print("After delete Amit:")
for row in cur.execute("SELECT * FROM users"): print(row)

print("\nOrders left:")
for row in cur.execute("SELECT * FROM orders"): print(row)

# UPDATE
cur.execute("UPDATE users SET email = ? WHERE name = ?", ('sara.new@test.com', 'Sara'))
conn.commit()

# INSERT Rahul - but don't crash if he already exists
cur.execute("""
    INSERT INTO users (name, email) VALUES (?, ?)
    ON CONFLICT(email) DO NOTHING
""", ('Rahul', 'rahul@example.com'))
conn.commit()

print("\nPaid orders JOIN:")
for row in cur.execute("SELECT u.name, o.amount, o.status FROM users u JOIN orders o ON u.id = o.user_id WHERE o.status = 'paid'"):
    print(row)
    
conn.close()
print("\nDone - you can run this file again and again, no error!")