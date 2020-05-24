#from my_project import app
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm , Form
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import json
import paramiko, time ,re
import smtplib
from flask_mail import Mail, Message
 



app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlalchemy_example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.config['DEBUG'] = True
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'mail2sunit.om@gmail.com'
app.config['MAIL_PASSWORD'] = 'ikpkzoomoctzuqtn'


mail = Mail(app)



bootstrap = Bootstrap(app)


@app.route('/')
def index():
    

    return render_template('index.html')

@app.route('/sendmail', methods=['GET','POST'])

def sendmail():

        name = request.form['name']
        print(name)
        email = request.form['email']
        print(email)
        phone = request.form['phone']
        print(phone)
        message = request.form['message']
        print(message)
        
        #sender = email
        #receivers = ['mail2sunit.om@gmail.com']

        msg = mail.send_message(
        'You have received an email from ascshipping.co.in',
        sender=email,
        recipients=['mail2sunit.om@gmail.com'],
        body='You have received a quote request from email:'+" "+email+" "+"Phone number:"+phone+" "+"with message:"+message
        )

        msg2 = mail.send_message(
        'Thanks for contacting ascshipping.co.in!',
        sender=email,
        recipients=[email],
        body='Thank you '+" "+name+" "+'for sending us your query. We will get back to you with the quotation soon! In case of urgency you can directly call on +91 6290347722'
        )

        
        #smtpObj = smtplib.SMTP('localhost')
        #smtpObj.sendmail(sender, receivers, message)         
        #print("Successfully sent email")
        return '<h1>Mail Sent!</h1>'



if __name__ == '__main__':
    app.run(debug=True)
