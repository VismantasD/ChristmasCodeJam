from flask import Flask
from flask import request, g
from sqlite3 import dbapi2 as sqlite3
import numpy as np
import base64
import StringIO

app = Flask(__name__)

def destringifynp(s):
    s = base64.b64decode(s)
    i = StringIO.StringIO(s)
    return np.load(i)

def connect_db():
    db = sqlite3.connect('mydb.db')
    db.row_factory = sqlite3.Row
    return db

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def leaderboard():
    db = get_db()
    cur = db.execute('select name from teams')
    names = cur.fetchall() 
    x = '<br>'.join((r['name'] for r in names))
    return 'Leaderboard will be here.<br>{}'.format(x)


@app.route('/submit', methods=['POST'])
def submit():
    r = request.get_json()
    teamname = r['teamname']
    predictions=np.array(r['predictions'])
    x = destringifynp(predictions)
    return 'Happy shape {} from team {}'.format(x.shape, teamname)

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return """
        <html>
        <head><title>Register New Team</title></head>
        <form method="post">
            Team name:<br>
            <input type="text" name="teamname"><br>
            <input type="submit" value="Register Team">
        </form>
        </head>
        """
    else:
        db = get_db()
        c = db.cursor()
        c.execute("insert into teams (name) values ('{}')".format(request.form['teamname']))
        db.commit()
        return "registering team: {}".format(request.form['teamname'])







