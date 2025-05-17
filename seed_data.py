# seed_data.py
import sqlite3

products = [
    ("Glock 17 Gen5", "Reliable 9mm pistol", "glock", "$139.99", "none"),
    ("Glock 19 Gen3", "Compact and durable", "glock", "$114.99", "none"),
    ("Glock 22 Gen4", "Perfect for defense", "glock", "$129.99", "none"),
    ("Xanax 2mg", "Anti-anxiety medication", "pills", "$1.50", "none"),
    ("Oxycodone 30mg", "Prescription painkiller", "pills", "$2.50", "none"),
    ("Adderall 20mg", "Focus enhancer", "pills", "$2.00", "none"),
]

conn = sqlite3.connect("database.db")
c = conn.cursor()

for name, desc, category, price, image in products:
    c.execute("INSERT INTO products (name, description, category, price, image) VALUES (?, ?, ?, ?, ?)",
              (name, desc, category, price, image))

conn.commit()
conn.close()
print("Database seeded.")
