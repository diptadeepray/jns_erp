import sqlite3, os










def know_database_details():
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = c.fetchall()

        print("Tables:")
        for t in tables:
                print(t[0])

        conn.close()
#know_database_details()







import sqlite3

def know_database_details():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Get all table names
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()

    print("\nTables and Columns:")
    for t in tables:
        table_name = t[0]
        print(f"\n📌 Table: {table_name}")
        
        # Get column details
        c.execute(f"PRAGMA table_info({table_name});")
        columns = c.fetchall()

        for col in columns:
            col_id = col[0]
            col_name = col[1]
            col_type = col[2]
            print(f"   - {col_name} ({col_type})")

    conn.close()

# know_database_details()










def view_table_data(table_name):

        # Connect to your SQLite database (replace 'your_database.db' with your DB file)
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Execute a query to get all data from the table
        cursor.execute(f"SELECT * FROM {table_name}")

        # Fetch all rows
        rows = cursor.fetchall()

        # Print column names
        column_names = [description[0] for description in cursor.description]
        print(" | ".join(column_names))
        print("-" * 50)

        # Print all rows of the table
        for row in rows:
                print(row)

        # Close the connection
        conn.close()

# view_table_data('expected_ap')


conn = sqlite3.connect("database.db")
cursor = conn.cursor()

        # Execute a query to get all data from the table
cursor.execute(f"SELECT id, source, category, site_name, venture_id, expected_office_expense, expected_material_expense, expected_labour_expense, expected_profit FROM expected_ap")

rows = cursor.fetchall()

# Print column names
column_names = [description[0] for description in cursor.description]
print(" | ".join(column_names))
print("-" * 50)

        # Print all rows of the table
for row in rows:
        print(row)

        # Close the connection
conn.close()
