from flask import Flask, render_template, request
import paramiko, time
from sqlite_ex import Base, Device
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json

engine = create_engine('sqlite:///sqlalchemy_example.db')
Base.metadata.bind = engine

DBSession = sessionmaker()
DBSession.bind = engine
#session = DBSession()


app = Flask(__name__)

@app.route("/", methods = ['POST','GET'])
def home():
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
    
if __name__ == "__main__":
    app.run(debug=True)