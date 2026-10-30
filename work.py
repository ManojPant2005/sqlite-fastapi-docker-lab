import sqlite3
conn = sqlite3.connect("mydata.db")
cur = conn.cursor()
cur.execute("PRAGMA foreign_keys = ON;")

# --- CORRECT WAY: Delete child (orders) first, then parent (users) ---
cur.execute("DELETE FROM orders WHERE user_id = (SELECT id FROM users WHERE name = ?)", ('Amit',))
cur.execute("DELETE FROM users WHERE name = ?", ('Amit',))
conn.commit()

# --- Check ---
print("After delete:")
for row in cur.execute("SELECT * FROM users"): 
    print(row)

print("\nOrders left:")
for row in cur.execute("SELECT * FROM orders"): 
    print(row)

conn.close()