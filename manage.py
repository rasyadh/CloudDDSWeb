import os

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from project import app
from project.core import db

app.config.from_object(os.environ['APP_SETTINGS'])

#migrate = Migrate(app,db)
manager = Manager(app)

#manager.add_command('db',MigrateCommand)

@manager.command
def createdb():
	db.create_all()

manager.run()