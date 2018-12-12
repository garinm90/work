from datetime import datetime
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

    def set_lower(self):
        self.name = self.name.lower()

    def __repr__(self):
        return self.name.title()


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer(), db.ForeignKey('customer.id'))
    controller = db.relationship('Controller', backref='order', lazy=True, cascade='delete,all')
    bubble_six = db.Column(db.Integer(), nullable=False)
    bubble_nine = db.Column(db.Integer(), nullable=False)
    bubble_fourteen = db.Column(db.Integer(), nullable=False)
    puck_six = db.Column(db.Integer(), nullable=False)
    puck_molex_six = db.Column(db.Integer(), nullable=False)
    puck_nine = db.Column(db.Integer(), nullable=False)
    long_nineteen = db.Column(db.Integer(), nullable=False)
    short_nineteen = db.Column(db.Integer(), nullable=False)
    green_nineteen = db.Column(db.Integer(), nullable=False)
    ads_twentyfour = db.Column(db.Integer(), nullable=False)
    ads_thirtysix = db.Column(db.Integer(), nullable=False)
    two_forty = db.Column(db.Integer(), nullable=False)
    three_twenty = db.Column(db.Integer(), nullable=False)
    image = db.relationship('Image', backref='order', lazy=True, cascade='delete,all')
    controller = db.relationship('Controller', backref='controller', lazy=True, cascade='delete,all')
    ride = db.Column(db.String(128), nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def set_lower(self):
        self.ride = self.ride.lower()


class Controller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer(), db.ForeignKey('order.id'))
    customer_id = db.Column(db.Integer(), db.ForeignKey('customer.id'))
    t_one_thousand = db.Column(db.Integer())
    t_one_thousand_a = db.Column(db.Integer())
    ym_four = db.Column(db.Integer())
    ym_eight = db.Column(db.Integer())
    falcon_two = db.Column(db.Integer)
    falcon_four = db.Column(db.Integer())
    falcon_sixteen = db.Column(db.Integer())
    twentyfour_to_five = db.Column(db.Integer())
    twentyfour_to_twelve = db.Column(db.Integer())
    number_of_datas = db.Column(db.Integer())
    raspberry_pi = db.Column(db.Integer())
    tp_link = db.Column(db.Integer())
    spokes = db.Column(db.Integer())
    boxes = db.Column(db.String())


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String())
    url = db.Column(db.String())
    controller_id = db.Column(db.Integer(), db.ForeignKey('controller.id'))
    order_id = db.Column(db.Integer(), db.ForeignKey('order.id'))
