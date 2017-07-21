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

@app.route('/interface')
def load():
	return render_template('interface.html')


# Main
if __name__ == "__main__":
	app.run(debug=True)