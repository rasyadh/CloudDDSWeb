
#from datetime import datetime
import datetime
from project.core import db, encrypt
from project import app

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), default=None, nullable=True)
    status = db.Column(db.Integer, default=0) #0=pending, 1=activate, 2=suspend, 3=delete
    nomorhp = db.Column(db.String(50), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    role = db.Column(db.Integer, default=0) #0=user, 1=admin, 2=superadmin
    keystone_token = db.Column(db.String(50),default="") #keperluan mobile

    def __init__(self, name=None, email=None, password=None, status=0, nomorhp=None, role=0, keystone_token=""):
        self.name = name
        self.email = email
        self.password = password
        self.status = status
        self.nomorhp = nomorhp
        self.registered_on = datetime.date.today()
        self.role = role
        self.keystone_token = keystone_token

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User {0}>'.format(self.name)

class Token(db.Model):

    __tablename__ = 'token'

    id = db.Column(db.Integer,primary_key=True)
    email_user = db.Column(db.String,nullable=False,unique=True)
    code = db.Column(db.String,nullable=False,unique=True)
    type = db.Column(db.Integer, nullable=False) #0 = registration, 1= reset password
    created_at = db.Column(db.DateTime)

    def __init__(self,id=None,email_user=None,code=None, type=None):
        self.id = id
        self.email_user = email_user
        self.code = code
        self.type = type
        self.created_at = datetime.date.today()

class Instance(db.Model):

    __tablename__ = 'instances'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    instance_id = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(50), nullable=False)
    image_name = db.Column(db.String(100), nullable=False)
    flavor_vcpu = db.Column(db.String(100), nullable=False)
    flavor_ram = db.Column(db.String(100), nullable=False)
    flavor_disk = db.Column(db.String(100), nullable=False)
    keyname = db.Column(db.String(100), nullable=False)
    purpose = db.Column(db.String(100), nullable=False)
    pic_name = db.Column(db.String(100), nullable=False)
    pic_telp = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Integer, default=1)
    request_at = db.Column(db.DateTime)
    build_on = db.Column(db.DateTime)

    def __init__(self, user_id=None, instance_id=None,name=None,image_name=None,flavor_vcpu=None, flavor_ram=None, flavor_disk=None, purpose=None, pic_name=None, pic_telp=None, status=None,request_at=None):
        self.user_id = user_id
        self.instance_id=instance_id
        self.name=name
        self.image_name=image_name
        self.flavor_vcpu = flavor_vcpu
        self.flavor_ram = flavor_ram
        self.flavor_disk = flavor_disk
        self.keyname = keyname
        self.purpose = purpose
        self.pic_name = pic_name
        self.pic_telp = pic_telp
        self.status=status
        self.request_at = request_at
        self.build_on = datetime.date.today()

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<Instance {0}>'.format(self.instance_id)

class Request(db.Model):

    __tablename__ = 'request_instance'

    id = db.Column(db.Integer, primary_key=True)
    owner_id=db.Column(db.String(100), nullable=False)
    server_id=db.Column(db.String(100), nullable=False, default="")
    name = db.Column(db.String(50), nullable=False)
    image_id = db.Column(db.String(100), nullable=False)
    image_name = db.Column(db.String(100), nullable=False)
    flavor_id = db.Column(db.String(100), nullable=False)
    flavor_vcpu = db.Column(db.String(100), nullable=False)
    flavor_ram = db.Column(db.String(100), nullable=False)
    flavor_disk = db.Column(db.String(100), nullable=False)
    network_id = db.Column(db.String(100), nullable=False)
    availability_zone = db.Column(db.String(100), nullable=False)
    keyname = db.Column(db.String(100), nullable=False)
    purpose = db.Column(db.String(100), nullable=False)
    pic_name = db.Column(db.String(100), nullable=False)
    pic_telp = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Integer, default=0) #0 = pending, 1 = accepted, 2 = decline
    request_at = db.Column(db.DateTime)

    def __init__(self,owner_id=None,server_id=None,name=None,image_id=None,image_name=None, flavor_id=None, flavor_vcpu=None, flavor_ram=None, flavor_disk=None,network_id=None, availability_zone=None, keyname=None, purpose=None, pic_name=None, pic_telp=None, status=None):
        self.owner_id = owner_id
        self.server_id = server_id
        self.name = name
        self.image_id = image_id
        self.image_name = image_name
        self.flavor_id = flavor_id
        self.flavor_vcpu = flavor_vcpu
        self.flavor_ram = flavor_ram
        self.flavor_disk = flavor_disk
        self.network_id = network_id
        self.availability_zone = availability_zone
        self.keyname = keyname
        self.purpose = purpose
        self.pic_name = pic_name
        self.pic_telp = pic_telp
        self.status = status
        self.request_at = datetime.date.today()

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<Request Instance {0}>'.format(self.name)

class Flavor(db.Model):

    __tablename__ = 'flavors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    flavor_id = db.Column(db.String(100),nullable=False)
    flavor_vcpu = db.Column(db.String(100), nullable=False)
    flavor_ram = db.Column(db.String(100), nullable=False)
    flavor_disk = db.Column(db.String(100), nullable=False)

    def __init__(self, name=None, flavor_id=None, flavor_ram=None, flavor_disk=None,flavor_vcpu=None):
        self.name = name
        self.flavor_id = flavor_id
        self.flavor_ram = flavor_ram
        self.flavor_disk = flavor_disk
        self.flavor_vcpu = flavor_vcpu

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User {0}>'.format(self.name)
