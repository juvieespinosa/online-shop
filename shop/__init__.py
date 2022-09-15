from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads
from flask_migrate import Migrate
from dotenv import load_dotenv
import os


load_dotenv()


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///shopping.db")
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


db = SQLAlchemy(app)
Bootstrap(app)
bcrypt = Bcrypt(app)

migrate = Migrate(app, db)
with app.app_context():
    if db.engine.url.drivername == "sqlite":
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="customerLogin"
login_manager.needs_refresh_message_category="danger"
login_manager.login_message = u"Please login first."


from shop.admin import routes
from shop.products import routes
from shop.carts import carts
from shop.customers import routes