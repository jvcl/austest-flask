from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<Question %r>' % self.title


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    question = db.relationship('Question', backref=db.backref('answers', lazy='dynamic'))
    answer = db.Column(db.String(100))
    response = db.Column(db.Boolean)

    def __init__(self, question, answer, response=False):
        self.question = question
        self.answer = answer
        self.response = response

    def __repr__(self):
        return '<Answer %r>' % self.answer


# Create the database tables.
db.create_all()

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        score = 0
        questions = []
        answers = []
        for i in range(20):
            try:
                answer_id = request.form[str(i)]
                answer = Answer.query.get(answer_id)
                question = answer.question
                if answer.response:
                    score +=1
                    questions.append(question)
                    answers.append((question.answers.all(), True))
                else:
                    questions.append(question)
                    answers.append((question.answers.all(), False))
            except KeyError:
                print "Not key"
                question = Question.query.get(request.form["a" + str(i)])
                questions.append(question)
                answers.append((question.answers.all(), False))
        return render_template('results.html', questions=questions, answers=answers, score=score)

    dic = {}
    for question in Question.query.all()[:20]:
        dic[question] = question.answers.all()
    return render_template('test.html', questions=dic)


if __name__ == '__main__':
    app.run(debug=True)
