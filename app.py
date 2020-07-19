from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()
 
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


@app.route("/home")
def home():
    return render_template('home.html')

	
if __name__ == "__main__":
    app.run()