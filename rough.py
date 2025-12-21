import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM table_name WHERE venture_id = known_venture_id")
row = cursor.fetchone()   # returns ONE row or None

if row:
    print(row)            # tuple of column values
    id = row[0]
    name = row[1]
    country = row[2]
    amount = row[3]
    print(f"ID: {id}, Name: {name}, Country: {country}, Amount: {amount}")
else:
    print("No matching record found.")
