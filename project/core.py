
from project import app
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
import config

db = SQLAlchemy(app)
encrypt = Bcrypt(app)
mail = Mail(app)