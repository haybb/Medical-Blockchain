from flask import *
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config['MYSQL_HOST'] = ''
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = ''
app.config['MYSQL_CURSORCLASS'] = ''

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    # cur.execute('''CREATE TABLE example (id INTEGER, name VARCHAR(20))''')

    # cur.execute('''INSERT INTO example VALUES (1, 'Anthony')''')
    # cur.execute('''INSERT INTO example VALUES (2, 'Billy')''')
    # mysql.connection.commit()

    # cur.execute('''create table blockchain(idx varchar(10), hash varchar(64), previous_hash varchar(64), transactions varchar(100), timestamp varchar(17), nonce varchar(15))''')
    # cur.execute('''DROP TABLE blockchain''')

    # cur.execute('''CREATE TABLE users(
    #                 name varchar(30),
    #                 username varchar(30),
    #                 email varchar(50),
    #                 password varchar(100))''')

    # cur.execute('''SELECT * FROM blockchain''')
    # print(cur.fetchall())

    return 'Done'


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
