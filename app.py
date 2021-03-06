from flask import Flask, render_template, request, json, redirect, session
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

app.secret_key = 'abaaba'
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'covid19DB'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql.init_app(app)

@app.route("/")
def main():
    return render_template('main.html')
	
@app.route("/register")
def register():
    return render_template('register.html')
	
@app.route("/login")
def login():
		return render_template('login.html')
	
@app.route("/doRegistration", methods=['POST'])
def registration():
	_fn = request.form['inputFirstName']
	_ln = request.form['inputLastName']
	_eml = request.form['inputEmail']
	_pwd = request.form['inputPassword']
	_id = request.form['inputId']
	_adrs = request.form['inputAdrs']
	_zc = request.form['inputZip']
	_uniname = request.form['inputUniv']
	_coll = request.form['inputColl']
	
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.callproc('createUser',(_id,_fn,_ln,_eml,_pwd,_adrs,_zc,_uniname,_coll))
	data = cursor.fetchall()
	
	if len(data) == 0:
		conn.commit()
		return json.dumps({'message':'User created successfully!'})
	else:
		return json.dumps({'error':str(data[0])})
	return json.dumps({'html':'<span>Registered</span>'})

@app.route("/doLogin", methods=['POST'])
def logingin():
	_eml = request.form['inputEmail']
	_pwd = request.form['inputPassword']
	
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.callproc('validateLogin', (_eml,))
	tmp = cursor.fetchall()
	if (len(tmp) > 0):
		if tmp[0][3] == _pwd:
			session['user'] = tmp[0][0]
			return redirect('/home')
		else:
			return redirect('/login')
	else:
		return redirect('/login')
	
@app.route("/logout")
def logout():
	session.pop("user", None)
	return redirect('/')

@app.route("/delete")
def delete():
	_eml = session.get('user')
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.callproc('deleteRecords',(_eml,))
	data = cursor.fetchall()
	
	if len(data) == 0:
		conn.commit()
		return redirect('/home')
	else:
		return json.dumps({'error':str(data[0])})
	return json.dumps({'html':'<span>Deleted</span>'})

@app.route("/displaysymptoms")
def displaysymptoms():
	_eml = session.get('user')
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.callproc('getSymptoms',(_eml,))
	data = cursor.fetchall()
	
	symps = []
	for s in data:
		symp_dict = {
			'sympName': s[0]
		}
		symps.append(symp_dict)
		
	return json.dumps(symps)

@app.route("/home")
def home():
		if (session.get('user')):
			return render_template('home.html')
		else:
			return render_template('main.html')

@app.route("/updatesymptoms")
def updatesymptoms():
	return render_template('updateSymptoms.html')

@app.route("/doupdate", methods=['GET','POST'])
def doupdate():
	_s1 = False
	_s2 = False
	_s3 = False
	_s4 = False
	_s5 = False
	_s6 = False
	_s7 = False
	_s8 = False
	_s9 = False
	_s10 = False
	_s11 = False
	if (request.form.get('symptom1') != None):
		_s1 = True
	if (request.form.get('symptom2') != None):
		_s2 = True
	if (request.form.get('symptom3') != None):
		_s3 = True
	if (request.form.get('symptom4') != None):
		_s4 = True
	if (request.form.get('symptom5') != None):
		_s5 = True
	if (request.form.get('symptom6') != None):
		_s6 = True
	if (request.form.get('symptom7') != None):
		_s7 = True
	if (request.form.get('symptom8') != None):
		_s8 = True
	if (request.form.get('symptom9') != None):
		_s9 = True
	if (request.form.get('symptom10') != None):
		_s10 = True
	if (request.form.get('symptom11') != None):
		_s11 = True
	
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.callproc('updateSymptoms',(_s1,_s2,_s3,_s4,_s5,_s6,_s7,_s8,_s9,_s10,_s11,session.get('user')))
	data = cursor.fetchall()
	
	if len(data) == 0:
		conn.commit()
		return redirect('/home')
	else:
		return json.dumps({'error':str(data[0])})
	return json.dumps({'html':'<span>Updated</span>'})
	
	
if __name__ == "__main__":
    app.run(debug=True)