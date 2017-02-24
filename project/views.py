import os, binascii, time

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
def login_required(login):
    @wraps(login)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return login(*args,**kwargs)
        else:
            abort(403)
    return wrap

def admin_required(admin):
    @wraps(admin)
    def wrap(*args, **kwargs):
        if 'admin_in' in session:
            return admin(*args,**kwargs)
        else:
            return redirect(url_for('index'))
    return wrap

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    session.pop('admin_in',None)
    session.pop('user_id',None)
    session.pop('admin_id',None)
    return redirect(url_for('index'))

# Client Side --- USER

@app.route('/')
def index():
    return render_template('partials/content.html')

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

                elif users.status == 1:
                    if encrypt.check_password_hash(users.password,request.form['password']) and users.role == 0:
                        session['logged_in'] = True
                        session['user_id'] = users.id
                        return redirect(url_for('manage'))

                    elif encrypt.check_password_hash(users.password,request.form['password']) and users.role == 1:
                        session['admin_in'] = True
                        session['admin_id'] = users.id
                        return redirect(url_for('admin_page'))

                    else :
                        errormsg = "Password Anda Salah !"

                elif users.status == 2:
                    errormsg = "Akun anda telah di SUSPEND, silahkan hubungi administrator untuk hal ini."

                elif users.status == 3:
                    errormsg = "Akun anda telah di BLACKLIST karena penggunaan ilegal pada layanan."

        except:
            return "Gagal bos"

    return render_template('login.html',errormsg=errormsg)

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
                activationcode = Token(
                    email_user=request.form['email']+request.form['email_domain'],
                    #email_user=request.form['email']+"@gmail.com",
                    code=activationcodetmp,type=0

                )

                db.session.add(users)
                db.session.add(activationcode)

                confirm_url = "http://localhost:5000/registration/activate_account?actemp="+activationcodetmp
                html = render_template('email/verification-email.html',confirm_url = confirm_url)
                subject = "Verification Email Cloud Telkom DDS"
                #send_email(users.email,subject,html)
                send_email("gravpokemongo@gmail.com",subject,html)
                db.session.commit()

                return redirect(url_for('login'))

            except:
                errormsg = "Terdapat kesalahan pada sistem"
                return render_template('signup.html',errormsg=errormsg)

    return render_template('signup.html',errormsg=errormsg)

def registrationred():
    return redirect(url_for('registration'))

@app.route('/registration/activate_account',methods=["GET","POST"])
def activate_account():
    codetemp = []

    if request.method == 'POST':
        if request.form['actemp'] is None :
            abort(404)

        else :
            try:
                activationcode = Token.query.filter_by(code=request.form['actemp']).first()
                users = User.query.filter_by(email=request.form['email']).first()
                users.status = 1
                users.password = encrypt.generate_password_hash(request.form['password'])
                db.session.delete(activationcode)
                db.session.commit()
                return redirect(url_for('login'))

            except:
                abort(404)

    else:
        activation_code = request.args.get('actemp')
        activationcode = Token.query.filter_by(code=activation_code).first()
        if activationcode is None:
            abort(404)
        else :
            users = User.query.filter_by(email=activationcode.email_user).first()
            return render_template('verifikasi.html',codetemp=activationcode.code,users=users)

@app.route('/registration/activate_account/<activation_code>/')
def activation_accountred(activation_code):
    return redirect(url_for('activate_account'))

#Check halaman verifikasi forgot password
@app.route('/forgot_password',methods=["GET","POST"])
def forgot_password():

    message = []
    if request.method == 'POST':
        users = User.query.filter_by(email=request.form['email']+request.form['email_domain']).first()
        if users is None :
            message = 'Email tidak ditemukan'

        else:
            token = binascii.b2a_hex(os.urandom(15))
            forgot_token = Token(
                email_user=request.form['email']+request.form['email_domain'],
                code=token,type=1
            )
            message = 'Request reset password telah dikirim'
            db.session.add(forgot_token)
            db.session.commit()

            confirm_url = "http://localhost:5000/forgot_password/reset_password?tokens="+token
            html = render_template('email/resetpass-email.html',confirm_url = confirm_url, users=users)
            subject = "Request Reset Password Cloud Telkom DDS"
            #send_email(users.email,subject,html)
            send_email("gravpokemongo@gmail.com",subject,html)
    return render_template('forgot-password.html')

@app.route('/forgot_password/')
def forgotredirect():
    return redirect(url_for('forgot_password'))

@app.route('/forgot_password/reset_password',methods=['GET','POST'])

def reset_pass():
    if request.method == 'POST':
        if request.form['tokens'] is None :
            abort(404)

        else :
            try:
                tokens = Token.query.filter_by(code=request.form['tokens']).first()
                users = User.query.filter_by(email=request.form['email']).first()

                users.password = encrypt.generate_password_hash(request.form['confirm_new_password'])
                db.session.delete(tokens)
                db.session.commit()
                return redirect(url_for('login'))

            except:
                abort(404)

    else:
        token = request.args.get('tokens')
        resetauth = Token.query.filter_by(code=token).first()
        if resetauth is None:
            abort(404)

        else :
            users = User.query.filter_by(email=resetauth.email_user).first()
            return render_template('verifikasi-forgotpass.html',reset=resetauth,users=users)

@app.route('/forgot_password/reset_password/<tokens>/')
def reset_passred(tokens):
    return redirect(url_for('reset_pass'))
<<<<<<< HEAD

@app.route('/layanan')
=======

@app.route('/layanan')
>>>>>>> 0211f1d9a7c43de0597de40e4030886d47058cab
def layanan():
    return render_template('partials/layanan.html')

@app.route('/bantuan')
def bantuan():
    return render_template('partials/bantuan.html')

@app.route('/manage')
@app.route('/manage/')
@login_required
def manage():
    return redirect(url_for('computes'))

@app.route('/manage/computes')
@login_required
def computes():
    users = User.query.filter_by(id=session['user_id']).first()
    serverreq = Request.query.filter_by(owner_id=session['user_id']).order_by(Request.status).all()

    return render_template('computes.html',users=users, serverreq=serverreq)    

@app.route('/manage/create', methods=['GET','POST'])
@login_required
def create_instance():
    nova = novaapi()
    glance = glanceapi()
    neutron = neutronapi()

    if request.method == 'POST':
        #try:
            imageRef = request.form['imageRef']
            flavorRef = str(request.form['flavorRef'])
            size = request.form['size']
            availability_zone = request.form['availability_zone']
            networks_uuid = "417b4cdd-b706-4f6c-8e6e-1b06f58e94c8"
            key_name = request.form['key_name']
            name = request.form['name']
            respJSON = nova.serverCreate(name,imageRef,flavorRef,availability_zone,key_name,networks_uuid,size)

            # time.sleep(30)
            # resp = json.loads(respJSON)
            # server_id = resp['server']['id']
            # respJSON = nova.serverList(server_id)
            # resp = json.loads(respJSON)
            # for addresses in resp['server']['addresses']['private']:
            #     if addresses["version"] == 4:
            #         private_ip = addresses["addr"]
            #         break
            # respJSON = neutron.floatipList()
            # respJSON = json.loads(respJSON)
            # iplist = respJSON['floatingips']
            # for ip in iplist:
            #     if ip['fixed_ip_address'] is Null:
            #         public_ip = ip['floating_ip_address']
            #         break
            # nova.setFloatingIp(private_ip,public_ip,server_id)

            req = Request(
                    name = name,
                    image_id = imageRef,
                    flavor_id = flavorRef,
                    network_id = networks_uuid,
                    availability_zone = availability_zone,
                    keyname = key_name,
                    purpose = request.form['purpose'],
                    pic_name = request.form['pic_name'],
                    pic_telp = request.form['pic_telp'],
                    status = 0
                )

            db.session.add(req)
            db.session.commit()

            return redirect(url_for('computes'))
        #except:
            #return "Bad Parameter"
    else:
        users = User.query.filter_by(id=session['user_id']).first()
        #ubahteko baris iki
        flavorJSON = nova.flavorList(0)
        flavorJSON = json.loads(flavorJSON)
        keyJSON = nova.keyList("yj34f8r7j34t79j38jgygvf3")
        keyJSON = json.loads(keyJSON)
        imageJSON = nova.imageList(0)
        imageJSON = json.loads(imageJSON)
        return render_template('create-instance.html',flavorlist = flavorJSON,keylist=keyJSON,imagelist=imageJSON,users=users)
    #return str(respJSON['flavors'])

@app.route('/manage/images')
@login_required
def images():
    users = User.query.filter_by(id=session['user_id']).first()
    return render_template('images.html',users=users)

@app.route('/manage/network')
@login_required
def network():
    users = User.query.filter_by(id=session['user_id']).first()
    return render_template('network.html',users=users)

@app.route('/manage/settings',methods=["GET","POST"])
@login_required
def settings():
    message = []
    users = User.query.filter_by(id=session['user_id']).first()

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

        elif 'deactivate' in request.form.values():
            users.status = 2
            db.session.commit()
            message = "Account telah diaktifasi"

    return render_template('settings.html',users=users,message=message)

@app.route('/manage/request')
@login_required
def request_flav():
    users = User.query.filter_by(id=session['user_id']).first()
    return render_template('request.html',users=users)

@app.route('/manage/instance')
def manage_instance():
    users = User.query.filter_by(id=session['user_id']).first()
    return render_template('manage-instance.html',users=users)

# Client Side --- ADMIN
@app.route('/admin')
@app.route('/admin/')
@app.route('/admin/manage')
@admin_required
def admin_page():
    return redirect(url_for('manage_resource'))

@app.route('/admin/manage-resource')
@admin_required
def manage_resource():
    admin = User.query.filter_by(id=session['admin_id']).first()
    return render_template('admin/managing-resource.html',admin=admin)

@app.route('/admin/manage-user',methods=['GET','POST'])
@admin_required
def manage_user():
    admin = User.query.filter_by(id=session['admin_id']).first()
    allusers = User.query.filter_by(role=0).all()
    if request.method == 'POST':
        if request.form['action'] == "activate" :
            users = User.query.filter_by(id=request.form['users-id']).first()
            users.status = 1
            db.session.commit()
        elif request.form['action'] == "suspend":
            users = User.query.filter_by(id=request.form['users-id']).first()
            users.status = 2
            db.session.commit()
        elif request.form['action'] == "delete":
            users = User.query.filter_by(id=request.form['users-id']).first()
            users.status = 3
            db.session.commit()
    return render_template('admin/managing-user.html',admin=admin,allusers=allusers)

@app.route('/admin/manage-vm')
@admin_required
def manage_vm():
    admin = User.query.filter_by(id=session['admin_id']).first()
    return render_template('admin/managing-vm.html',admin=admin)

@app.route('/admin/manage-admin')
@admin_required
def manage_admin():
    admin = User.query.filter_by(id=session['admin_id']).first()
    return render_template('admin/managing-admin.html',admin=admin)

# error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'),404

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
    imageRef = "2efaef5b-13d2-439b-bb55-a6e4a3878c2d"
    flavorRef = "2"
    key_name = "aziz"
    networks_uuid = "5eb3b761-4a8e-41b3-a512-b0d9e349f743"
    availability_zone = "nova"

    respJSON = nova.serverCreate(name,imageRef,flavorRef,availability_zone,key_name,networks_uuid)


    return respJSON

@app.route('/restapi/nova/server/list')
@app.route('/restapi/nova/server/list/')
def serverList():
    nova = novaapi()
    respJSON = nova.serverList()

    return respJSON

@app.route('/restapi/nova/server/list/<server_id>')
@app.route('/restapi/nova/server/list/<server_id>/')
def serverListDetail(server_id):
    nova = novaapi()
    respJSON = nova.serverList(server_id)


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

            if resp['status'] is True:
                #pk = resp['keypair']['private_key'].replace("\n","<br>")
                resp = resp['content']
                resp = json.loads(resp)
                pk = resp['keypair']
                r = Response(response=pk, status=200, mimetype="text/plain")
                r.headers["Content-Type"] = "text/plain; charset=utf-8"
                r.headers["Content-Disposition"] = "attachment; filename="+ key_name +".pem"
                return r
            else:
                return resp['content']['conflictingRequest']['message']

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
