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
	cur.execute('''SELECT * FROM MentalHealth.category_description WHERE category = "sleep"''')
	rv = cur.fetchall()
	return str(rv)

# Route for form with the button 
@app.route('/button', methods=['POST', 'GET'])
def result():
	return render_template('button.html')

# Route after the button is clicked
@app.route('/afterbutton')
def afterButton():
	codeValue = request.args.get('codeButton')
	catValue = request.args.get('catButton')
	cur = mysql.connection.cursor()
	if codeValue: 
		cur.execute('''SELECT code.code, name_description.diagnosis, chapter_description.chapter, symptom_description.symptom 
			FROM code, symptom_description, name_description, chapter_description 
			WHERE code.Index = symptom_description.code_ID AND code.Index = name_description.code_ID AND code.Index = chapter_description.code_ID 
			AND code = %s''', (codeValue,))
	elif catValue:
		if len(catValue.split(" ")) == 1:
			cur.execute('''SELECT * FROM MentalHealth.category_description WHERE category = %s''', (catValue,))
		else: 
			complex_value = catValue.split(" or ")
			cur.execute('''SELECT * FROM MentalHealth.category_description WHERE category = %s OR category = %s''', (complex_value[0], complex_value[1]))
	rv = cur.fetchall()
	return str(rv)

# Main
if __name__ == "__main__":
	app.run(debug=True)


