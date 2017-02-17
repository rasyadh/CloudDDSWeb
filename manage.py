import os

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from project import app
from project.core import db
from project.models import User

#migrate = Migrate(app,db)
manager = Manager(app)

#manager.add_command('db',MigrateCommand)

@manager.command
def createdb():
	db.create_all()

@manager.command
def create_admin():
	admin = User(name = 'Admin', email='admin@telkom.co.id', password="admintelkom", status=1, nomorhp="081234567", role=1)
	db.session.add(admin)
	db.session.commit()

if __name__ == '__main__':
	manager.run()
