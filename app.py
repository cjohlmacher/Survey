from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)

app.config['SECRET_KEY'] = 'placeholder'
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

responses = []
active_survey = None

@app.route('/')
def choose_survey():
    return render_template('home.html', surveys=surveys)

@app.route('/intro/<id>')
def start_survey(id):
    return render_template('intro.html', survey=active_survey)

@app.route('/select', methods=["POST"])
def log_survey_choice():
    survey_choice = request.form['options']
    survey_choice = survey_choice[0:len(survey_choice)-1]
    global active_survey
    active_survey = surveys[survey_choice]
    return redirect('/intro/'+survey_choice)

@app.route('/questions/<id>')
def show_question(id):
    global active_survey
    if not active_survey:
        flash("Please choose a survey first")
        return redirect('/')
    elif len(responses) == len(surveys[active_survey.slug].questions):
        flash("The survey is complete","error")
        return redirect('/finish')
    elif int(id) == len(responses):
        return render_template('question.html', id=id, question=surveys[active_survey.slug].questions[int(id)])
    else:
        flash("Please answer the questions in order","error")
        return redirect('/questions/'+str(len(responses)))

@app.route('/answers/<id>', methods=["GET","POST"])
def store_answer(id):
    if not request.form.get('options'):
        flash('Trouble submitting answer. Please try again.')
        return redirect('/questions/'+id)
    choiceIndex = request.form['options']
    choiceIndex = choiceIndex[0:len(choiceIndex)-1]
    question = surveys[active_survey.slug].questions[int(id)]
    answer = question.choices[int(choiceIndex)]
    responses.append(answer)
    nextId = int(id)+1
    if nextId >= len(surveys[active_survey.slug].questions):
        return redirect('/finish')
    return redirect('/questions/'+str(nextId))

@app.route('/finish')
def finish():
    return render_template('finish.html', responses=responses)