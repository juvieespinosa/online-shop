from flask_login import UserMixin
from shop import db
from datetime import datetime
# from flask_security import UserMixin, RoleMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=False, nullable=False)
    profile = db.Column(db.String(180), unique=False, nullable=False,default='profile.jpg')



    def __repr__(self):
        return "<User %r>" % self.username


db.create_all()