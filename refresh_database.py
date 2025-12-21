import sqlite3

def clear_all_tables(db="database.db"):
    conn = sqlite3.connect(db)
    c = conn.cursor()

    # Get all user tables except sqlite internal tables
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = c.fetchall()

    for (table,) in tables:
        c.execute(f"DELETE FROM {table};")   # delete all rows
        conn.commit()   # <-- VACUUM requires this
        c.execute(f"VACUUM;")                # optional: clean unused space

    conn.commit()
    conn.close()

clear_all_tables()
