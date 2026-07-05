import sqlite3
import pandas as pd

# ----------------------------
# Connect to SQLite Database
# ----------------------------
conn = sqlite3.connect("shipment_database.db")
cursor = conn.cursor()

# ----------------------------
# Load CSV Files
# ----------------------------
df0 = pd.read_csv("data/shipping_data_0.csv")
df1 = pd.read_csv("data/shipping_data_1.csv")
df2 = pd.read_csv("data/shipping_data_2.csv")

# ----------------------------
# Helper Function
# ----------------------------
def get_product_id(product_name):
    """
    Returns the product ID.
    If the product doesn't exist, insert it.
    """
    cursor.execute(
        "SELECT id FROM product WHERE name = ?",
        (product_name,)
    )
    result = cursor.fetchone()

    if result:
        return result[0]

    cursor.execute(
        "INSERT INTO product(name) VALUES (?)",
        (product_name,)
    )

    return cursor.lastrowid


# ==================================================
# PART 1 : shipping_data_0.csv
# ==================================================

for _, row in df0.iterrows():

    product_id = get_product_id(row["product"])

    cursor.execute("""
        INSERT INTO shipment
        (product_id, quantity, origin, destination)
        VALUES (?, ?, ?, ?)
    """, (
        product_id,
        int(row["product_quantity"]),
        row["origin_warehouse"],
        row["destination_store"]
    ))

conn.commit()

# ==================================================
# PART 2 : shipping_data_1 + shipping_data_2
# ==================================================

# Count quantity of each product inside each shipment
grouped = (
    df1
    .groupby(["shipment_identifier", "product"])
    .size()
    .reset_index(name="quantity")
)

# Merge with origin & destination
merged = grouped.merge(
    df2,
    on="shipment_identifier"
)

# Insert into database
for _, row in merged.iterrows():

    product_id = get_product_id(row["product"])

    cursor.execute("""
        INSERT INTO shipment
        (product_id, quantity, origin, destination)
        VALUES (?, ?, ?, ?)
    """, (
        product_id,
        int(row["quantity"]),
        row["origin_warehouse"],
        row["destination_store"]
    ))

conn.commit()

print("Database populated successfully!")

conn.close()