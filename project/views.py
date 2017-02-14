import os

from functools import wraps
from flask import Flask,flash, request, Response, jsonify, json
from flask import render_template, url_for, redirect, send_from_directory
from flask import send_file, make_response, abort, session

from project import app
from restapi import keystone as keystoneapi
from restapi import nova as novaapi

# Client Side

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
    return render_template('partials/content.html')

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
    return render_template('partials/layanan.html')

@app.route('/bantuan')
def bantuan():
    return render_template('partials/bantuan.html')

@app.route('/manage')
def manage():
    return redirect(url_for('computes'))

@app.route('/manage/computes')
def computes():
    return render_template('computes.html')

@app.route('/manage/create')
def create_instance():
    return render_template('create-instance.html')

@app.route('/manage/images')
def images():
    return render_template('images.html')

@app.route('/manage/network')
def network():
    return render_template('network.html')

@app.route('/manage/settings')
def settings():
    return render_template('settings.html')

# error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

# back-end side

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


'''
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path,'static'),'favicon.png')
    '''