from flask import Flask, request, render_template, session
from flask import redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

def create_connection():
    return sqlite3.connect('login_password.db')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/authorization', methods=['GET', 'POST'])
def form_authorization():
    if request.method == 'POST':
        Login = request.form.get('Login')
        Password = request.form.get('Password')

        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT password FROM passwords WHERE login = ?', (Login,))
            pas = cursor.fetchone()

        if pas is not None and pas[0] == Password:
            session['user_id'] = Login
            return redirect(url_for('add_project'))
        else:
            return render_template('auth_bad.html')

    return render_template('authorization.html')


@app.route('/registration', methods=['GET', 'POST'])
def form_registration():
    if request.method == 'POST':
        Login = request.form.get('Login')
        Password = request.form.get('Password')

        with create_connection() as conn:
            cursor = conn.cursor()

            # Проверяем, существует ли уже пароль с таким логином
            cursor.execute('SELECT * FROM passwords WHERE login = ?', (Login,))
            existing_user = cursor.fetchone()

            if existing_user:
                return render_template('password_exists.html')  # Добавьте свой шаблон с подсказкой

            # Если такого логина еще нет, то добавляем пользователя
            sql_insert = 'INSERT INTO passwords VALUES (?, ?)'
            cursor.execute(sql_insert, (Login, Password))
            conn.commit()

        return render_template('successfulregis.html')

    return render_template('registration.html')

@app.route('/view_data', methods=['GET'])
def view_data():
        db_lp = sqlite3.connect('login_password.db')
        cursor_db = db_lp.cursor()
        cursor_db.execute('SELECT * FROM passwords')
        data = cursor_db.fetchall()
        cursor_db.close()
        db_lp.close()
        return render_template('view_data.html', data=data)

@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
    user_id = session.get('user_id')

    if user_id == 'admin':
        return redirect(url_for('view_projects'))  # Если пользователь админ, сразу переходим к просмотру проектов

    if request.method == 'POST':
        user_id = session['user_id']
        full_name = request.form.get('full_name')
        passport_number = request.form.get('passport_number')
        course = request.form.get('course')
        groups = request.form.get('group')
        project_name = request.form.get('project_name')
        project_content = request.form.get('project_content')

        db = sqlite3.connect('login_password.db')
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO projects (user_id, full_name, passport_number, course, groups, project_name, project_content)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, full_name, passport_number, course, groups, project_name, project_content))
        db.commit()
        cursor.close()
        db.close()

        return redirect(url_for('add_project'))

    return render_template('add_project.html')


@app.route('/projects', methods=['GET'])
def view_projects():
    user_id = session.get('user_id')

    if user_id is not None:
        with create_connection() as conn:
            cursor = conn.cursor()


            if user_id == 'admin':
                cursor.execute('SELECT * FROM projects')
            else:

                cursor.execute('SELECT * FROM projects WHERE user_id = ?', (user_id,))

            projects = cursor.fetchall()

        return render_template('projects.html', projects=projects)

    return redirect(url_for('form_authorization'))


if __name__ == "__main__":
    app.debug = True
    app.run()