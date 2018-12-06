from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Customer(db.Model):
    name = db.Column(db.String(120), index=True)
    email = db.Column(db.String(64), index=True, unique=True)
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    order = db.relationship('Order', backref='customer', lazy=True, cascade='delete,all')
    controller = db.relationship('Controller', backref='customer', lazy=True, cascade='delete,all')


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer(), db.ForeignKey('customer.id'))


class Controller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer(), db.ForeignKey('order.id'))
    customer_id = db.Column(db.Integer(), db.ForeignKey('customer.id'))
    images = db.Column(db)
