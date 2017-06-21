from __future__ import print_function 
from flask import Flask, request, redirect, render_template
from flask_mysqldb import MySQL
import sys

# Create connection with MySQL
mysql = MySQL()

# Create Flask app
app = Flask(__name__)

# Set user, password, database, and host
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'dbswldud'
app.config['MYSQL_DB'] = 'MentalHealth'
app.config['MYSQL_HOST'] = 'localhost'
mysql = MySQL(app)

# Route for getting the result of a query
@app.route('/')
def index():
	cur = mysql.connection.cursor()
	cur.execute('''SELECT * FROM MentalHealth.category_description WHERE description = "sleep"''')
	rv = cur.fetchall()
	return str(rv)

# Route for form with the button 
@app.route('/result', methods=['POST', 'GET'])
def result():
	return render_template('button.html')

# Route after the button is clicked
@app.route('/afterbutton')
def afterButton():
	value = request.args.get('mybutton')
	print(value, file=sys.stderr)
	cur = mysql.connection.cursor()
	cur.execute('''SELECT * FROM MentalHealth.category_description WHERE description = %s''', (value,))
	rv = cur.fetchall()
	return str(rv)

# Main
if __name__ == "__main__":
	app.run(debug=True)


