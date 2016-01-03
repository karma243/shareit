from databases.SqlLiteConnector import app, get_db
from flask import render_template, request, session, flash, redirect, url_for, \
    abort, get_flashed_messages
from jinja2 import Environment, PackageLoader
import sys

sys.path.append('/home/karma/Development/shareit/request_handler')
env = Environment(loader=PackageLoader('request_handler', 'templates'))
env.globals.update(url_for=url_for)
env.globals.update(session=session)
env.globals.update(get_flashed_messages=get_flashed_messages)


@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    template = env.get_template('show_entries.html')
    return template.render(entries=entries)


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


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9558)
