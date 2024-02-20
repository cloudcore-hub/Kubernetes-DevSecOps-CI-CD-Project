import html


class QuizBrain:

    def __init__(self, q_list):
        self.question_number = 0
        self.score = 0
        self.question_list = q_list
        self.current_question = None

    def to_dict(self):
        current_question_index = self.question_list.index(self.current_question) if self.current_question else None
        return {
            'question_number': self.question_number,
            'score': self.score,
            'current_question_index': current_question_index,
        }

    @staticmethod
    def from_dict(data, question_list):
        quiz = QuizBrain(question_list)
        quiz.question_number = data.get('question_number', 0)
        quiz.score = data.get('score', 0)
        current_question_index = data.get('current_question_index')
        if current_question_index is not None:
            quiz.current_question = quiz.question_list[current_question_index]
        return quiz

    def still_has_questions(self):
        return self.question_number < len(self.question_list)

    def next_question(self):
        self.current_question = self.question_list[self.question_number]
        self.question_number += 1
        q_text = html.unescape(self.current_question.text)
        # user_answer = input(f"Q.{self.question_number}: {q_text} (True/False): ")
        # self.check_answer(user_answer)
        return f"Q.{self.question_number}: {q_text}"

    def check_answer(self, user_answer):
        correct_answer = self.current_question.answer
        if user_answer.lower() == correct_answer.lower():
            self.score += 100
            return True
        else:
            return False

