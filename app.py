from flask import Flask, request, render_template, redirect, session, flash
from surveys import Question, Survey, surveys

app =Flask(__name__)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "123@45#"


#responses =[]
final_resp =""
surv =""
submitted = ""
surveys_done = []

@app.route('/')
def home_page():
    print(surveys_done)
    return render_template("index.html", surveys=surveys)

@app.route('/select',methods=["POST"])
def page():
    survey = request.form.get("select_survey")
    if survey is None:
        return redirect('/')
    elif survey in surveys_done:
        flash(f"You submitted the survey {survey}")
        return redirect('/')
    else:
        session['surv'] = survey
        print("**************Session***************")
        print (session['surv'])
        print("**************Session***************")
        return render_template("home.html", survey= surveys[survey])

@app.route('/start',methods = ["POST"])
def start_survey():
    session['final_resp'] = []
    print("**************Session confirm***************")
    print (session['surv'])
    print("**************Session************************")
    return redirect("/questions/0")

@app.route("/questions/<int:nums>")
def questions(nums):

    sid = session['surv']

    if (len(list(session['final_resp'] )) == len(list(surveys[sid].questions))):
        session['answers'] = session['final_resp']
        return redirect("/done")
    if (nums > len(surveys[sid].questions)):
        flash(f"Invalid question id: {nums}.")
        return redirect(f"/questions/{len(responses)}")
    question = surveys[sid].questions[nums]
    return render_template("form.html", question =question, num = nums)

@app.route("/survey", methods=["POST"])
def submit_survey():

    #session['final_resp'].append(....)
    responses = session['final_resp']
    resp = request.form['answer']
    comment = request.form.get('comment',"")
    responses.append({'answer':resp, 'comment':comment})
    session['final_resp'] = responses
    sid = session['surv'] 
    if (len(session['final_resp']) == len(surveys[sid].questions)):
        session['final_resp'] =[]
        return redirect("/done")
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/done")
def submit():
    surveys_done.append(session['surv'])
    print("bbbbbbbbbbbbbbbbbbbbbbbbb")
    print(surveys_done)
    
    return render_template('thank.html')

