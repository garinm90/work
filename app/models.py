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
    controller = db.relationship('Controller', backref='order', lazy=True, cascade='delete,all')
    bubble_six = db.Column(db.Boolean(), nullable=True)
    bubble_nine = db.Column(db.Boolean(), nullable=True)
    bubble_fourteen = db.Column(db.Boolean(), nullable=True)
    puck_six = db.Column(db.Boolean(), nullable=True)
    puck_molex_six = db.Column(db.Boolean(), nullable=True)
    puck_nine = db.Column(db.Boolean(), nullable=True)
    long_nineteen = db.Column(db.Boolean(), nullable=True)
    short_nineteen = db.Column(db.Boolean(), nullable=True)
    green_nineteen = db.Column(db.Boolean(), nullable=True)
    ads_twentyfour = db.Column(db.Boolean(), nullable=True)
    ads_thirtysix = db.Column(db.Boolean(), nullable=True)
    two_forty = db.Column(db.Boolean(), nullable=True)
    three_twenty = db.Column(db.Boolean(), nullable=True)


class Controller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer(), db.ForeignKey('order.id'))
    customer_id = db.Column(db.Integer(), db.ForeignKey('customer.id'))
    image = db.relationship('Image', backref='controller', lazy=True, cascade='delete,all')


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String())
    url = db.Column(db.String())
    controller_id = db.Column(db.Integer(), db.ForeignKey('controller.id'))
