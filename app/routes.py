from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, login, db
from app.forms import LoginForm, RegistrationForm, CreateCustomerForm, DeleteForm
from app.models import User, Customer, Order


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now registered!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/customers')
@login_required
def customers():
    customers = Customer.query.all()
    return render_template('customers.html', customers=customers)


@app.route('/create_customer', methods=['GET', 'POST'])
@login_required
def create_customer():
    form = CreateCustomerForm()
    if form.validate_on_submit():
        customer = Customer(name=form.name.data, email=form.email.data, company=form.company.data,
                            phone=form.phone.data,
                            address=form.address.data)
        db.session.add(customer)
        db.session.commit()
        flash('New customer added!')
        return redirect(url_for('detail_customer', number=customer.id))
    return render_template('create_customer.html', form=form)


@app.route('/customer/<number>')
@login_required
def detail_customer(number):
    customer = Customer.query.filter_by(id=number).first()
    return render_template('detail_customer.html', customer=customer)


@app.route('/delete_customer/<number>', methods=['GET', 'POST'])
@login_required
def delete_customer(number):
    customer = Customer.query.get_or_404(number)
    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(customer)
        db.session.commit()
        flash('Customer has been removed')
        return redirect(url_for('customers'))
    return render_template('delete.html', form=form, customer=customer)


@app.route('/edit_customer/<number>', methods=['GET', 'POST'])
@login_required
def edit_customer(number):
    customer = Customer.query.get(number)
    form = CreateCustomerForm(obj=customer)
    if form.validate_on_submit():
        form.populate_obj(customer)
        db.session.commit()
        flash('Successfully Updated')
        return redirect(url_for('detail_customer', number=customer.id))
    return render_template('create_customer.html', form=form)


@app.route('/create_order')
@login_required
def create_order():
    customer_id = request.args.get('customer_id')
    order = Order(customer_id=customer_id)
    db.session.add(order)
    db.session.commit()
    flash('New order created')
    return redirect(url_for('index'))


@app.route('/orders')
@login_required
def orders():
    customer_id = request.args.get('customer_id')
    customer = Customer.query.get(customer_id)
    orders = customer.order
    return render_template('orders.html', orders=orders)
