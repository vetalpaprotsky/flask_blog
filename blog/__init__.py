from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b761c08b1700924b80af4500b79575fc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Just running all of the code in routes.py file. In order to avoid the
# circular imports error, routes.py needs to be imported at the bottom of
# this file, because routes.py imports app instance from here.
from blog import routes  # noqa: F401,E402
