from __future__ import print_function 
from flask import Flask, request, redirect, render_template
from flask_mysqldb import MySQL
import sys

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

@app.route('/result', methods=['POST', 'GET'])
def result():
	return render_template('button.html')
	# print("in function")
	# print(request.form)
	# print(request.form['click'])
	# return redirect('/')
	
	# if request.form['clicked'] == "ON":
	# 	print("yes")
	# elif request.form['clicked'] == "OFF":
	# 	print("no")
@app.route('/afterbutton')
def yes():
	# print("YES", file=sys.stderr)
	# return "YES"
	#return redirect('/')
	value = request.args.get('mybutton')
	print(value, file=sys.stderr)
	cur = mysql.connection.cursor()
	# cur.execute('''SELECT * FROM MentalHealth.category_description WHERE description = ''' + str(value))
	# # line = '''SELECT * FROM MentalHealth.category_description WHERE category_ID = 111'''
	cur.execute('''SELECT * FROM MentalHealth.category_description WHERE description = %s''', (value,))
	# query = "SELECT * FROM MentalHealth.category_description WHERE description = (?)"
	# cur.execute("SELECT * FROM MentalHealth.category_description WHERE description = (?)", value)
	rv = cur.fetchall()
	return str(rv)



if __name__ == "__main__":
	app.run(debug=True)


