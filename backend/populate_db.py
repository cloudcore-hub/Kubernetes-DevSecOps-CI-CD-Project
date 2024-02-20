from app import app, db, Question
from data import question_data

def add_questions_to_db():
    with app.app_context():  # Create an application context
        for q in question_data:
            question = Question(text=q['question'], answer=q['correct_answer'])
            db.session.add(question)
        db.session.commit()

if __name__ == '__main__':
    add_questions_to_db()
