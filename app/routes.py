from flask import render_template, flash, redirect, url_for, request, current_app, session
from flask_login import current_user, login_user, logout_user, login_required
from flask_principal import identity_loaded, RoleNeed, UserNeed, Permission, identity_changed, Identity, AnonymousIdentity, RoleNeed
from werkzeug.urls import url_parse
from app import app, db, images
from app.forms import LoginForm, RegistrationForm, CreateCustomerForm, DeleteForm, CreateOrderForm, ImageUploadForm, \
    QuoteForm, CreateControllerForm
from app.models import User, Customer, Order, Image, Controller

admin_permission = Permission(RoleNeed('admin'))

@app.errorhandler(403)
def page_not_found(e):
    flash(f'403 Forbidden {request.url}')
    session['redirected_from'] = request.url
    return redirect(url_for('index'))

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    # Assuming the User model has a list of roles, update the
    # identity with the roles that the user provides
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.name))


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
        identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.id))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())
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
@admin_permission.require(http_exception=403)
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
        flash(f'Updated order #{order.id} for {order.customer}')
        return redirect(url_for('detail_order', number=order.id))
    return render_template('create_order.html', form=form, title=f'Edit Order for {order.customer}')


@app.route('/order/<number>')
@login_required
def detail_order(number):
    order = Order.query.get(number)
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
    return render_template('orders.html', orders=orders, title=f'Order List for {customer.name.title()}', customer_id=customer_id)


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
        return redirect(url_for('detail_order', number=order_id))
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


@app.route('/create_controller', methods=['GET', 'POST'])
@login_required
def create_controller():
    customers = Customer.query.all()
    orders = Order.query.all()
    order_id = request.args.get('order_id', 1)
    customer_id = request.args.get('customer_id', 1)
    form = CreateControllerForm(order=order_id, customer=customer_id)
    form.customer_id.choices = [(c.id, '{}'.format(c)) for c in customers]
    form.order_id.choices = [(o.id, '{} Order #{}'.format(o.ride.capitalize(), o.id)) for o in orders]
    controller = Controller()
    if form.validate_on_submit():
        controller = Controller(controller_number=form.controller_number.data, order_id=form.order.data, customer_id=form.customer.data,
        t_one_thousand=form.t_one_thousand.data, t_one_thousand_a=form.t_one_thousand_a.data, ym_four=form.ym_four.data, ym_eight=form.ym_eight.data,
        falcon_two=form.falcon_two.data, falcon_four=form.falcon_four.data, falcon_sixteen=form.falcon_sixteen.data, twentyfour_to_five=form.twentyfour_to_five.data,
        twentyfour_to_twelve=form.twentyfour_to_twelve.data, number_of_datas=form.number_of_datas.data, raspberry_pi=form.raspberry_pi.data, tp_link=form.tp_link.data,
        spokes=form.spokes.data, boxes=form.boxes.data, phoenix_one_by_one=form.phoenix_one_by_one.data, phoenix_one_by_two=form.phoenix_one_by_two.data, phoenix_two_by_two=form.phoenix_two_by_two.data)
        db.session.add(controller)
        db.session.commit()
        flash('Successfully added controller!')
        return redirect(url_for('detail_controller', controller_number=controller.controller_number))
    return render_template('create_controller.html', form=form, title='Create Controller')

@app.route('/controller/<controller_number>')
@login_required
def detail_controller(controller_number):
    controller = Controller.query.filter_by(controller_number=controller_number).first()
    return render_template('detail_controller.html', controller=controller, image_url=images.url)

@app.route('/controller/<controller_number>/edit', methods=['GET', 'POST'])
@login_required
def edit_controller(controller_number):
    controller = Controller.query.filter_by(controller_number=controller_number).first()
    customers = Customer.query.all()
    orders = Order.query.all()
    form = CreateControllerForm(obj=controller)
    form.customer_id.choices = [(c.id, '{}'.format(c)) for c in customers]
    form.order_id.choices = [(o.id, '{} Order #{}'.format(o.ride.capitalize(), o.id)) for o in orders]
    if form.validate_on_submit():
        form.populate_obj(controller)
        db.session.commit()
        flash(f'Updated controller #{controller.controller_number} for {controller.customer}')
        return redirect(url_for('detail_controller', controller_number=controller.controller_number))
    return render_template('create_controller.html', form=form)

@app.route('/controllers')
@login_required
def list_controllers():
    controllers = Controller.query.all()
    return render_template('list_controllers.html', controllers=controllers)