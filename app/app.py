import os
import secrets
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, make_response, flash, Response
import requests
import urllib.parse
from livereload import Server
from forms import LoginForm, FileUploadForm
import redis
from config import Config
from jwt_tokens import create_download_token, create_upload_token, create_list_token, create_delete_token
from setup import create_sample_users
from decorators import login_required

from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode
from functools import wraps
from werkzeug.exceptions import HTTPException

from flask_sse import sse

from api import api

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(sse, url_prefix='/stream')

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id=Config.AUTH0_CLIENT_ID,
    client_secret=Config.AUTH0_CLIENT_SECRET,
    api_base_url=Config.AUTH0_API_BASE_URL,
    access_token_url=f'{Config.AUTH0_API_BASE_URL}/oauth/token',
    authorize_url=f'{Config.AUTH0_API_BASE_URL}/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)


# user_manager = Config.user_manager
login_manager = Config.login_manager

# create_sample_users(user_manager)


@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    user_info = resp.json()
    user_name = user_info['name']

    # Use custom login manager from milestone 2
    session_id = login_manager.registerLogin(user_name)
    response = redirect(url_for('index'))
    response.set_cookie('session-id', session_id,
                        httponly=True)
    return response


@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    session_id = request.cookies.get('session-id')
    if session_id is None:
        return render_template('index.html')

    if not login_manager.isSessionValid(session_id):
        flash('Sesja wygasła', 'alert-warning')
        response = make_response(render_template('index.html'))
        response.set_cookie('session-id', '', expires=0)  # Clear cookie
        return response

    login = login_manager.getLogin(session_id)
    return render_template('index.html', logged=True, login=login)


@app.route('/publications', defaults={'u_path': ''})
@app.route('/publications/<path:u_path>')
@login_required
def publications(u_path, login):
    app_url = Config.APP_URL
    file_api_url = Config.FILE_STORE_URL
    publications_api_url = Config.PUBLICATION_API_URL
    return render_template('publications.html', logged=True, login=login,
                           app_url=app_url, file_api_url=file_api_url, publications_api_url=publications_api_url)


@app.route('/files/delete/<int:id>')
@login_required
def delete_file(id, login):
    # Map id to file name
    token = create_list_token(login)
    url = Config.FILE_STORE_URL + f"/files?user={login}&token={token}"
    r = requests.get(url)
    if (r.status_code != 200):
        flash("Nie udało się pobrać pliku", "alert-danger")
        return redirect(url_for('index'))

    files = r.json()
    file_name = files[id]['fileName']

    token = create_delete_token(login)
    url = Config.FILE_STORE_URL + \
        f"/files?user=jan&file={file_name}&token={token}"
    r = requests.delete(url)

    if r.status_code == 200:
        flash('Plik został usunięty', category='alert-success')
    else:
        flash('Nie udało się usunąć pliku', category='alert-danger')

    return redirect(url_for('files'))


@app.route('/files/download/<int:id>')
@login_required
def download_file(id, login):
    # Map id to file name
    token = create_list_token(login)
    url = Config.FILE_STORE_URL + f"/files?user={login}&token={token}"
    r = requests.get(url)
    if (r.status_code != 200):
        flash("Nie udało się pobrać pliku", "alert-danger")
        return redirect(url_for('index'))

    files = r.json()
    file_name = files[id]['fileName']

    token = create_download_token(login, file_name)
    url = 'http://localhost:8081' + \
        f'/files/{file_name}?user={login}&token={token}'

    return redirect(url)


@app.route('/files/upload', methods=["POST"])
@login_required
def upload_file(login):
    form = FileUploadForm()
    form.validate()
    if len(form.file.errors) > 0:
        flash('Brak pliku do wysłania', category='alert-warning')
        return redirect(url_for('files'))

    token = create_upload_token(login)
    url = Config.FILE_STORE_URL + f'/files?user={login}&token={token}'
    files = {'file': (form.file.data.filename, form.file.data)}

    r = requests.post(url, files=files)
    if r.status_code == 200:
        flash('Plik został przesłany', category='alert-success')
    else:
        flash('Nie udało się przesłać pliku', category='alert-danger')

    return redirect(url_for('files'))


@app.route('/files')
@login_required
def files(login):
    # Get user files
    token = create_list_token(login)
    url = Config.FILE_STORE_URL + f"/files?user={login}&token={token}"

    r = requests.get(url)
    if (r.status_code != 200):
        flash("Nie udało się pobrać listy plików", "alert-danger")
        return redirect(url_for('index'))

    files_dto_list = r.json()
    for i, file in enumerate(files_dto_list):
        delete_link = url_for('delete_file', id=i)
        file_name = file['fileName']
        download_link = url_for('download_file', id=i)
        file['links'] = {'delete': delete_link, 'download': download_link}
        file['id'] = str(i)

    return render_template('files.html', logged=True, login=login, files=files_dto_list)


@app.route('/signup')
def signup():
    # TODO: Create user and validate
    flash('Kreacja konta aktualnie nie działa', 'alert-danger')
    return render_template('signup.html', title='Kreacja konta')


@app.route('/login', methods=["GET", "POST"])
def login():
    redirect_uri = Config.APP_URL + url_for('callback_handling')

    return auth0.authorize_redirect(redirect_uri=redirect_uri)


@app.route('/logout', methods=["GET"])
def logout():
    session_id = request.cookies.get('session-id')
    login_manager.registerLogout(session_id)

    flash('Nastąpiło poprawne wylogowanie', 'alert-success')

    # Build redirect to Auth0
    return_url = Config.APP_URL + url_for('index')
    params = {'returnTo': return_url, 'client_id': Config.AUTH0_CLIENT_ID}
    response = redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

    response.set_cookie('session-id', '', expires=0,
                        httponly=True)  # Clear cookie
    return response


# Run app with live reload
if app.debug:
    server = Server(app.wsgi_app)
    # server.watch
    server.serve(port=5000)
