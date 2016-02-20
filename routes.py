import os

from databases import SqlLiteConnector
from databases.SqlLiteConnector import get_db
from application import app
import application
from flask import render_template, request, session, flash, redirect, url_for, \
    abort, get_flashed_messages
from jinja2 import Environment, PackageLoader
import sys
# from databases import CassandraConnector
import jinja2.filters
sys.path.append('/home/karma/Development/shareit/request_handler')
env = Environment(loader=PackageLoader('request_handler', 'templates'))
env.globals.update(url_for=url_for)
env.globals.update(session=session)
env.globals.update(get_flashed_messages=get_flashed_messages)
env.line_statement_prefix = '#'

# dataBase = CassandraConnector.CassandraConnector
# current_dir = os.curdir()


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        print(str(request))
        local_json = request.get_json()
        username = local_json['username']
        password = local_json['password']
        hashed_password = hash(password)
        db = get_db()
        print(username+" "+str(hashed_password))
        db.execute('insert into authentication (username, password) values (?, ?)', [username, password])
        db.commit()
        return 'user added'
    template = env.get_template('add_user.html')
    return template.render()


@app.route('/insert_into_authentication_table', methods=['POST'])
def insert_into_authentication_table():
    db = get_db()
    db.execute('insert into authentication (username, password) values (?, ?)', [request.form['username'],
                                                                                 request.form['password']])
    db.commit()


@app.route('/check_valid_user', methods=['GET', 'POST'])
def check_valid_user():
    if request.method == 'GET':
        db = get_db()
        cur = db.execute('select username, password from authentication')
        entries = cur.fetchall()
        print(len(entries))
        for entry in entries:
            print(entry['username']+":"+entry['password'])
        template = env.get_template('show_entries.html')
        return template.render(entries=entries, application=application)
    local_json = request.get_json()
    username = (local_json['username'],)
    password = local_json['password']
    db = get_db()
    cur = db.execute('select password from authentication where username=?', username)
    results = cur.fetchall()
    for result in results:
        if result['password'] == password:
            return 'valid user'
        else:
            return 'invalid user'


@app.route('/documentation')
def get_doc():
    seq = [1, 2, 3, 4, 5]
    link = '/home/karma/Desktop/pp.jpeg'
    template = env.get_template('documentation.html')
    return template.render(karma=seq, link=link)


@app.route('/')
def show_entries():
    # print(type(session['master_user']))
    # print(str(session['master_user']))
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    template = env.get_template('show_entries.html')
    return template.render(entries=entries, application=application)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
               [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    template = env.get_template('login.html')
    return template.render(error=error)


@app.route('/login_master', methods=['GET', 'POST'])
def login_master():
    error = None
    # cookie = request.cookies
    # print(cookie.keys())
    session['master_user'] = False
    print("hallaue")
    if request.method == 'POST':
        # json_part = request.get_json()
        # print(json_part.keys())
        # for key in json_part.keys():
        #     print(json_part[key])
        # if json_part['username'] != app.config['USERNAME']:
        #     error= 'Invalid username'
        # elif json_part['password'] != app.config['PASSWORD']:
        #     error = 'Invalid password'
        # else:
        #     session['logged_in'] = True
        #     flash('You have been logged in')
        #     return redirect(url_for('show_entries'))
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            session['master_user'] = True
            print(type(session['master_user']))
            print(str(session['master_user']))
            flash('You were logged in')
            return redirect(url_for('show_entries'))

    print(type(session['master_user']))
    print(str(session['master_user']))
    template = env.get_template('login.html')
    return template.render(error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


# @app.route('/createdatabase')
# def createDatabase():
#     CassandraConnector.get_session()
#     return 'keyspace created'

@app.route('/help')
def help():
    SqlLiteConnector.init_db()
    return "done"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9558)
