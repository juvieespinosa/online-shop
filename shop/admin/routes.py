from flask import Flask, render_template, session, request, redirect, url_for, flash, abort
from flask_login import login_user, login_required, current_user, logout_user, LoginManager
from shop import app, db, bcrypt
from .forms import RegistrationForm, LoginForm
from .models import User
from shop.products.models import Addproduct, Brand, Category
from functools import wraps

from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView


login = LoginManager(app)

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login"))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

admin = Admin(app, index_view=AdminIndexView())
admin.add_view(ModelView(User, db.session))


# def admin_only(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if current_user.id != 1:
#             return abort(403)
#         return f(*args, **kwargs)
#     return decorated_function


@app.route("/admin")
def admin():
    if "email" not in session:
        flash(f"Please login first", "danger")
        return redirect(url_for("login"))
    products = Addproduct.query.all()
    return render_template("admin/index.html", title="Admin Page", products=products)

@app.route("/brands")
def brands():
    if "email" not in session:
        flash(f"Please login first", "danger")
        return redirect(url_for("login"))
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template("admin/brand.html", title="Brand Page", brands=brands)

@app.route("/category")
def category():
    if "email" not in session:
        flash(f"Please login first", "danger")
        return redirect(url_for("login"))
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template("admin/brand.html", title="Category Page", categories=categories)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data,email=form.email.data,
            password=hash_password)
        db.session.add(user)
        flash(f'Welcome {form.name.data}! Thanks for signing up!','success')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('admin/register.html',title='Register user', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'Welcome {form.email.data} You have successfully logged in.','success')
            return redirect(url_for('admin'))
            # return redirect(request.args.get("next") or url_for("admin"))
        else:
            flash(f'Wrong email and password', 'danger')
            # return redirect(url_for('home'))
    return render_template('admin/login.html', title='Login Page', form=form)