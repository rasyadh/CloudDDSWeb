import os, binascii

from functools import wraps
from flask import Flask,flash, request, Response, jsonify, json
from flask import render_template, url_for, redirect, send_from_directory
from flask import send_file, make_response, abort, session

from project import app
from project.core   import db, encrypt
from project.email import send_email
from restapi.keystone import keystone as keystoneapi
from restapi.nova import nova as novaapi
from restapi.neutron import neutron as neutronapi
from restapi.glance import glance as glanceapi
from models import *

#login session handler
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args,**kwargs)
        else:
            abort(403)
    return wrap

# Client Side

@app.route('/')
def index():
    return render_template('partials/content.html')

@app.route('/registration',methods=['POST','GET'])
def registration():
    activationcodetmp = ""
    errormsg = []


    if request.method == 'POST':
        users = User.query.filter_by(email=request.form['email']+request.form['email_domain']).first()

        if users is not None :
            errormsg = "Email telah terdaftar"

        else:
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

                return redirect(url_for('login'))

            except:
                errormsg = "Terdapat kesalahan pada sistem"
                return render_template('signup.html',errormsg=errormsg)

    return render_template('signup.html',errormsg=errormsg)

@app.route('/registration/')
def registrationred():
    return redirect(url_for('registration'))

@app.route('/login',methods=['GET','POST'])
def login():
    errormsg = []

    if request.method == 'POST' :
        try:
            users = User.query.filter_by(email=request.form['email']+request.form['email_domain']).first()

            if users is None :
                errormsg = "Email Tidak Terdaftar"

            else :
                if users.status == 0:
                    errormsg = "Akun Anda Belum TERVERIFIKASI"

                else:
                    if encrypt.check_password_hash(users.password,request.form['password']) :
                        session['logged_in'] = True
                        session['email'] = users.email
                        return redirect(url_for('manage'))

                    else :
                        errormsg = "Password Anda Salah !"

        except:
            return "Gagal bos"

    return render_template('login.html',errormsg=errormsg)

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
    session.pop('logged_in',None)
    session.pop('email',None)
    return redirect(url_for('index'))

@app.route('/layanan')
def layanan():
    return render_template('partials/layanan.html')

@app.route('/bantuan')
def bantuan():
    return render_template('partials/bantuan.html')

@app.route('/manage')
@login_required
def manage():
    return redirect(url_for('computes'))

@app.route('/manage/computes')
@login_required
def computes():
    email = session['email']
    users = User.query.filter_by(email=email).first()
    return render_template('computes.html',users=users)

@app.route('/manage/create', methods=['GET','POST'])
@login_required
def create_instance():

    if request.method == 'POST':
        return "oke"

    else:        
        email = session['email']
        users = User.query.filter_by(email=email).first()
        nova = novaapi()
        glance = glanceapi()
        flavorJSON = nova.flavorList(0)
        flavorJSON = json.loads(flavorJSON)
        keyJSON = nova.keyList("yj34f8r7j34t79j38jgygvf3")
        keyJSON = json.loads(keyJSON)
        imageJSON = glance.imageList("yj34f8r7j34t79j38jgygvf3")
        imageJSON = json.loads(imageJSON)
        return render_template('create-instance.html',flavorlist = flavorJSON,keylist=keyJSON,imagelist=imageJSON,users=users)
    #return str(respJSON['flavors'])

@app.route('/manage/images')
@login_required
def images():
    email = session['email']
    users = User.query.filter_by(email=email).first()
    return render_template('images.html',users=users)

@app.route('/manage/network')
@login_required
def network():
    email = session['email']
    users = User.query.filter_by(email=email).first()
    return render_template('network.html',users=users)

@app.route('/manage/settings',methods=["GET","POST"])
@login_required
def settings():
    message = []
    email = session['email']
    users = User.query.filter_by(email=email).first()

    if request.method == 'POST':
        if 'updateprofile' in request.form.values():
            if encrypt.check_password_hash(users.password,request.form['password']) :
                users.name = request.form['name']
                users.nomorhp = request.form['phone-number']
                db.session.commit()
                message = "Data berhasil dirubah"

            else:
                message = "Password anda salah"

        elif 'changepassword' in request.form.values():
            if encrypt.check_password_hash(users.password,request.form['old-password']) :
                 users.password = encrypt.generate_password_hash(request.form['confirm-password'])
                 db.session.commit()
                 message = "Password telah berubah"
                 
            else:
                 message = "Password anda salah"

    return render_template('settings.html',users=users,message=message)

@app.route('/manage/request')
@login_required
def request_flav():
    email = session['email']
    users = User.query.filter_by(email=email).first()
    return render_template('request.html',users=users)

@app.route('/manage/instance')
def manage_instance():
    email = session['email']
    users = User.query.filter_by(email=email).first()
    return render_template('manage-instance.html',users=users)

@app.route('/admin')
@app.route('/admin/manage')
def admin_page():
    return redirect(url_for('manage_resource'))

@app.route('/admin/manage-resource')
def manage_resource():
    return render_template('managing-resource.html')

@app.route('/admin/manage-user')
def manage_user():
    return render_template('managing-user.html')

@app.route('/admin/manage-vm')
def manage_vm():
    return render_template('managing-vm.html')

# error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(403)
def page_login_required(e):
    return render_template('login-required.html'),403

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

@app.route('/restapi/nova/server/create')
@app.route('/restapi/nova/server/create/')
def serverCreate():
    nova = novaapi()
    name = "Tes-Web"
    imageRef = "04e2143e-a72a-4157-b744-0ae1c48377b1"
    flavorRef = "2"
    key_name = "fatih-debian"
    networks_uuid = "4740af3d-582e-432f-9286-92b9c943e1cf"
    availability_zone = "nova"

    respJSON = nova.serverCreate(name,imageRef,flavorRef,availability_zone,key_name,networks_uuid)


    return respJSON

@app.route('/restapi/nova/server/list')
@app.route('/restapi/nova/server/list/')
def serverList():
    nova = novaapi()
    respJSON = nova.serverList()


    return respJSON

@app.route('/restapi/nova/flavorlist')
@app.route('/restapi/nova/flavorlist/')
def flavorlist():
    nova = novaapi()
    respJSON = nova.flavorList(0)
    #resp = json.loads(respJSON)

    return respJSON

@app.route('/restapi/nova/flavorlist/<flavor_id>')
@app.route('/restapi/nova/flavorlist/<flavor_id>/')
def flavorlistdetail(flavor_id):
    flavorid = flavor_id
    nova = novaapi()
    respJSON = nova.flavorList(str(flavorid))

    return str(respJSON)

@app.route('/restapi/nova/imagelist')
@app.route('/restapi/nova/imagelist/')
def imagelist():
    nova = novaapi()
    respJSON = nova.imageList(0)
    #resp = json.loads(respJSON)

    return respJSON

@app.route('/restapi/glance/imagelist')
@app.route('/restapi/glance/imagelist/')
def gimagelist():
    glance = glanceapi()
    respJSON = glance.imageList("yj34f8r7j34t79j38jgygvf3")
    #resp = json.loads(respJSON)

    return respJSON

@app.route('/restapi/nova/keylist')
@app.route('/restapi/nova/keylist/')
def keylist():
    nova = novaapi()
    respJSON = nova.keyList("yj34f8r7j34t79j38jgygvf3")


    return respJSON

@app.route('/restapi/nova/keylist/<key_name>')
@app.route('/restapi/nova/keylist/<key_name>/')
def keylistdetail(key_name):
    nova = novaapi()
    respJSON = nova.keyList(key_name)

    return str(respJSON)

@app.route('/restapi/nova/keylist/delete',methods=["GET"])
def keylistdelete():
    if request.method == "GET":
        if request.args.get('keyname') is None:
            return "Bad Parameter"
        else:
            key_name = request.args.get('keyname')
            nova = novaapi()
            respJSON = nova.keyDel(key_name)
            #resp = json.loads(respJSON)

            return redirect(url_for('keylist'))
    else:
        return "Bad Request"

@app.route('/restapi/nova/keylist/new',methods=["GET"])
def keylistnew():
    if request.method == "GET":
        if request.args.get('keyname') is None:
            return "Bad Parameter"
        else:
            key_name = request.args.get('keyname')
            nova = novaapi()
            respJSON = nova.keyNew(key_name)
            resp = json.loads(respJSON)
            #pk = resp['keypair']['private_key'].replace("\n","<br>")
            pk = resp['keypair']['private_key']
            r = Response(response=pk, status=200, mimetype="text/plain")
            r.headers["Content-Type"] = "text/plain; charset=utf-8"
            r.headers["Content-Disposition"] = "attachment; filename="+ key_name +".pem"
            return r
    else:
        return "Bad Request"

@app.route('/restapi/nova/netlist')
@app.route('/restapi/nova/netlist/')
def netlist():
    nova = novaapi()
    respJSON = nova.netList("yj34f8r7j34t79j38jgygvf3")
    #resp = json.loads(respJSON)

    return respJSON

@app.route('/restapi/neutron/floatiplist')
@app.route('/restapi/neutron/floatiplist/')
def floatiplist():
    neutron = neutronapi()
    respJSON = neutron.floatipList("yj34f8r7j34t79j38jgygvf3")
    #resp = json.loads(respJSON)

    return respJSON


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path,'static'),'favicon.png')
