import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Add the new column
try:
    c.execute("ALTER TABLE orders ADD COLUMN payment_method TEXT")
    print("Column 'payment_method' added successfully.")
except sqlite3.OperationalError as e:
    print("Error:", e)

conn.commit()
conn.close()
