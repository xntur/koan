from app import app
from app.forms import LoginForm
from flask import render_template, flash, redirect, url_for, request, make_response
from app import db

def makequestions(questions, answered):
    todo = []
    todo_temp = []
    done = []
    done_temp = []
    for i in questions:
        if i['id'] in answered:
            done_temp.append(i)
            if len(done_temp) == 3:
                done.append(done_temp)
                done_temp = []
        else:
            todo_temp.append(i)
            if len(todo_temp) == 3:
                todo.append(todo_temp)
                todo = []
    if len(todo_temp) > 0:
        todo.append(todo_temp)
    if len(done_temp) > 0:
        done.append(done_temp)
    return todo, done

def render_index(team):
    questions = db.questions()
    answered = db.getanswered(team)
    points = db.getpoints(team)
    todo, done = makequestions(questions, answered)
    return make_response(
        render_template('index.html', team=team, points=points,
                        question_lists=todo,
                        done_question_lists=done))
    
def render_login(message):
    return make_response(render_template('login.html', message=message))

def handle_login(request):
    print("here!!!")
    if request.method == 'POST':
        team = request.form.get('team')
        print(team)
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
    index = handle_login(request)
    if index is not None:
        return index
    return render_login('Sign In')

@app.route('/signout', methods=['GET'])
def sign_out():
    response = redirect(url_for('login'))
    response.set_cookie('team', '', expires=0)
    return response

@app.route('/question', methods=['GET', 'POST'])
def question():
    team = request.cookies.get('team')
    if team == '' or team is None:
        return redirect(url_for('login'))

    team = request.cookies.get('team')
    question = db.getquestion(request.args.get('question_id'))
    guess = ''
    if request.method == 'POST':
        guess = request.form.get('guess')

    return render_template('question.html',
                           question=questionpage(question, guess, team))

def questionpage(question, guess, team):
    if (guess != ''):
        question['guess'] = guess
        if (guess.rstrip() == question['answer'].rstrip()):
            db.correct(team, question)
    return question
                           
