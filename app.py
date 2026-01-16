from flask import Flask, render_template, request, redirect
from db import get_db_connection

# Server = a program that stays ON and responds when someone asks for something.
app = Flask(__name__)

@app.route("/")
def home():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("home.html", products=products)

@app.route("/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO products (name, price) VALUES (%s, %s)",
            (name, price)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/")
    
    return render_template("add_product.html")

@app.route("/delete/<int:id>")
def delete_product(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM products WHERE id = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_product(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ---------- WHEN PAGE IS OPENED ----------
    if request.method == "GET":
        cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
        product = cursor.fetchone()

        cursor.close()
        conn.close()

        return render_template("edit.html", product=product)

    # ---------- WHEN FORM IS SUBMITTED ----------
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]

        cursor.execute(
            "UPDATE products SET name=%s, price=%s WHERE id=%s",
            (name, price, id)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
