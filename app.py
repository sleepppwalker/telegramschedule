from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from functools import wraps
import logging
import subprocess

subprocess.Popen(['python', 'bk.py'])

app = Flask(__name__)
app.secret_key = '123'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        c = conn.cursor()

        c.execute('SELECT * FROM users WHERE tblogin = ? AND tbpassword = ?', (username, password))
        user = c.fetchone()

        conn.close()

        if user:
            session['logged_in'] = True
            return redirect('/')
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/')

@app.route('/')
@login_required
def index():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM schedule')
    rows = c.fetchall()
    conn.close()
    return render_template('index.html', rows=rows)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        start_day = request.form['start_day']
        groupname = request.form['groupname']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        lessonname = request.form['lessonname']
        auditory = request.form['auditory']
        teachername = request.form['teachername']
        date = request.form['date']
        course = request.form['course']
        comment_to_day = request.form['comment_to_day']
        pod_groups = request.form['pod_groups']

        conn = get_db_connection()
        c = conn.cursor()
        c.execute('INSERT INTO schedule (start_day, groupname, start_time, end_time, lessonname, auditory, teachername, date, course, comment_to_day, pod_groups) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (start_day, groupname, start_time, end_time, lessonname, auditory, teachername, date, course, comment_to_day, pod_groups))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('add.html')
    
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM schedule WHERE id = ?', (id,))
    row = c.fetchone()
    logging.debug('Row: %s', row)
    if row is None:
        return "Запись не найдена"

    if request.method == 'POST':
        start_day = request.form['start_day']
        groupname = request.form['groupname']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        lessonname = request.form['lessonname']
        auditory = request.form['auditory']
        teachername = request.form['teachername']
        date = request.form['date']
        course = request.form['course']
        comment_to_day = request.form['comment_to_day']
        pod_groups = request.form['pod_groups']

        c.execute('''UPDATE schedule SET start_day = ?, groupname = ?, start_time = ?, end_time = ?, lessonname = ?, auditory = ?, teachername = ?, date = ?, course = ?, comment_to_day = ?, pod_groups= ? WHERE id = ?''',
                  (start_day, groupname, start_time, end_time, lessonname, auditory, teachername, date, course, comment_to_day, pod_groups, id))
        conn.commit()
        conn.close()
        return redirect('/')

    conn.close()
    return render_template('edit.html', row=row)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM schedule WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8080)