import os

from functools import wraps
from flask import Flask,flash, request, Response
from flask import render_template, url_for, redirect, send_from_directory
from flask import send_file, make_response, abort, session

from project import app

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

#@app.route('/static/<path:filanename>')
#def img(filename):
 #   return send_from_directory(img,filename,as_attachment=)

# error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404
