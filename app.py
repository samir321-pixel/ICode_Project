from flask import Flask, render_template, request
import os

app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


local_server = True
app.secret_key = 'super secret-key'
import json

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

app.config['UPLOAD_FOLDER'] = params['upload_location']

db = SQLAlchemy(app)


class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)


class Createpost(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    ctitle = db.Column(db.String(12), nullable=True)
    ctag = db.Column(db.String(12), nullable=True)
    clink = db.Column(db.String(120), nullable=False)
    cdes = db.Column(db.String(120), nullable=True)
    cimage = db.Column(db.String(12), nullable=True)
    suggestion = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/terms')
def terms():
    return render_template('test.html')


@app.route('/about_me')
def about_me():
    return render_template('about.html')


@app.route('/codecademy')
def codecademy():
    return render_template('codecademy.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    submit = False
    if (request.method == 'POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name=name, phone=phone, message=message, date=datetime.now(), email=email)
        db.session.add(entry)
        db.session.commit()
        submit = True
    return render_template('contact.html', params=params, submit=submit)


@app.route('/createpost', methods=['GET', 'POST'])
def createpost():
    submit = False

    if (request.method == 'POST'):
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        ctitle = request.form.get('ctitle')
        ctag = request.form.get('ctag')
        clink = request.form.get('clink')
        cdes = request.form.get('cdes')
        cimage = request.form.get('cimage')
        if request.files:
            cimage1 = request.files['cimage']
            #cimage1 = secure_filename(cimage)
            cimage1.save(os.path.join(app.config['UPLOAD_FOLDER'],cimage1.filename))
            print("Image saved")
        suggestion = request.form.get('suggestion')
        entry = Createpost(name=name, phone=phone, email=email, ctitle=ctitle, cimage=cimage, date=datetime.now(),
                           ctag=ctag,
                           clink=clink, cdes=cdes,
                           suggestion=suggestion)
        db.session.add(entry)
        db.session.commit()
        submit = True
    return render_template('createpost.html', params=params, submit=submit)




if __name__ == '__main__':
    app.run(debug=True)
