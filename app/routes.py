from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db, images
from app.forms import LoginForm, RegistrationForm, CreateCustomerForm, DeleteForm, CreateOrderForm, ImageUploadForm, \
    QuoteForm
from app.models import User, Customer, Order, Image


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
    return render_template('list_customers.html', title='Customer List', customers=customers)


@app.route('/create_customer', methods=['GET', 'POST'])
@login_required
def create_customer():
    form = CreateCustomerForm(original_email="")
    if form.validate_on_submit():
        customer = Customer(name=form.name.data.lower(), email=form.email.data, company=form.company.data,
                            phone=form.phone.data,
                            address=form.address.data)
        db.session.add(customer)
        db.session.commit()
        flash('New customer added!')
        return redirect(url_for('detail_customer', number=customer.id))
    return render_template('create_customer.html', title='Create Customer', form=form)


@app.route('/customer/<number>')
@login_required
def detail_customer(number):
    customer = Customer.query.filter_by(id=number).first()
    return render_template('detail_customer.html', title=customer.name.title(), customer=customer)


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
    return render_template('delete.html', form=form, customer=customer, title=f'Delete {customer.name}')


@app.route('/edit_customer/<number>', methods=['GET', 'POST'])
@login_required
def edit_customer(number):
    customer = Customer.query.get(number)
    form = CreateCustomerForm(obj=customer, original_email=customer.email)
    if form.validate_on_submit():
        form.populate_obj(customer)
        customer.set_lower()
        db.session.commit()
        flash('Successfully Updated')
        return redirect(url_for('detail_customer', number=customer.id))
    return render_template('create_customer.html', title=f'Edit: {customer.name.title()}', form=form)


@app.route('/create_order', methods=['GET', 'POST'])
@login_required
def create_order():
    customer_number = request.args.get('customer_id', 1)
    form = CreateOrderForm(obj=request.form, customer_id=customer_number)
    customer = Customer.query.get(customer_number)
    form.customer_id.choices = [(g.id, g.name.title()) for g in Customer.query.all()]
    if form.validate_on_submit():
        order = Order(customer_id=form.customer_id.data, bubble_six=form.bubble_six.data,
                      bubble_nine=form.bubble_nine.data, bubble_fourteen=form.bubble_fourteen.data,
                      puck_six=form.puck_six.data, puck_molex_six=form.puck_molex_six.data,
                      puck_nine=form.puck_nine.data, long_nineteen=form.long_nineteen.data,
                      short_nineteen=form.short_nineteen.data, green_nineteen=form.green_nineteen.data,
                      ads_thirtysix=form.ads_thirtysix.data, ads_twentyfour=form.ads_twentyfour.data,
                      three_twenty=form.three_twenty.data, two_forty=form.two_forty.data, ride=form.ride.data.lower())
        order.set_lower()
        db.session.add(order)
        db.session.commit()
        flash('Order created!')
        return redirect(url_for('index'))
    return render_template('create_order.html', form=form, title=f'Create order for {customer.name.title()}')


@app.route('/edit_order/<number>', methods=['GET', 'POST'])
@login_required
def edit_order(number):
    order = Order.query.get(number)
    form = CreateOrderForm(obj=order)
    form.customer_id.choices = [(g.id, g.name.title()) for g in Customer.query.all()]
    if form.validate_on_submit():
        form.populate_obj(order)
        order.set_lower()
        db.session.commit()
        flash(f'Updated {order.customer_id}')
        return redirect(url_for('index'))
    return render_template('create_order.html', form=form, title=f'Edit Order for {order.customer}')


@app.route('/order/<number>')
@login_required
def detail_order(number):
    order = Order.query.get(number)
    keys = []
    for key, value in order.__dict__.items():
        print(key, value)
        if value == True:
            keys.append(key)
    return render_template('detail_order.html', order=order, image_url=images.url)


@app.route('/orders/<customer_id>')
@login_required
def customer_orders(customer_id):
    customer = Customer.query.get(customer_id)
    orders = customer.order
    for order in orders:
        for image in order.image:
            url = images.url(image.filename)
            print(url)
    return render_template('orders.html', orders=orders, title=f'Order List for {customer.name.title()}')


@app.route('/orders')
def list_orders():
    orders = Order.query.all()
    return render_template('list_orders.html', orders=orders, title='All Orders')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    order_id = request.args.get('order_id', 1)
    form = ImageUploadForm(order=order_id)
    orders = Order.query.all()
    order_information = Order.query.get(int(order_id))
    orders = [(o.id, '{} Order #{}'.format(o.customer, o.id, o.ride)) for o in orders]
    form.order.choices = orders
    if request.method == 'POST':
        for picture in request.files.getlist("images"):
            filename = images.save(picture)
            i = Image(filename=filename, order_id=form.order.data)
            db.session.add(i)
            db.session.commit()
        flash('Uploaded!')
        return redirect(url_for('view_images', order_id=form.order.data))
    return render_template('upload.html', form=form, order_information=order_information)


@app.route('/order/<order_id>/images')
@login_required
def view_images(order_id):
    pictures = Image.query.filter_by(order_id=order_id).all()
    image_files = []
    for image in pictures:
        image_files.append(images.url(image.filename))
    return render_template('images.html', pictures=image_files, order_id=order_id)


@app.route('/quote_one', methods=['GET', 'POST'])
@login_required
def quote_one():
    form = QuoteForm()
    part_one = True
    if request.method == 'POST':
        return redirect(url_for('quote_two'))
    return render_template('quote_first.html', form=form, part_one=part_one)


@app.route('/quote_two', methods=['GET', 'POST'])
@login_required
def quote_two():
    form = QuoteForm()
    part_two = True
    return render_template('quote_first.html', form=form, part_two=part_two)
