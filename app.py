from flask import *
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL

"""
This file allows us to configure and launch our Flask application (in order to make our display)
"""
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'sql11.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql11427664'
app.config['MYSQL_PASSWORD'] = '1wMlmK2mBF'
app.config['MYSQL_DB'] = 'sql11427664'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
@app.route("/index")
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)