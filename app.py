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
import Mail,  Message
 



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
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

engine = create_engine('sqlite:///sqlalchemy_example.db',connect_args={'check_same_thread': False})
DBSession = sessionmaker(bind=engine)
session = DBSession()

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    is_admin = db.Column(db.String(1),nullable = False)
    first_name = db.Column(db.String(250),nullable = False)
    last_name = db.Column(db.String(250),nullable = False)
    username = db.Column(db.String(15), unique=False)
    email = db.Column(db.String(50), unique=False)
    password = db.Column(db.String(80))


class Device(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    series = db.Column(db.String(50),nullable = False)
    software_version = db.Column(db.String(250),nullable = False)

class DeviceAssociation(db.Model):

    id = db.Column(db.Integer,primary_key = True)
    ip = db.Column(db.String(50),nullable = False)
    endpoint_name = db.Column(db.String(250),nullable = False)
    software_version = db.Column(db.String(250),nullable = False)
    owner = db.Column(db.String(250),nullable = False)
    registered_to = db.Column(db.String(250),nullable = False)
    status = db.Column(db.String(250),nullable = False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    first_name = StringField('first_name', validators=[InputRequired(), Length(max=50)]) 
    last_name = StringField('last_name', validators=[InputRequired(), Length(max=50)]) 
    is_admin = StringField('is_admin', validators=[InputRequired(), Length(max=50)]) 

#class DeviceAssociationForm(FlaskForm):
#    ip = StringField('ip', validators=[InputRequired(), Length(max=50)])
#    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
#    password = StringField('password')
   
class DeviceForm(FlaskForm):

    series = QuerySelectField(query_factory=lambda: session.query(Device).all(), get_label="series")
    software_version = StringField('software_version', validators=[InputRequired(), Length(min=8, max=80)])

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

   

        
   
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])

def signup():

    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(is_admin=form.is_admin.data , first_name=form.first_name.data, last_name=form.last_name.data, username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)

#@app.route('/add_endpoint')
#@login_required
#def add_endpoint():
 #   return render_template('add_endpoint.html', name=current_user.username)


@app.route('/dashboard')
@login_required
def dashboard():
    engine = create_engine('sqlite:///sqlalchemy_example.db',connect_args={'check_same_thread': False})
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    device_association = session.query(DeviceAssociation).all()
    return render_template('dashboard.html', name=current_user.username , device_association = device_association)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/addSwPage', methods = ['POST','GET'])
@login_required
def addSwPage():
    engine = create_engine('sqlite:///sqlalchemy_example.db',connect_args={'check_same_thread': False})
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    device = session.query(Device).all()

    #for populating drop-down
    test_list = []
    for i in device:
        test_list.append((i.series,i.software_version))
    d = {}
    for a,b in test_list:
        d.setdefault(a,[]).append(b)

    y = json.dumps(d)



    form = DeviceForm()


    if form.validate_on_submit():

        new_device=Device(series= form.series.data.series, software_version= form.software_version.data)
        db.session.add(new_device)
        db.session.commit()

        return '<h1>New sw has been added!</h1>'

    return render_template('addSwPage.html', form=form, device=device , y = y)


@app.route('/addEndpointDetails', methods = ['POST','GET'])
@login_required
def addEndpointDetails():
    #form = DeviceAssociationForm()
    if request.method == 'POST':
        ip = request.form['ip']
        print(ip)
        owner = request.form['owner']
        print(ip)
        username = request.form['username']
        print(username)
        password = request.form['password']
        print(password)
        host = ip
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)
        print("SSH connection established to " + host)
        remote_conn = ssh.invoke_shell()
        print("Interactive SSH session established")
        command = "xstatus SIP Proxy 1 Address"
        remote_conn.send("\n")
        remote_conn.send(command)
        remote_conn.send("\n")
        time.sleep(0.5)
        output1 = remote_conn.recv(10000)
        swr = re.findall(r'\d+.\d+.\d+.\d+', str(output1))
        finalsw=str(swr)
        test1 = finalsw.split(",")[2].strip("['']")
        test1 = test1.replace("'","")
        print(test1) 
        print(output1)
        command = "xstatus SystemUnit Software DisplayName"
        remote_conn.send("\n")
        remote_conn.send(command)
        remote_conn.send("\n")
        time.sleep(0.5)
        output2 = remote_conn.recv(10000)
        swr = re.findall(r'tc|ce\s\d.\d.\d', str(output2))
        finalsw=str(swr)
        test2 = finalsw.strip("['']")
        print(test2) 
        #print(output2)
        command = "xstatus SystemUnit ProductId"
        remote_conn.send("\n")
        remote_conn.send(command)
        remote_conn.send("\n")
        time.sleep(0.5)
        output3 = remote_conn.recv(10000)
        swr = re.findall(r'Cisco\s.*', str(output3))
        finalsw=str(swr)
        test3 = finalsw.split('"')[0].replace("['","")
        print(output3)
        engine = create_engine('sqlite:///sqlalchemy_example.db',connect_args={'check_same_thread': False})
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        new_device_association=DeviceAssociation(ip= ip, endpoint_name= test3,software_version=test2,owner=request.form['owner'],registered_to=test1,status="Active")
        db.session.add(new_device_association)
        db.session.commit()
        return '<h1>POST added!' +ip +username + password + "<br><br><br>" +str(test1) +"<br>"+str(test2)+"<br>"+str(test3)+'</h1>'
    else:
        return '<h1>GET REQUEST</h1>'

@app.route("/upgradePage", methods = ['POST','GET'])
@login_required
def upgradePage():

    engine = create_engine('sqlite:///sqlalchemy_example.db',connect_args={'check_same_thread': False})
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    device = session.query(Device).all()

    test_list = []
    for i in device:
        test_list.append((i.series,i.software_version))
    d = {}
    for a,b in test_list:
        d.setdefault(a,[]).append(b)

    y = json.dumps(d)

    if request.method == 'POST':
        ip = request.form['ip']
        host = ip
        username = request.form['username']
        password = request.form['password']
        sv = request.form['sv']
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)
        print("SSH connection established to " + host)
        remote_conn = ssh.invoke_shell()
        print("Interactive SSH session established")
        command = "xcommand SystemUnit SoftwareUpgrade URL:"+" "+'"http://10.106.118.100:8000/'+sv+'"'+" "+"Forced: True"
        remote_conn.send("\n")
        remote_conn.send(command)
        remote_conn.send("\n")
        #time.sleep(5)
        output = remote_conn.recv(10000)
        print(output)
        return render_template('username.html', username = username , ip = ip , password = password , command = command)
    else:
        return render_template("hometest.html", device = device , y = y, d = d)

if __name__ == '__main__':
    app.run(debug=True)
