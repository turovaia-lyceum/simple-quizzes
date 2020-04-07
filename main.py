from flask import Flask, render_template

from data import db_session
from data.option import Option
from data.question import Question
from data.quiz import Quiz

app = Flask('Quiz app')


def main():
    db_session.global_init("db/quizzes.sqlite")

    @app.route('/')
    @app.route('/quizzes')
    def index():
        session = db_session.create_session()
        quizzes = session.query(Quiz).all()
        return render_template('index.html', quizzes=quizzes)

    @app.route('/quiz/<int:quiz_id>')
    def show_quiz(quiz_id):
        session = db_session.create_session()
        quiz = session.query(Quiz).get(quiz_id)

        if not quiz:
            return 'Quiz with that id not found'

        return render_template('quiz.html', quiz=quiz)

    app.debug = True
    app.run()


def fill_data():
    db_session.global_init("db/quizzes.sqlite")
    session = db_session.create_session()

    quiz1 = Quiz(name='Python quiz')

    question1 = Question(text='Как называется строковый тип в Python?', quiz=quiz1)
    # session.add(question1)
    option1 = Option(text='int', question=question1)
    # session.add(option1)
    option2 = Option(text='string', question=question1)
    option3 = Option(text='str', question=question1)
    option4 = Option(text='char', question=question1)

    session.add(option1)
    session.add(option2)
    session.add(option3)
    session.add(option4)

    question2 = Question(text='2 + 2?', quiz=quiz1)
    option1 = Option(text='2', question=question2)
    option2 = Option(text='3', question=question2)
    option3 = Option(text='4', question=question2)
    option4 = Option(text='5', question=question2)

    session.add(option1)
    session.add(option2)
    session.add(option3)
    session.add(option4)

    session.commit()


if __name__ == '__main__':
    # fill_data()
    main()
