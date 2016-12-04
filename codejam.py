from flask import Flask
from flask import request, g
from sqlite3 import dbapi2 as sqlite3
import numpy as np
import base64
import StringIO
import random

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
    secret = r['secret']
    predictions=np.array(r['predictions'])
    db = get_db()
    c = db.cursor()
    r = c.execute("select teamid, secret from teams where name='{}'".format(teamname))
    row = r.fetchone()
    if row[1] <>secret:
        return "Wrong Password", 401
    c.execute("insert into entries (teamid, entry) values ({}, '{}')".format(row[0], predictions))
    db.commit()
    x = destringifynp(predictions)
    return 'Happy shape {} from team {}'.format(x.shape, teamname)
@app.route('/list/<name>')

def listSubmissions(name):
    db = get_db()
    c = db.cursor()
    print name
    rows = c.execute("select * from entries inner join teams on entries.teamid=teams.teamid where teams.name='{}'".format(name))
    r = ""
    for row in rows:
        print row
        r += row['entry'] 
    return r


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
        secret = random.randrange(1000,9999+1)
        c.execute("insert into teams (name, secret) values ('{}', {})".format(request.form['teamname'], secret))
        db.commit()
        return "registering team: {}. Secret key: {}".format(request.form['teamname'], secret)







