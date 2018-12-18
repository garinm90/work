from flask import render_template, flash, redirect, url_for, request, current_app, session
from flask_login import current_user, login_user, logout_user, login_required
from flask_principal import identity_loaded, RoleNeed, UserNeed, Permission, identity_changed, Identity, AnonymousIdentity, RoleNeed
from app import app, db, images
from app.forms import  ImageUploadForm, \
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