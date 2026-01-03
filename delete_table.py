import sqlite3

# Connect to the database (it will create the file if it doesn't exist)
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# --- 1. Delete an existing table ---
table_to_delete = "all_suppliers"
cursor.execute(f"DROP TABLE IF EXISTS {table_to_delete}")
print(f"Table '{table_to_delete}' deleted (if it existed).")

# --- 1. Delete an existing table ---
table_to_delete = "all_contractors"
cursor.execute(f"DROP TABLE IF EXISTS {table_to_delete}")
print(f"Table '{table_to_delete}' deleted (if it existed).")

# # --- 2. Create a new table ---
# new_table_name = "new_table"
# cursor.execute(f"""
# CREATE TABLE {new_table_name} (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL,
#     age INTEGER,
#     email TEXT UNIQUE
# )
# """)
# print(f"Table '{new_table_name}' created successfully.")

# Commit changes and close connection
conn.commit()
conn.close()
