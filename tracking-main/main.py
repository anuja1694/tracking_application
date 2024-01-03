from flask import Flask, render_template, session, request, redirect, url_for, g
import os
import pandas as pd
import sqlite3

from werkzeug.security import generate_password_hash, check_password_hash

from database import get_database

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = os.urandom(24)


@app.teardown_appcontext
def close_database(error):
    if hasattr(g, 'tracking_db'):
        g.tracking_db.close()


def get_current_user():
    user = None
    if 'user' in session:
        user = session['user']
        db = get_database()
        user_cur = db.execute('select * from users where name = ?', [user])
        user = user_cur.fetchone()
    return user


@app.route('/')
def index():
    user = get_current_user()
    return render_template('home.html', user=user)


@app.route('/register', methods=["POST", "GET"])
def register():
    user = get_current_user()
    db = get_database()
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        trkuser_cur = db.execute('select * from users where name = ?', [name])
        existing_username = trkuser_cur.fetchone()
        if existing_username:
            return render_template('register.html', registererror='Username already taken , try different username.')
        db.execute('insert into users ( name, password) values (?, ?)', [name, hashed_password])
        db.commit()
        return redirect(url_for('login'))
    return render_template('register.html', user=user)


@app.route('/login', methods=["POST", "GET"])
def login():
    user = get_current_user()
    error = None
    db = get_database()
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        user_cursor = db.execute('select * from users where name = ?', [name])
        user = user_cursor.fetchone()
        if user:
            if check_password_hash(user['password'], password):
                session['user'] = user['name']
                return redirect(url_for('tracking'))
            else:
                error = "Username or Password did not match, Try again."
        else:
            error = 'Username or password did not match, Try again.'
    return render_template('login.html', loginerror=error, user=user)


@app.route('/tracking')
def tracking():
    user = get_current_user()
    if user is None:
        return redirect(url_for('login'))
    db = get_database()
    trk_cur = db.execute('select * from trk ')
    alltrk = trk_cur.fetchall()
    return render_template('tracking.html', user=user, alltrk=alltrk)



@app.route('/addtracking', methods=["POST", "GET"])
def addtracking():
    user = get_current_user()
    if request.method == "POST":
        route = request.form['route']
        vehicle = request.form['vehicle']
        status = request.form['status']
        team = request.form['team']
        trk_date = request.form['trk_date']
        db = get_database()
        db.execute('insert into trk (route, vehicle, status ,team,trk_date ) values (?,?,?,?,?)',
                   [route, vehicle, status, team, trk_date])
        db.commit()
        return redirect(url_for('tracking'))
    return render_template('addtracking.html', user=user)


@app.route('/singletracking/<int:trkid>')
def singletracking(trkid):
    user = get_current_user()
    db = get_database()
    trk_cur = db.execute('select * from trk where trkid = ?', [trkid])
    single_trk = trk_cur.fetchone()
    return render_template('singletracking.html', user=user, single_trk=single_trk)


@app.route('/fetchone/<int:trkid>')
def fetchone(trkid):
    user = get_current_user()
    db = get_database()
    trk_cur = db.execute('select * from trk where trkid = ?', [trkid])
    single_trk = trk_cur.fetchone()
    return render_template('updatetracking.html', user=user, single_trk=single_trk)


@app.route('/updatetracking', methods=["POST", "GET"])
def updatetracking():
    user = get_current_user()
    if request.method == 'POST':
        trkid = request.form['trkid']
        route = request.form['route']
        vehicle = request.form['vehicle']
        status = request.form['status']
        team = request.form['team']
        trk_date = request.form['trk_date']
        db = get_database()
        db.execute('update trk set route = ?, vehicle =? , status = ? , team = ?, trk_date= ? where trkid = ?',
                   [route, vehicle, status, team, trk_date, trkid])
        db.commit()
        return redirect(url_for('tracking'))
    return render_template('updatetracking.html', user=user)


@app.route('/deletetrk/<int:trkid>', methods=["GET", "POST"])
def deletetrk(trkid):
    user = get_current_user()
    if request.method == 'GET':
        db = get_database()
        db.execute('delete from trk where trkid = ?', [trkid])
        db.commit()
        return redirect(url_for('tracking'))
    return render_template('tracking.html', user=user)


@app.route('/logout')
def logout():
    session.pop('user', None)
    render_template('home.html')


if __name__ == '__main__':
    app.run()
