import sqlite3

get_inventory_declaration = {
    "name": "get_inventory",
    "description": "Retrieves the inventory list",
}


def setup_database():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect("inventory.db")

    # Create a cursor object using the cursor() method
    cursor = conn.cursor()

    # Create table as per requirement
    sql = """CREATE TABLE IF NOT EXISTS inventory (
       part_id INTEGER PRIMARY KEY,
       part_name TEXT NOT NULL,
       quantity INTEGER NOT NULL,
       price INTEGER NOT NULL
    )"""

    cursor.execute(sql)
    print("Table created successfully")

    # Close the connection
    conn.close()


def insert_sample_data():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    # Sample data
    parts = [
        (1, "Tesla Windshield", 10, 1500),
        (2, "Porsche Tire", 50, 750),
        (3, "Porsche Brake Pad", 100, 300),
        (4, "Tesla Display", 5, 2000),
        (5, "Tesla Bumper", 5, 2000),
    ]

    # Inserting data
    cursor.executemany("INSERT INTO inventory VALUES (?, ?, ?, ?)", parts)

    # Committing the changes
    conn.commit()
    conn.close()
    print("Sample data inserted successfully")


def get_inventory():
    # Connect to the SQLite database
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    # SQL query to fetch all entries from the inventory table
    query = "SELECT * FROM inventory;"
    cursor.execute(query)

    # Fetch all rows
    rows = cursor.fetchall()

    # Format the results into a readable format
    inventory_list = [
        {"part_id": row[0], "part_name": row[1], "quantity": row[2], "price": row[3]}
        for row in rows
    ]

    # Close the connection
    conn.close()

    return inventory_list


def clear_database():
    # Connect to the SQLite database
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    # Clear the inventory table
    cursor.execute("DELETE FROM inventory;")
    conn.commit()

    # Close the connection
    conn.close()
    print("Database cleared successfully")


# Uncomment these lines to setup the database, insert sample data or clear the database
# setup_database()
# insert_sample_data()
# clear_database()
# print(get_inventory())
