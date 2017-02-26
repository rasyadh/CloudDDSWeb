import os
import json

from flask import Flask, flash, request, Response,url_for
from flask import render_template, jsonify
import config
APP_SETTINGS = config.DevelopmentConfig

app = Flask(__name__)

#use this for windows
app.config.from_object(APP_SETTINGS)
myDOMAIN = APP_SETTINGS.domain_url
#use this for linux
#app.config.from_object(os.environ['APP_SETTINGS'])

if __name__ == '__main__':
    app.run(threaded=True)

from project import core
from project import views
from project import models
