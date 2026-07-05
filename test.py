import sqlite3

conn = sqlite3.connect("shipment_database.db")
cursor = conn.cursor()

tables = ["product", "shipment"]

for table in tables:
    print(f"\n===== {table.upper()} TABLE =====")
    cursor.execute(f"PRAGMA table_info({table});")
    for column in cursor.fetchall():
        print(column)

conn.close()