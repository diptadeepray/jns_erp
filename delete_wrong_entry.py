import sqlite3

conn = sqlite3.connect("database.db")   # use your actual db name
cursor = conn.cursor()

try:
    cursor.execute("""DELETE FROM inbound_payments WHERE category = ?""", ("supplier_category",))

# CODE TO CHECK BEFOR DELETION-OPTIONAL

#     cursor.execute("""
#     SELECT * FROM inbound_payments
#     WHERE category = ?
# """, ("supplier_category",))
    
#     rows = cursor.fetchall()

#     for row in rows:
#         print(row)


    
    conn.commit()
    print("Row(s) deleted successfully")

except sqlite3.Error as e:
    print("Error while deleting row:", e)

finally:
    conn.close()
