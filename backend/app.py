from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import random

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')


# Configuring the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'  # Change this to a random secret key

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    scores = db.relationship('Score', backref='user', lazy=True)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(250), nullable=False)
    answer = db.Column(db.String(5), nullable=False)


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #user = db.relationship('User', backref=db.backref('scores', lazy=True))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('quiz'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists')
            return redirect(url_for('login'))

        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully, please login.')
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('quiz'))

    if request.method == 'POST':
        email = request.form['email']  # Use email instead of username
        password = request.form['password']
        user = User.query.filter_by(email=email).first()  # Query by email
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('quiz'))
        else:
            flash('Invalid email or password')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/quiz')
@login_required
def quiz():
    session['current_question_index'] = 0  # Reset index at quiz start
    session['current_score'] = 0  # Reset the score
    return render_template('quiz.html')


@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:  # Replace with actual admin check
        return redirect(url_for('index'))
    scores = Score.query.all()
    return render_template('admin.html', scores=scores)


@app.route('/get_question')
@login_required
def get_question():
    current_index = session.get('current_question_index', 0)
    total_questions = Question.query.count()

    if current_index >= total_questions:
        # Include the final score in the response
        final_score = session.get('current_score', 0)
        return jsonify({"finished": True, "score": final_score})

    question = Question.query.offset(current_index).first()

    if question:
        session['current_question_index'] = current_index + 1
        return jsonify({
            "question_number": current_index + 1,
            "question": question.text,
            "answer": question.answer,
            "total_questions": total_questions
        })
    else:
        return jsonify({"finished": True})


@app.route('/check_answer', methods=['POST'])
@login_required
def check_answer():
    data = request.get_json()
    user_answer = data.get('answer')
    current_index = session.get('current_question_index', 0) - 1
    question = Question.query.offset(current_index).first()

    if question:
        is_correct = (user_answer.lower() == question.answer.lower())
        if is_correct:
            # Update the score in the session
            session['current_score'] = session.get('current_score', 0) + 100
            # # Create a new Score object and save it to the database
            # new_score = Score(score=session['current_score'],
            #                   user_id=current_user.id)
            # db.session.add(new_score)
            # db.session.commit()
        return jsonify({'correct': is_correct, 'score': session.get('current_score', 0)})
    else:
        return jsonify({'correct': False, 'error': 'Question not found'}), 404


@app.route('/finish_quiz', methods=['POST'])
@login_required
def finish_quiz():
    final_score = session.get('current_score', 0)
    new_score = Score(score=final_score, user_id=current_user.id)
    db.session.add(new_score)
    db.session.commit()

    # Optionally, reset the score in the session
    session['current_score'] = 0

    return jsonify({'message': 'Quiz completed, score saved.'})


if __name__ == '__main__':
    app.run(debug=True)
