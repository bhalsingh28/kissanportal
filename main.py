from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json
from datetime import datetime


with open('config.json', 'r') as c:
    params = json.load(c)["params"]
local_server = True


app = Flask(__name__)
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USER_NAME = params['gmail-user'],
    MAIL_PASSWORD = params['gmail-password']
)

mail = Mail(app)
if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] =  params['local_url']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_url']
db = SQLAlchemy(app)


class Contacts(db.Model):
    # sno_ , name_ , phone_no_ , msg_ , date_ , email_
    sno_ = db.Column(db.Integer, primary_key=True)
    name_ = db.Column(db.String(80), unique=False, nullable=False)
    phone_no_ = db.Column(db.String(12), unique=True, nullable=False)
    msg_ = db.Column(db.String(120),  nullable=False)
    email_ = db.Column(db.String(20), unique=True, nullable=False)



class Details(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20),unique = False, nullable=False)
    mob_no = db.Column(db.String(14), unique = True, nullable=False)
    addr = db.Column(db.String(20), nullable=False)
    adh_ca = db.Column(db.Integer, unique = True, nullable=False)
    pan = db.Column(db.String(10), unique = True, nullable=False)
    ut_state = db.Column(db.String(30), unique = False, nullable = False)
    cr_name = db.Column(db.String(20), unique = False, nullable=False)
    cr_type = db.Column(db.String(20), unique = False, nullable=False)
    quantity = db.Column(db.Integer, unique = False, nullable=False)


@app.route("/")
def home():
    return render_template("index.html", params=params)


@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if (request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name_=name, phone_no_=phone, msg_=message, email_=email)
        db.session.add(entry)
        db.session.commit()
            # mail.send_message('New message from Blog',
            #                   sender = email,
            #                   recipients = [params['gmail-user']],
            #                   body = message + "\n" +phone)
    return render_template("contact.html", params=params)


@app.route("/sell", methods = ['GET', 'POST'])
def sell():
    if (request.method=='POST'):
        name = request.form.get('name')
        mobile = request.form.get('mobile')
        address = request.form.get('address')
        adhar_card = request.form.get('adhar_card')
        pan_ = request.form.get('pan_')
        ut_state = request.form.get('ut_state')
        crop_name = request.form.get('crop_name')
        crop_type = request.form.get('crop_type')
        quantity = request.form.get('quantity')
        entry = Details(name=name, mob_no=mobile, addr=address, adh_ca=adhar_card, pan=pan_, ut_state=ut_state, cr_name=crop_name, cr_type=crop_type, quantity=quantity)
        db.session.add(entry)
        db.session.commit()

    return render_template("sell.html", params=params)


app.run(debug=True)