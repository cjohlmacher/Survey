from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)

app.config['SECRET_KEY'] = 'placeholder'
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

@app.route('/')
def choose_survey():
    return render_template('home.html', surveys=surveys)

@app.route('/intro/<id>')
def start_survey(id):
    return render_template('intro.html', survey=surveys[session['active_survey_slug']])

@app.route('/select', methods=["POST"])
def log_survey_choice():
    survey_choice = request.form['options']
    session['active_survey_slug'] = surveys[survey_choice].slug
    session['responses'] = []
    return redirect('/intro/'+survey_choice)

@app.route('/questions/<id>')
def show_question(id):
    active_survey_slug = session['active_survey_slug']
    if not active_survey_slug:
        flash("Please choose a survey first")
        return redirect('/')
    elif len(session['responses']) == len(surveys[active_survey_slug].questions):
        flash("The survey is complete","error")
        return redirect('/finish')
    elif int(id) == len(session['responses']):
        return render_template('question.html', id=id, question=surveys[active_survey_slug].questions[int(id)])
    else:
        flash("Please answer the questions in order","error")
        return redirect('/questions/'+str(len(session['responses'])))

@app.route('/answers/<id>', methods=["GET","POST"])
def store_answer(id):
    active_survey_slug = session['active_survey_slug']
    if not request.form.get('options'):
        flash('Trouble submitting answer. Please try again.')
        return redirect('/questions/'+id)
    choiceIndex = request.form['options']
    question = surveys[active_survey_slug].questions[int(id)]
    answer = {
        'response': question.choices[int(choiceIndex)],
        'comment': None
    }
    if request.form.get('comment'):
        answer['comment'] = request.form.get('comment')
    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses
    nextId = int(id)+1
    if nextId >= len(surveys[active_survey_slug].questions):
        return redirect('/finish')
    return redirect('/questions/'+str(nextId))

@app.route('/finish')
def finish():
    active_survey_slug = session['active_survey_slug']
    if len(session['responses']) != len(surveys[active_survey_slug].questions):
        flash("The survey is incomplete","error")
        return redirect('/questions/'+str(len(session['responses'])))
    return render_template('finish.html', surveys=surveys, survey=session['active_survey_slug'], responses=session['responses'])