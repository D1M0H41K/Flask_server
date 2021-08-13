import json
import os
import requests
from flask import request, render_template, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user
from . import app, login_manager, openid_config_file_name, client, google_client_id, google_client_secret, \
    integrate_delay
from .db import Todo, remove_todo_by_id, add_todo_to_db, get_todo_by_id, \
    commit_db_changes, get_todo_list, User, add_user_to_db, get_user_by_login, \
    get_user_by_email, RegistrationForm, LogInForm
from .flask_celery import integrate


def get_google_config():
    with open(os.path.join('todo/google_openid', openid_config_file_name), 'r') as config:
        return json.load(config)


def remove_todo_db(todo_id):
    remove_todo_by_id(todo_id)


def add_todo_db(data):
    if 'task' in data and data.get('task') != '':
        todo = Todo(task=data.get('task'), user_id=current_user.id)
        add_todo_to_db(todo, current_user)
        integrate.delay(integrate_delay, todo.id)


def update_todo_db(data, todo_id):
    todo_task = get_todo_by_id(todo_id)
    if 'done' in data:
        todo_task.done = not todo_task.done
    commit_db_changes()


def get_user_data(data):
    if get_user_by_login(data.login.data) is not None:
        if check_password_hash(pwhash=get_user_by_login(data.login.data).password, password=data.password.data):
            return get_user_by_login(data.login.data)
    elif get_user_by_email(data.login.data) is not None:  # Here login is email
        if check_password_hash(pwhash=get_user_by_email(data.login.data).password, password=data.password.data):
            return get_user_by_email(data.login.data)
    flash('Not correct login or password')


def register_user(data):
    if get_user_by_login(data.login.data) is None:
        if get_user_by_email(data.email.data) is None:
            add_user_to_db(User(email=data.email.data,
                                login=data.login.data,
                                password=generate_password_hash(password=data.password.data)))
        else:
            flash('Account with given email already exists')
            return -1
    else:
        flash('Account with given login already exists')
        return -1


@app.route('/')
def hello_world():
    if current_user.is_authenticated:
        return redirect('/todo')
    return redirect('/login')


@app.route('/login/google')
def login_google():
    google_conf = get_google_config()
    auth_endpoint = google_conf['authorization_endpoint']
    request_uri = client.prepare_request_uri(
        auth_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"]
    )
    return redirect(request_uri)


@app.route('/login/google/callback')
def login_google_callback():
    code = request.args.get("code")
    google_conf = get_google_config()
    token_endpoint = google_conf['token_endpoint']
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(google_client_id, google_client_secret),
    )
    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_conf["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    if userinfo_response.json().get("email_verified"):
        if not get_user_by_email(userinfo_response.json()["email"]):
            add_user_to_db(User(email=userinfo_response.json()["email"],
                                login=userinfo_response.json()["given_name"],
                                password='google'))
        login_user(get_user_by_email(userinfo_response.json()["email"]))
        return redirect('/todo')
    else:
        return "User email not available or not verified by Google.", 400


@app.route('/login', methods=['GET', 'POST'])
def login_main():
    form = LogInForm(request.form)
    if request.method == 'POST':
        if form.validate():
            user = get_user_data(form)
            if user is None:
                return redirect('/login')
            login_user(user, remember=True)
            return redirect('/todo')
        else:
            flash('Not correct data in fields')
            return redirect('/login')
    else:
        return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register_main():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        if form.validate():
            if register_user(form) == -1:
                return redirect('/register')
        else:
            flash('Not correct data in fields')
            return redirect('/register')
        login_user(get_user_by_login(form.login.data))
        return redirect('/todo')
    else:
        return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')


@app.route('/todo', methods=['GET', 'POST'])
@login_required
def todo_main():
    if request.method == 'POST':
        add_todo_db(request.form)
        return redirect('/todo')
    else:
        todo_list = get_todo_list(current_user)
        return render_template('todo.html', todo_list=todo_list)


@app.route('/todo/<todo_id>/update', methods=['POST'])
@login_required
def todo_update(todo_id=None):
    update_todo_db(request.form, int(todo_id))
    return redirect('/todo')


@app.route('/todo/<todo_id>/delete', methods=['POST'])
@login_required
def todo_remove(todo_id=None):
    remove_todo_db(int(todo_id))
    return redirect('/todo')
