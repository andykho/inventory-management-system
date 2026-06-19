from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "inventory-secret-key"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="inventory_db",
    port=3306
)

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM users
            WHERE username = %s
            AND password = %s
        """, (
            username,
            password
        ))

        user = cursor.fetchone()

        if user:

            session["user_id"] = user["id"]
            session["username"] = user["username"]

            return redirect("/")

    return render_template("login.html")

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")

@app.route("/")
def home():

    if "user_id" not in session:
        return redirect("/login")
    
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM products")
    total_products = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM suppliers")
    total_suppliers = cursor.fetchone()[0]

    return f"""
    <h1>Inventory Dashboard</h1>

    <p>Total Products: {total_products}</p>
    <p>Total Suppliers: {total_suppliers}</p>

    <hr>

    <h3>Menu</h3>

    <ul>
        <li><a href="/products">Products</a></li>
        <li><a href="/suppliers">Suppliers</a></li>
        <li><a href="/logout">Logout</a></li>
    </ul>
    """

@app.route("/products")
def products():

    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    return render_template(
        "products.html",
        products=products
    )

@app.route("/add-product", methods=["GET", "POST"])
def add_product():

    if request.method == "POST":

        product_code = request.form["product_code"]
        product_name = request.form["product_name"]
        current_stock = request.form["current_stock"]
        minimum_stock = request.form["minimum_stock"]
        supplier_id = request.form["supplier_id"]

        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO products
            (product_code, product_name, current_stock, minimum_stock, supplier_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            product_code,
            product_name,
            current_stock,
            minimum_stock,
            supplier_id
        ))

        db.commit()

        return redirect("/products")

    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM suppliers")
    suppliers = cursor.fetchall()

    return render_template(
        "add_product.html",
        suppliers=suppliers
    )

@app.route("/suppliers")
def suppliers():

    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM suppliers")
    suppliers = cursor.fetchall()

    return render_template(
        "suppliers.html",
        suppliers=suppliers
    )

@app.route("/add-supplier", methods=["GET", "POST"])
def add_supplier():

    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]
        address = request.form["address"]

        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO suppliers
            (name, phone, address)
            VALUES (%s, %s, %s)
        """, (
            name,
            phone,
            address
        ))

        db.commit()

        return redirect("/suppliers")

    return render_template("add_supplier.html")

@app.route("/delete-product/<int:id>")
def delete_product(id):

    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM products WHERE id = %s",
        (id,)
    )

    db.commit()

    return redirect("/products")

@app.route("/delete-supplier/<int:id>")
def delete_supplier(id):

    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM suppliers WHERE id = %s",
        (id,)
    )

    db.commit()

    return redirect("/suppliers")

@app.route("/edit-product/<int:id>", methods=["GET", "POST"])
def edit_product(id):

    cursor = db.cursor(dictionary=True)

    if request.method == "POST":

        product_code = request.form["product_code"]
        product_name = request.form["product_name"]
        current_stock = request.form["current_stock"]
        minimum_stock = request.form["minimum_stock"]
        supplier_id = request.form["supplier_id"]

        cursor.execute("""
            UPDATE products
            SET
                product_code = %s,
                product_name = %s,
                current_stock = %s,
                minimum_stock = %s,
                supplier_id = %s
            WHERE id = %s
        """, (
            product_code,
            product_name,
            current_stock,
            minimum_stock,
            supplier_id,
            id
        ))

        db.commit()

        return redirect("/products")

    cursor.execute(
        "SELECT * FROM products WHERE id = %s",
        (id,)
    )

    product = cursor.fetchone()

    cursor.execute("SELECT * FROM suppliers")
    suppliers = cursor.fetchall()

    return render_template(
        "edit_product.html",
        product=product,
        suppliers=suppliers
    )

@app.route("/edit-supplier/<int:id>", methods=["GET", "POST"])
def edit_supplier(id):

    cursor = db.cursor(dictionary=True)

    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]
        address = request.form["address"]

        cursor.execute("""
            UPDATE suppliers
            SET
                name = %s,
                phone = %s,
                address = %s
            WHERE id = %s
        """, (
            name,
            phone,
            address,
            id
        ))

        db.commit()

        return redirect("/suppliers")

    cursor.execute(
        "SELECT * FROM suppliers WHERE id = %s",
        (id,)
    )

    supplier = cursor.fetchone()

    return render_template(
        "edit_supplier.html",
        supplier=supplier
    )

if __name__ == "__main__":
    app.run(debug=True)