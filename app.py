from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)

app.config['SECRET_KEY'] = 'placeholder'
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def start_survey():
    return render_template('home.html', survey=surveys['satisfaction'])

@app.route('/questions/<id>')
def show_question(id):
    if len(responses) == len(surveys['satisfaction'].questions):
        flash("The survey is complete","error")
        return redirect('/finish')
    elif int(id) == len(responses):
        return render_template('question.html', id=id, question=surveys['satisfaction'].questions[int(id)])
    else:
        flash("Please answer the questions in order","error")
        return redirect('/questions/'+str(len(responses)))

@app.route('/answers/<id>', methods=["GET","POST"])
def store_answer(id):
    choiceIndex = request.form['options']
    choiceIndex = choiceIndex[0:len(choiceIndex)-1]
    question = surveys['satisfaction'].questions[int(id)]
    answer = question.choices[int(choiceIndex)]
    responses.append(answer)
    nextId = int(id)+1
    if nextId >= len(surveys['satisfaction'].questions):
        return redirect('/finish')
    return redirect('/questions/'+str(nextId))

@app.route('/finish')
def finish():
    return render_template('finish.html', responses=responses)