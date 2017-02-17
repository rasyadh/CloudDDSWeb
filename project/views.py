import os, binascii

from functools import wraps
from flask import Flask,flash, request, Response, jsonify, json
from flask import render_template, url_for, redirect, send_from_directory
from flask import send_file, make_response, abort, session

from project import app
from project.core   import db, encrypt
from project.email import send_email
from restapi import keystone as keystoneapi
from restapi import nova as novaapi
from models import *

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

@app.route('/registration',methods=['POST','GET'])
def registration():
    activationcodetmp = ""

    if request.method == 'POST':
        try:
            users = User(
                name=request.form['name'],
                email=request.form['email']+request.form['email_domain'],
                #email=request.form['email']+"@gmail.com",
                #password= encrypt.generate_password_hash(request.form['password']),
                status=0,
                nomorhp=request.form['nomorhp']
            )

            activationcodetmp = binascii.b2a_hex(os.urandom(15))

            activationcode = ActivationCode(
                email_user=request.form['email']+request.form['email_domain'],
                #email_user=request.form['email']+"@gmail.com",
                activationcode=activationcodetmp,
                
            )

            db.session.add(users)
            db.session.add(activationcode)
            db.session.commit()

            confirm_url = "localhost:5000/registration/activate_account?actemp="+activationcodetmp
            html = render_template('activation.html',confirm_url = confirm_url)
            subject = "Please confirm your email"
            #send_email(users.email,subject,html)
            send_email("gravpokemongo@gmail.com",subject,html)

            return redirect(url_for('registration')) 
        
        except:
            return "gagal"

    return render_template('signup.html')

@app.route('/registration/')
def registrationred():
    return redirect(url_for('registration'))


@app.route('/login',methods=['GET','POST'])
@login_required
def login():
    errormsg = []
    
    if request.method == 'POST' :
        try:
            users = User.query.filter_by(email=request.form['email']+request.form['email_domain']).first()
            #users = User.query.filter_by(email=request.form['email']+"@gmail.com").first()

            if users is None :
                errormsg = "Email tidak terdaftar"
                print(errormsg)
                return render_template('login.html', errormsg=errormsg)
            else :
                if users.status == 0:
                    errormsg = "Akun anda belum terverifikasi"
                    print(errormsg)
                else:
                    if encrypt.check_password_hash(users.password,request.form['password']) :
                        return redirect(url_for('manage'))
                    else :
                        errormsg = "Password mu salah"
                        print(errormsg)
                        return render_template('login.html', errormsg=errormsg)

        except:
            return "gagal"

    return render_template('login.html')

@app.route('/registration/activate_account',methods=["GET","POST"])
def activate_account():
    codetemp = []
    
    if request.method == 'POST':
        if request.form['actemp'] is None :
            return redirect(url_for('login'))
        else :
            try:
                activationcode = ActivationCode.query.filter_by(activationcode=request.form['actemp']).first()
                users = User.query.filter_by(email=request.form['email']).first()
                users.status = 1
                users.password = encrypt.generate_password_hash(request.form['password'])
                db.session.delete(activationcode)
                db.session.commit()
                return redirect(url_for('login'))
            
            except:
                return "gagal"
    else:
        activation_code = request.args.get('actemp')
        activationcode = ActivationCode.query.filter_by(activationcode=activation_code).first()
        if activationcode is None:
            return "kode tidak ditemukan"
        else :
            users = User.query.filter_by(email=activationcode.email_user).first()
            return render_template('verifikasi.html',codetemp=activationcode.activationcode,users=users)

@app.route('/registration/activate_account/<activation_code>/')
def activation_accountred(activation_code):
    return redirect(url_for('activate_account'))

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

@app.route('/manage/request')
def request_flav():
    return render_template('request.html')

@app.route('/manage/instance')
def manage_instance():
    return render_template('manage-instance.html')

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