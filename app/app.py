import os
import secrets
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, make_response, flash
from livereload import Server
from forms import LoginForm
import redis
from config import Config
from jwt_tokens import create_download_token, create_upload_token, create_list_token
from setup import create_sample_users

app = Flask(__name__)
app.config.from_object(Config)

user_manager = Config.user_manager
login_manager = Config.login_manager

create_sample_users(user_manager)


@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    session_id = request.cookies.get('session-id')
    if session_id is None:
        return render_template('index.html')

    if not login_manager.isSessionValid(session_id):
        # TODO: Display invalid message
        flash('Sesja wygasła', 'alert-warning')
        response = make_response(render_template('index.html'))
        response.set_cookie('session-id', '', expires=0)  # Clear cookie
        return response

    login = login_manager.getLogin(session_id)
    return render_template('index.html', logged=True, login=login)


@app.route('/files')
def files():
    session_id = request.cookies.get('session-id')
    if session_id is None:
        # TODO: Display require login message message
        flash('Wprowadzony adres wymaga logowania', 'alert-danger')
        return render_template('index.html'), 403

    if not login_manager.isSessionValid(session_id):
        # TODO: Display invalid message
        flash('Sesja wygasła', 'alert-warning')
        response = make_response(render_template('index.html'))
        response.set_cookie('session-id', '', expires=0)  # Clear cookie
        return response, 403

    login = login_manager.getLogin(session_id)
    tokens = {
        'download_token': create_download_token(login),
        'upload_token': create_upload_token(login),
        'list_token': create_list_token(login),
    }

    return render_template('files.html', logged=True, login=login, **tokens)


@app.route('/signup')
def signup():
    # TODO: Create user and validate
    flash('Kreacja konta aktualnie nie działa', 'alert-danger')
    return render_template('signup.html', title='Kreacja konta')


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login = form.login.data

        session_id = login_manager.registerLogin(login)
        response = redirect(url_for('index'))
        response.set_cookie('session-id', session_id)
        return response

    else:
        return render_template('login.html', title='Logowanie', form=form)


@app.route('/logout', methods=["GET"])
def logout():
    session_id = request.cookies.get('session-id')
    login_manager.registerLogout(session_id)

    flash('Nastąpiło poprawne wylogowanie', 'alert-success')
    response = redirect(url_for('index'))
    response.set_cookie('session-id', '', expires=0)  # Clear cookie
    return response


# Run app with live reload
if app.debug:
    server = Server(app.wsgi_app)
    # server.watch
    server.serve(port=5000)
