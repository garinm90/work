from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_principal import Principal

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

from app import routes, models
