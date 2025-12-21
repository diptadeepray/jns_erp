import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

c.execute("""
    ALTER TABLE expected_ap
    RENAME COLUMN total_amount_paid_to_that_party TO total_amount;
""")

conn.commit()
conn.close()

print("Column renamed successfully!")
