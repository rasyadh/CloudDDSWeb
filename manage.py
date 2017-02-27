import os

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from project import app
from project.core import db, encrypt
from project.models import User

migrate = Migrate(app,db)
manager = Manager(app)

manager.add_command('db',MigrateCommand)

@manager.command
def createdb():
	db.create_all()

@manager.command
def create_superadmin():
	admin = User(name = 'Super Admin', email='superadmin@telkom.co.id',password=encrypt.generate_password_hash("superadmintelkom"), status=1, nomorhp="081618129", role=2)
	db.session.add(admin)
	db.session.commit()

@manager.command
def create_admincnp():
	admin = User(name = 'Admin CNP', email='admincnp@telkom.co.id',password=encrypt.generate_password_hash("admintelkom"), status=1, nomorhp="081234567", role=1)
	db.session.add(admin)
	db.session.commit()

@manager.command
def create_adminoasis():
	admin = User(name = 'Admin OASIS', email='adminoasis@telkom.co.id',password=encrypt.generate_password_hash("admintelkom"), status=1, nomorhp="081234567", role=1)
	db.session.add(admin)
	db.session.commit()

@manager.command
def create_user():
	user = User(name = 'User Biasa', email='user@telkom.co.id',password=encrypt.generate_password_hash("usertelkom"),status=1,nomorhp="0812691299")
	db.session.add(user)
	db.session.commit()


if __name__ == '__main__':
	manager.run()
