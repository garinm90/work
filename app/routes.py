from flask import render_template, flash, redirect, url_for, request, current_app, session
from flask_login import current_user, login_user, logout_user, login_required
from flask_principal import identity_loaded, RoleNeed, UserNeed, Permission, identity_changed, Identity, AnonymousIdentity, RoleNeed
from app import app, db, images
from app.forms import  ImageUploadForm, QuoteForm
from app.models import User, Customer, Order, Image, Controller


@app.errorhandler(403)
def page_not_found(e):
    flash(f'403 Forbidden {request.url}')
    session['redirected_from'] = request.url
    return redirect(url_for('main.index'))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    order_id = request.args.get('order_id')
    if order_id is not None:
        session['order'] = order_id
    form = ImageUploadForm(order=order_id)
    # orders = Order.query.all()
    if order_id is None:
        order_information = Order.query.get(int(session['order']))
    else:
        order_information = Order.query.get(int(order_id))
    # orders = [(o.id, '{} Order #{}'.format(o.customer, o.id, o.ride)) for o in orders]
    # form.order.choices = orders
    if request.method == 'POST':
        for key, f in request.files.items():
            if key.startswith('file'):
                filename = images.save(f)
                print(session['order'])
                i = Image(filename=filename, order_id=session['order'])
                db.session.add(i)
                db.session.commit()
                print('success')
        # for picture in request.files.getlist("myDropzone"):
            # print(picture)
            # filename = images.save(picture)
            # i = Image(filename=filename, order_id=form.order.data)
            # db.session.add(i)
            # db.session.commit()
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


