import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

# c.execute("""
#     ALTER TABLE expected_ap
#     RENAME COLUMN total_amount_paid_to_that_party TO total_amount;
# """)

# print("Column renamed successfully!")



c.execute("""
    ALTER TABLE expected_ap
ADD COLUMN inbound_payments_column_id INTEGER;
""")


conn.commit()
conn.close()