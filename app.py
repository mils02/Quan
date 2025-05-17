from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import smtplib

app = Flask(__name__)

BITCOIN_WALLET = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
USDT_WALLET = "T7wZcHWq3FqZCBa4bBdXMfdz6xShmzKDbk"

# Helper functions
def get_products():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    products = c.fetchall()
    conn.close()
    return products

def get_product_by_id(product_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE id=?", (product_id,))
    product = c.fetchone()
    conn.close()
    return product

def add_order(product_id, product_name, price, payment_method, wallet):
    # Set a timeout value for SQLite to retry for 5 seconds before throwing the locked error
    with sqlite3.connect('database.db', check_same_thread=False) as conn:
        conn.execute("PRAGMA busy_timeout = 5000")  # Set a timeout of 5000ms (5 seconds)
        c = conn.cursor()
        # Insert into the 'orders' table, notice the change to match your schema
        c.execute("INSERT INTO orders (product_id, product_name, price, payment_method, bitcoin_address) VALUES (?, ?, ?, ?, ?)",
                  (product_id, product_name, str(price), payment_method, wallet))  # Convert price to string
        conn.commit()

    # Send a notification to the admin (like email)
    send_admin_notification(product_name, price, payment_method, wallet)

def send_admin_notification(product_name, price, payment_method, wallet):
    # Example of sending email, modify according to your needs
    admin_email = "BESTBILLS901@example.com"
    subject = f"New Order: {product_name}"
    body = f"Product: {product_name}\nPrice: {price}\nPayment Method: {payment_method}\nWallet: {wallet}"

    # Replace with your email service and credentials (example using Gmail SMTP)
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login("your_email@gmail.com", "your_password")  # Use real credentials
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail("your_email@gmail.com", admin_email, message)

@app.route('/')
def home():
    products = get_products()  # Fetch products from the database
    return render_template('index.html', products=products)  # Render the homepage with the products list

@app.route('/shop')
def shop():
    products = get_products()  # Fetch products from the database
    return render_template('shop.html', products=products)  # Render the shop page with the products list

@app.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product(product_id):
    product = get_product_by_id(product_id)
    if not product:
        return "Product not found.", 404

    if request.method == 'POST':
        price = request.form['price']
        payment_method = request.form['payment_method']
        wallet = BITCOIN_WALLET if payment_method == "Bitcoin" else USDT_WALLET

        add_order(product_id, product[1], price, payment_method, wallet)

        return redirect(url_for('payment_page', product_id=product_id, price=price, payment_method=payment_method))

    return render_template('product.html', product=product)
    
@app.route('/payment')
def payment_page():
    product_id = request.args.get('product_id')
    price = request.args.get('price')
    payment_method = request.args.get('payment_method')

    product = get_product_by_id(product_id)
    if not product:
        return "Product not found.", 404

    wallet = BITCOIN_WALLET if payment_method == "Bitcoin" else USDT_WALLET

    return render_template('payment.html', product=product, price=price, payment_method=payment_method, wallet=wallet)

if __name__ == '__main__':
    app.run(debug=True, port=5020)  # Adjust the port number if necessary
