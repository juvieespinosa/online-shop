from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop import db, app
from shop.products.models import Addproduct
from shop.products.routes import brands, categories


def MagerDicts(dict1,dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False



@app.route("/addcart", methods=["POST"])
def AddCart():
    try:
        product_id = request.form.get("product_id")
        product = Addproduct.query.filter_by(id=product_id).first()
        if product_id and request.method == "POST":
            DictItems = {product_id:{'name':product.name,'price':product.price,
                                     'image':product.image_1}}
            if "Shoppingcart" in session:
                print(session["Shoppingcart"])
                if product_id in session["Shoppingcart"]:
                    print("This product in already in your cart")
                else:
                    session["Shoppingcart"] = MagerDicts(session["Shoppingcart"], DictItems)
                    return redirect(request.referrer)
            else:
                session["Shoppingcart"] = DictItems
                return redirect(request.referrer)

    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)



@app.route('/carts')
def getCart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for("home"))
    price = 0
    subtotal = 0
    grandtotal = 0
    for key, product in session["Shoppingcart"].items():
        price += float(product["price"])
        subtotal += float(product['price'])
        shipping = (7.99)
        tax = ("%.2f" %(.07 * float(price)))
        grandtotal = ("%.2f" % (1.07 * price + shipping))

    return render_template("products/carts.html", grandtotal=grandtotal, subtotal=subtotal, shipping=shipping, tax=tax, brands=brands(), categories=categories())


@app.route("/deleteitem/<int:id>")
def deleteitem(id):
    if "Shoppingcart" not in session or len(session["Shoppingcart"]) <= 0:
        return redirect(url_for("home"))
    try:
        session.modified = True
        for key, item in session["Shoppingcart"].items():
            if int(key) == id:
                session["Shoppingcart"].pop(key, None)
                return redirect(url_for("getCart"))
    except Exception as e:
        print(e)
        return redirect(url_for("getCart"))


@app.route("/clearcart")
def clearcart():
    try:
        session.pop("Shoppingcart", None)
        return redirect(url_for("home"))
    except Exception as e:
        print(e)