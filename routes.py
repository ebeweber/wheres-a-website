import sqlite3

from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

# Open database and use them in scripts elegantly
@app.before_request
def before_request():
    g.db = connect_db()

# Shut down the database after use
@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
	return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_email():
	if request.form['email'] != "":
		g.db.execute('insert into entries (email) values (?)',
                 [request.form['email']])
		g.db.commit()
	return redirect(url_for('index'))

if __name__ == "__main__":
	app.run()