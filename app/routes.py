from app import app
from app.forms import LoginForm
from flask import render_template, flash, redirect, url_for, request, make_response
from app import db

def threes(questions):
    out = []
    out2 = []
    x = 0
    for i in questions:
        out2.append(i)
        x += 1
        if x == 3:
            out.append(out2)
            x = 0
            out2 = []
    if len(out2) > 0:
        out.append(out2)
    return out

def render_index(team):
    questions = db.questions()
    points = db.getpoints(team)
    return make_response(render_template('index.html', team=team, points=points, question_lists=threes(questions)))
    
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

@app.route('/question', methods=['GET', 'POST'])
def question():
    team = request.cookies.get('team')
    if team == '' or team is None:
        return login()

    team = request.cookies.get('team')
    question = db.getquestion(request.args.get('question_id'))
    guess = ''
    if request.method == 'POST':
        guess = request.form.get('guess')

    print(team + "  " + guess)
    return render_template('question.html',
                           question=questionpage(question, guess, team))

def questionpage(question, guess, team):
    if (guess != ''):
        question['guess'] = guess
        print(guess)
        print(question['answer'])
        print("heh")
        if (guess.rstrip() == question['answer'].rstrip()):
            print('yay!')
            db.correct(team, question)
    return question
                           
