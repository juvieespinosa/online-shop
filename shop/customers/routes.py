from flask import redirect, render_template, url_for, flash, request, session, abort, current_app, Response
from flask_login import login_user, login_required, current_user, logout_user, LoginManager
from werkzeug.exceptions import Unauthorized
from shop import db, app, photos, bcrypt, login_manager
from .forms import CustomerRegisterForm, CustomerLoginFrom
from .models import Register, CustomerOrder
import secrets
from dotenv import load_dotenv
import os
import stripe
import json

from ..admin.models import User

load_dotenv()

login = LoginManager(app)

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)



publishable_key = os.getenv("STRIPE_PUBLISHABLE_KEY")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


@app.route("/payment", methods=["POST"])
def payment():
    invoice = request.form.get('invoice')
    amount = request.form.get('amount')
    customer = stripe.Customer.create(
      email=request.form['stripeEmail'],
      source=request.form['stripeToken'],
    )
    charge = stripe.Charge.create(
      customer=customer.id,
      description="JHUV'S SHOPLINE",
      amount=amount,
      currency='usd',
    )
    orders = CustomerOrder.query.filter_by(customer_id=current_user.id, invoice=invoice).order_by(
        CustomerOrder.id.desc()).first()
    orders.status = "Paid"
    db.session.commit()
    return redirect(url_for("confirmation"))


@app.route("/confirmation")
def confirmation():
    return render_template('customer/confirmation.html')


@app.route("/customer/register", methods=["GET", "POST"])
def customer_register():
    form = CustomerRegisterForm()
    if form.validate_on_submit():
            hash_password = bcrypt.generate_password_hash(form.password.data)
            register = Register(name=form.name.data, email=form.email.data,  contact=form.contact.data,
                                password=hash_password, address=form.address.data, city=form.city.data,
                             zipcode=form.zipcode.data, country=form.country.data,)
            db.session.add(register)
            flash(f'Welcome {form.name.data}! Thanks for signing up!', 'success')
            db.session.commit()
            return redirect(url_for('customerLogin'))
    return render_template('customer/register.html', form=form)


@app.route('/customer/login', methods=["GET", "POST"])
def customerLogin():
    form = CustomerLoginFrom()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You are login now!', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash('Wrong email and password', 'danger')
        return redirect(url_for('customerLogin'))
    return render_template('customer/login.html', form=form)


@app.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect(url_for('home'))



def updateshoppingcart():
    for key, shopping in session['Shoppingcart'].items():
        session.modified = True
        del shopping['image']
    return updateshoppingcart


@app.route('/getorder')
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        updateshoppingcart()
        try:
            order = CustomerOrder(invoice=invoice, customer_id=customer_id, orders=session['Shoppingcart'])
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            return redirect(url_for('orders', invoice=invoice))
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))
    else:
        if "email" not in session:
            flash(f"Please login first", "danger")
            return redirect(url_for("customerLogin"))




@app.route('/orders/<invoice>')
def orders(invoice):
    if current_user.is_authenticated:
        price = 0
        subtotal = 0
        grandtotal = 0
        customer_id = current_user.id
        customer = Register.query.filter_by(id=customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id=customer_id, invoice=invoice).order_by(CustomerOrder.id.desc()).first()
        for _key, product in orders.orders.items():
            price += float(product["price"])
            subtotal += float(product['price'])
            shipping = (7.99)
            tax = ("%.2f" % (.07 * float(price)))
            grandtotal = ("%.2f" % (1.07 * price + shipping))

    else:
        return redirect(url_for('customerLogin'))
    return render_template('customer/order.html', invoice=invoice, tax=tax, shipping=shipping, subtotal=subtotal, grandtotal=grandtotal, customer=customer, orders=orders)


