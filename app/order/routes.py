from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required
from app import db, images
from app.order.forms import CreateOrderForm
from app.models import Order, Customer
from app.order import bp

@bp.route('/create_order', methods=['GET', 'POST'])
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
        return redirect(url_for('main.index'))
    return render_template('order/create_order.html', form=form, title=f'Create order for {customer.name.title()}')

@bp.route('/edit_order/<number>', methods=['GET', 'POST'])
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
        return redirect(url_for('order.detail_order', number=order.id))
    return render_template('order/create_order.html', form=form, title=f'Edit Order for {order.customer}')

@bp.route('/order/<number>')
@login_required
def detail_order(number):
    order = Order.query.get(number)
    return render_template('order/detail_order.html', order=order, image_url=images.url)


@bp.route('/orders/<customer_id>')
@login_required
def customer_orders(customer_id):
    customer = Customer.query.get(customer_id)
    orders = customer.order
    for order in orders:
        for image in order.image:
            url = images.url(image.filename)
            print(url)
    return render_template('order/orders.html', orders=orders, title=f'Order List for {customer.name.title()}', customer_id=customer_id)


@bp.route('/orders')
def list_orders():
    orders = Order.query.all()
    return render_template('order/list_orders.html', orders=orders, title='All Orders')

