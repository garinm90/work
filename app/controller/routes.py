from flask import request, flash, redirect, url_for, render_template
from flask_login import login_required
from app import db, images
from app.controller.forms import CreateControllerForm
from app.models import Controller, Customer, Order
from app.controller import bp


@bp.route('/create_controller', methods=['GET', 'POST'])
@login_required
def create_controller():
    customers = Customer.query.all()
    orders = Order.query.all()
    order_id = request.args.get('order_id', 1)
    customer_id = request.args.get('customer_id', 1)
    form = CreateControllerForm(order=order_id, customer=customer_id)
    form.customer_id.choices = [(c.id, '{}'.format(c)) for c in customers]
    form.order_id.choices = [(o.id, '{} Job #{}'.format(o.ride.capitalize(), o.id)) for o in orders]
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
        return redirect(url_for('controller.detail_controller', controller_number=controller.controller_number))
    return render_template('controller/create_controller.html', form=form, title='Create Controller')

@bp.route('/controller/<controller_number>')
@login_required
def detail_controller(controller_number):
    controller = Controller.query.filter_by(controller_number=controller_number).first()
    return render_template('controller/detail_controller.html', controller=controller, image_url=images.url)

@bp.route('/controller/<controller_number>/edit', methods=['GET', 'POST'])
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
        return redirect(url_for('controller.detail_controller', controller_number=controller.controller_number))
    return render_template('controller/create_controller.html', form=form)

@bp.route('/controllers')
@login_required
def list_controllers():
    controllers = Controller.query.all()
    return render_template('controller/list_controllers.html', controllers=controllers)