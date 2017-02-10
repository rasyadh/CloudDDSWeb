import os

from functools import wraps
from flask import Flask,flash, request, Response, jsonify, json
from flask import render_template, url_for, redirect, send_from_directory
from flask import send_file, make_response, abort, session

from project import app
from restapi.keystone import keystone as keystoneapi
from restapi.nova import nova as novaapi

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args,**kwargs)
        else:
            flash('You need to login first')
            return redirect(url_for('login'))
    return wrap


@app.route('/')
def index():
    session['logged_in']=True
    return render_template('index.html')

@app.route('/registration')
def registration():
    return render_template('signup.html')

@app.route('/login')
@login_required
def login():
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in')
    return "logout PAGE"

@app.route('/layanan')
def layanan():
    return render_template('layanan.html')

@app.route('/bantuan')
def bantuan():
    return render_template('bantuan.html')

@app.route('/about')
def about():
    return "about PAGE"

@app.route('/restapi/keystone')
@app.route('/restapi/keystone/')
def keystone(): 
    keystone = keystoneapi()
    respJSON = keystone.myRequest()

    return respJSON

@app.route('/restapi/nova')
@app.route('/restapi/nova/')
def nova():
    nova = novaapi()
    url = nova.getUrl()

    return url

@app.route('/restapi/nova/flavorlist')
@app.route('/restapi/nova/flavorlist/')
def flavorlist():
    nova = novaapi()
    respJSON = nova.flavorList(0)
    #resp = json.loads(respJSON)
    
    return str(respJSON)

@app.route('/restapi/nova/flavorlist/<flavor_id>')
def flavorlistdetail(flavor_id):
    flavorid = flavor_id
    nova = novaapi()
    respJSON = nova.flavorList(str(flavorid))

    return str(respJSON)

# error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404