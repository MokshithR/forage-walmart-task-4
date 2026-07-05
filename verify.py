import sqlite3

conn = sqlite3.connect("shipment_database.db")
cursor = conn.cursor()

print("Products:", cursor.execute("SELECT COUNT(*) FROM product").fetchone()[0])
print("Shipments:", cursor.execute("SELECT COUNT(*) FROM shipment").fetchone()[0])

conn.close()