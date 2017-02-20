
#from datetime import datetime
import datetime
from project.core import db, encrypt
from project import app

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, default=None, nullable=True)
    status = db.Column(db.Integer, default=0)
    nomorhp = db.Column(db.String, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    role = db.Column(db.Integer, default='0')

    def __init__(self, name=None, email=None, password=None, status=0, nomorhp=None, role=0):
        self.name = name
        self.email = email
        self.password = password
        self.status = status
        self.nomorhp = nomorhp
        self.registered_on = datetime.date.today()
        self.role = role

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User {0}>'.format(self.name)

class ActivationCode(db.Model):

    __tablename__ = 'activationcode'

    id = db.Column(db.Integer,primary_key=True)
    email_user = db.Column(db.String,nullable=False,unique=True)
    activationcode = db.Column(db.String,nullable=False,unique=True)

    def __init__(self,id=None,email_user=None,activationcode=None):
        self.id = id
        self.email_user = email_user
        self.activationcode = activationcode

class Instance(db.Model):

    __tablename__ = 'instances'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, unique=True)
    instance_id = db.Column(db.String, unique=True)
    build_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id=None, instance_id=None):
        self.user_id = user_id
        self.instance_id=instance_id
        self.build_on = datetime.date.today

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<Instance {0}>'.format(self.instance_id)
