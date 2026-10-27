import mysql.connector

# Notice we did NOT include the "database" key here yet.
# We are connecting directly to the server to create the database first.
DB_SERVER_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "baloCH123&"
}

def setup_everything():
    print("Connecting to MySQL Server...")
    conn = mysql.connector.connect(**DB_SERVER_CONFIG)
    cursor = conn.cursor()

    # 1. Create the Database
    print("Creating database 'fastapiappdb'...")
    cursor.execute("CREATE DATABASE IF NOT EXISTS fastapiappdb;")
    
    # 2. Tell MySQL to use this new database
    cursor.execute("USE fastapiappdb;")

    # 3. Create the 'items' table
    print("Creating 'items' table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            price DECIMAL(10, 2) NOT NULL
        )
    """)

    # 4. Clear out any old data (to prevent duplicates if run multiple times)
    cursor.execute("TRUNCATE TABLE items;")

    # 5. Insert sample data
    print("Inserting dummy data...")
    insert_query = "INSERT INTO items (name, description, price) VALUES (%s, %s, %s)"
    sample_data = [
        ("Gaming Mouse", "Wireless RGB gaming mouse", 49.99),
        ("Mechanical Keyboard", "Blue switch mechanical keyboard", 89.50),
        ("27-inch Monitor", "144Hz 1080p gaming monitor", 210.00)
    ]
    
    cursor.executemany(insert_query, sample_data)
    conn.commit()

    print("Success! Database and tables are created and populated.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    setup_everything()