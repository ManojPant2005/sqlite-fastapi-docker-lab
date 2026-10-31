#File, not server: sqlite3 mydata.db creates a whole DB file. No users, no passwords.
#Typing is loose: It has only 5 types: TEXT, INTEGER, REAL, BLOB, NULL. You can put text in an integer column, it won't stop you. That's called Type Affinity.
#No ALTER much: You can't DROP COLUMN in old versions, can't change column type easily. You recreate table.
#AUTOINCREMENT is different: Just use INTEGER PRIMARY KEY - it auto-increments. Don't use AUTOINCREMENT keyword unless you need to.
#Top commands: In sqlite3 CLI, these save time:
#.tables , .schema table_name , .mode column , .headers on

import sqlite3
conn = sqlite3.connect(":memory:") # in-memory DB, disappears when you close
cur = conn.cursor()


# Hands-On Practices with FAST API
# In terminal
# pip install fastapi uvicorn