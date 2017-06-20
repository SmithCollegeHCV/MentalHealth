from flask import Flask, request, redirect
from flask_mysqldb import MySQL

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'dbswldud'
app.config['MYSQL_DB'] = 'MentalHealth'
app.config['MYSQL_HOST'] = 'localhost'
mysql = MySQL(app)

@app.route('/')
def index():
	cur = mysql.connection.cursor()
	cur.execute('''SELECT * FROM MentalHealth.category_description WHERE description = "sleep"''')
	rv = cur.fetchall()
	return str(rv)

@app.route('/result', methods=['GET', 'POST'])
def result():
	print("in function")
	print(request.form['clicked'])
	# print(request.form['click'])
	# return redirect('/')
	
	if request.form['clicked'] == "ON":
		print("yes")
	elif request.form['clicked'] == "OFF":
		print("no")


if __name__ == "__main__":
	app.run(debug=True)