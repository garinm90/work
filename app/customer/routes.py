from flask import render_template, flash, redirect, url_for
from flask_login import login_required
from app import db
from app.models import Customer
from app.customer.forms import CreateCustomerForm, DeleteForm
from app.customer import bp

@bp.route('/customers')
@login_required
def customers():
    customers = Customer.query.all()
    return render_template('customer/list_customers.html', title='Customer List', customers=customers)


@bp.route('/create_customer', methods=['GET', 'POST'])
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
        return redirect(url_for('customer.detail_customer', number=customer.id))
    return render_template('customer/create_customer.html', title='Create Customer', form=form)


@bp.route('/customer/<number>')
@login_required
def detail_customer(number):
    customer = Customer.query.filter_by(id=number).first()
    return render_template('customer/detail_customer.html', title=customer.name.title(), customer=customer)


@bp.route('/delete_customer/<number>', methods=['GET', 'POST'])
@login_required
def delete_customer(number):
    customer = Customer.query.get_or_404(number)
    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(customer)
        db.session.commit()
        flash('Customer has been removed')
        return redirect(url_for('customer.customers'))
    return render_template('customer/delete.html', form=form, customer=customer, title=f'Delete {customer.name}')


@bp.route('/edit_customer/<number>', methods=['GET', 'POST'])
@login_required
def edit_customer(number):
    customer = Customer.query.get(number)
    form = CreateCustomerForm(obj=customer, original_email=customer.email)
    if form.validate_on_submit():
        form.populate_obj(customer)
        customer.set_lower()
        db.session.commit()
        flash('Successfully Updated')
        return redirect(url_for('customer.detail_customer', number=customer.id))
    return render_template('customer/create_customer.html', title=f'Edit: {customer.name.title()}', form=form)

