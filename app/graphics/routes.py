from flask import render_template, flash, redirect, url_for
from flask_login import login_required
from app import db
from app.graphics.forms import CreateGraphicsForm
from app.graphics import bp

@bp.route('/create')
@login_required
def create_graphics():
    form = CreateGraphicsForm()
    return render_template('graphics/create_graphics.html', form=form)