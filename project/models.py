
#from datetime import datetime

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
    role = db.Column(db.Integer, default='0')

    def __init__(self, name=None, email=None, password=None, status=0, nomorhp=None, role=0):
        self.name = name
        self.email = email
        self.password = password
        self.status = status
        self.nomorhp = nomorhp
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
