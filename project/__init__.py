import os
import json

from flask import Flask, flash, request, Response
from flask import render_template, jsonify

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

if __name__ == '__main__':
    app.run()
    
from project import core
from project import views
from project import models
