from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_principal import Principal, UserNeed, RoleNeed, identity_loaded

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'main.login'
images = UploadSet('images', IMAGES)
configure_uploads(app, images)
principals = Principal(app)


from app.main import bp as main_bp
app.register_blueprint(main_bp)

from app.customer import bp as customer_bp
app.register_blueprint(customer_bp)

from app.order import bp as order_bp
app.register_blueprint(order_bp)

from app.controller import bp as controller_bp
app.register_blueprint(controller_bp)

from app.calculator import bp as calculator_bp
app.register_blueprint(calculator_bp)

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

from app import routes, models
