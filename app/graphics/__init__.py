from flask import Blueprint

bp = Blueprint('graphics', __name__)

from app.graphics import routes, forms