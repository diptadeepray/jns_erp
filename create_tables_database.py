import sqlite3, os







def delete_table():


        # Connect to the database
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        # Delete the table
        c.execute("DROP TABLE IF EXISTS all_contracters")

        conn.commit()
        conn.close()

# delete_table()










def creating_demo_table():
        
        conn = sqlite3.connect("database.db")
        # If database.db already exists → SQLite opens the existing file.
        # If database.db does NOT exist → SQLite creates a new empty database file, then opens it.       

        c = conn.cursor()

        c.execute(""" CREATE TABLE IF NOT EXISTS demo 
                  ( id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    a_number INTEGER, 
                    first_text TEXT, 
                    second_text TEXT ) """)
        
# creating_demo_table()









def creating_onboarding_tables():
        
        conn = sqlite3.connect("database.db")
        # If database.db already exists → SQLite opens the existing file.
        # If database.db does NOT exist → SQLite creates a new empty database file, then opens it.       

        c = conn.cursor()

        c.execute(""" CREATE TABLE IF NOT EXISTS all_clients 
                  ( id INTEGER PRIMARY KEY AUTOINCREMENT, client_name TEXT, 
                    site_name TEXT, contract_type TEXT, entry_date TEXT, 
                    contract_amount REAL, venture_id TEXT ) """)
        c.execute(""" CREATE TABLE IF NOT EXISTS all_suppliers 
                  ( id INTEGER PRIMARY KEY AUTOINCREMENT, supplier_name TEXT, 
                    supplier_id TEXT ) """)
        c.execute(""" CREATE TABLE IF NOT EXISTS all_contractors
                  ( id INTEGER PRIMARY KEY AUTOINCREMENT, contractor_name TEXT, 
                    contractor_id TEXT ) """)
        

        ''' In SQLite, whenever you create a table that contains:
            INTEGER PRIMARY KEY AUTOINCREMENT
            SQLite automatically creates a table named sqlite_sequence
            It stores the last used AUTOINCREMENT value for each table.'''


        
        conn.commit()
        conn.close()
# creating_onboarding_tables()




def creating_inbound_payments_table():
        
        conn = sqlite3.connect("database.db")
        # If database.db already exists → SQLite opens the existing file.
        # If database.db does NOT exist → SQLite creates a new empty database file, then opens it.       

        c = conn.cursor()

        # Create table
        c.execute("""
    CREATE TABLE IF NOT EXISTS inbound_payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT,
        category TEXT,
        client_name TEXT,
        site_name TEXT,
        venture_id TEXT,
        supplier_name TEXT,
        supplier_id TEXT,
        cash_amount REAL,
        cheque_amount REAL,
        total_amount REAL,
        amount_number TEXT,
        cash_name TEXT,
        cheque_name TEXT,
        cheque_date TEXT,
        cheque_bank TEXT,
        cheque_number TEXT,
        entry_date TEXT,
        ar_id TEXT)""")

        
        conn.commit()
        conn.close()

# creating_inbound_payments_table()








def creating_outbound_payments_table():
        
        conn = sqlite3.connect("database.db")
        # If database.db already exists → SQLite opens the existing file.
        # If database.db does NOT exist → SQLite creates a new empty database file, then opens it.       

        c = conn.cursor()

        # Create table
        c.execute("""
    CREATE TABLE IF NOT EXISTS outbound_payments (
id INTEGER PRIMARY KEY AUTOINCREMENT,
destination TEXT,
client_name TEXT,
site_name TEXT,
venture_id TEXT,
supplier_name TEXT,
supplier_id TEXT,
material_description TEXT,
contractor_name TEXT,
contractor_id TEXT,
labour_description TEXT,
office_reason TEXT,
cash_amount REAL,
cheque_amount REAL,
total_amount REAL,
amount_number TEXT,
cash_name TEXT,
cheque_name TEXT,
cheque_date TEXT,
cheque_bank TEXT,
cheque_number TEXT,
entry_date TEXT,
actual_ap_id TEXT
)""")

        
        conn.commit()
        conn.close()

# creating_outbound_payments_table()







def creating_expected_ap_table():
        
        conn = sqlite3.connect("database.db")
        # If database.db already exists → SQLite opens the existing file.
        # If database.db does NOT exist → SQLite creates a new empty database file, then opens it.       

        c = conn.cursor()

        # Create table
        c.execute("""
    CREATE TABLE IF NOT EXISTS expected_ap (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT,
    category TEXT,
    client_name TEXT,
    site_name TEXT,
    venture_id TEXT,
    supplier_name TEXT,
    supplier_id TEXT,
    total_amount_received_from_that_party REAL,
    expected_office_expense REAL,
    expected_material_expense REAL,
    expected_labour_expense REAL,
    expected_profit REAL
)
""")

        
        conn.commit()
        conn.close()

#creating_expected_ap_table()




















def know_database_details():
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = c.fetchall()

        print("Tables:")
        for t in tables:
                print(t[0])

        conn.close()
# know_database_details()