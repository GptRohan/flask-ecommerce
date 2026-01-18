from flask import Flask, render_template, request, redirect
from db import get_products_collection

# Server = a program that stays ON and responds when someone asks for something.
app = Flask(__name__)



@app.route("/")
def home():
    products_col = get_products_collection()
    products = list(products_col.find())
    return render_template("home.html", products=products)

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    price = request.form["price"]

    get_products_collection().insert_one({
        "name": name,
        "price": price
    })
    return redirect("/")

@app.route("/delete/<id>")
def delete(id):
    get_products_collection().delete_one({"_id": ObjectId(id)})
    return redirect("/")


from bson.objectid import ObjectId

@app.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    col = get_products_collection()

    if request.method == "POST":
        col.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "name": request.form["name"],
                "price": request.form["price"]
            }}
        )
        return redirect("/")

    product = col.find_one({"_id": ObjectId(id)})
    return render_template("edit.html", product=product)


if __name__ == "__main__":
    app.run(debug=True)
