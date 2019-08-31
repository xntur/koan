from app import app
from app.forms import LoginForm
from flask import render_template, flash, redirect, url_for, request, make_response
import db

def render_index(team):
    questions = db.questions()
    return make_response(render_template('index.html', team=team, question_list=questions))
    
def render_login(message):
    return make_response(render_template('login.html', message=message))

def handle_login(request):
    if request.method == 'POST':
        team = request.form.get('team')
        if team is not None:
            response = render_index(team)
            response.set_cookie('team', team)
            return response
    return None

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    index = handle_login(request)
    if index is not None:
        return index

    team = request.cookies.get('team')
    if team == '' or team is None:
        return login()

    return render_index(team)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_login('Sign In')

@app.route('/signout', methods=['GET', 'POST'])
def sign_out():
    index = handle_login(request)
    if index is not None:
        return index

    response = render_login('Thanks for playing. Play again?')
    response.set_cookie('team', '', expires=0)
    return response
