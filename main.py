from flask import Flask, render_template, request, redirect, url_for
from pymorphy2 import MorphAnalyzer

from data import db_session
from data.option import Option
from data.question import Question
from data.quiz import Quiz

app = Flask('Quiz app')


def main():
    db_session.global_init("db/quizzes.sqlite")
    morph = MorphAnalyzer()

    @app.route('/')
    @app.route('/index')
    def index():
        session = db_session.create_session()
        quizzes = session.query(Quiz).all()
        return render_template('index.html', quizzes=quizzes)

    @app.route('/quiz/<int:quiz_id>')
    def quiz(quiz_id):
        session = db_session.create_session()
        quiz = session.query(Quiz).get(quiz_id)

        if not quiz:
            return 'Quiz with that id not found'

        options = request.args.getlist('options[]')
        if not options:
            options = []

        option = request.args.get('option')
        is_submitted = 'submitted' in request.args

        if not is_submitted:
            next_question = quiz.questions[0]
        else:
            if option:
                options.append(option)
            options_info = session.query(Option).filter(Option.id.in_(options)).all()
            questions_ids = [option.question_id for option in options_info]
            next_question = session.query(Question).filter(Question.quiz_id == quiz.id,
                                                           Question.id.notin_(questions_ids)).first()

            if not next_question:
                right_cnt = len(session.query(Option).filter(Option.id.in_(options), Option.is_answer).all())
                score_noun = morph.parse('балл')[0].make_agree_with_number(right_cnt).word
                return render_template('results.html', quiz=quiz, score=right_cnt, score_noun=score_noun)

        return render_template('quiz.html', quiz=quiz, question=next_question, options=options)

    @app.route('/quiz/new', methods=['GET', 'POST'])
    def add_quiz():
        if request.method == 'GET':
            return render_template('add_quiz.html')
        elif request.method == 'POST':
            name = request.form.get('quiz_name', '').strip()
            if not name:
                return "Can't create quiz with blank name"
            session = db_session.create_session()
            quiz = Quiz(name=name)
            session.add(quiz)
            session.commit()

            return redirect(url_for('edit_quiz', quiz_id=quiz.id))

    @app.route('/quiz/<int:quiz_id>/edit', methods=['GET', 'POST'])
    def edit_quiz(quiz_id):
        if request.method == 'GET':
            session = db_session.create_session()
            quiz = session.query(Quiz).get(quiz_id)
            if not quiz:
                return 'Quiz with that id not found'
            return render_template('edit_quiz.html', quiz=quiz)
        elif request.method == 'POST':
            question_text = request.form.get('question_text', '')
            if not question_text:
                return "Can't create question with blank text"

            session = db_session.create_session()
            question = Question(text=question_text, quiz_id=quiz_id)
            session.add(question)
            option = Option(text='Ответ 1', is_answer=True, question=question)
            session.add(option)
            session.commit()

            return redirect(url_for('edit_quiz', quiz_id=quiz_id))

    @app.route('/quiz/<int:quiz_id>/delete', methods=['GET'])
    def delete_quiz(quiz_id):
        session = db_session.create_session()
        quiz = session.query(Quiz).get(quiz_id)
        if not quiz:
            return 'Quiz with that id not found'
        session.delete(quiz)
        session.commit()

        return redirect(url_for('index'))

    @app.route('/question/<int:question_id>/edit', methods=['GET', 'POST'])
    def edit_question(question_id):
        session = db_session.create_session()

        if request.method == 'GET':
            question = session.query(Question).get(question_id)
            if not question:
                return 'Question with that id not found'
            return render_template('edit_question.html', question=question)
        elif request.method == 'POST':
            question = session.query(Question).get(question_id)
            if 'question_text' in request.form:
                question_text = request.form.get('question_text', '')
                if not question_text:
                    return "Can't update question text to blank"

                question.text = question_text

                right_option_id = int(request.form.get('right_option', -1))
                for option in session.query(Option).filter(Option.question_id == question_id):
                    if option.id == right_option_id:
                        option.is_answer = True
                    else:
                        option.is_answer = False

                session.commit()
            if 'option_text' in request.form:
                option_text = request.form.get('option_text', '')
                if not option_text.strip():
                    return "Can't set option text blank"
                if 'option_edit' in request.form:
                    option_id = int(request.form.get('option_id', -1))
                    option = session.query(Option).get(option_id)
                    option.text = option_text
                    session.commit()
                if 'option_delete' in request.form:
                    option_id = int(request.form.get('option_id', -1))
                    option = session.query(Option).get(option_id)
                    session.delete(option)
                    session.commit()
                elif 'option_add' in request.form:
                    is_answer = len(question.options) == 0
                    option = Option(text=option_text, question_id=question_id, is_answer=is_answer)
                    session.add(option)
                    session.commit()

            return redirect(url_for('edit_question', question_id=question_id))

    @app.route('/question/<int:question_id>/delete')
    def delete_question(question_id):
        session = db_session.create_session()

        question = session.query(Question).get(question_id)
        quiz_id = question.quiz_id
        if not question:
            return 'Question with that id not found'

        session.delete(question)
        session.commit()

        return redirect(url_for('edit_quiz', quiz_id=quiz_id))

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
    option3 = Option(text='str', question=question1, is_answer=True)
    option4 = Option(text='char', question=question1)

    session.add(option1)
    session.add(option2)
    session.add(option3)
    session.add(option4)

    question2 = Question(text='2 + 2?', quiz=quiz1)
    option1 = Option(text='2', question=question2)
    option2 = Option(text='3', question=question2)
    option3 = Option(text='4', question=question2, is_answer=True)
    option4 = Option(text='5', question=question2)

    question2.correct_option = option3

    session.add(option1)
    session.add(option2)
    session.add(option3)
    session.add(option4)

    session.commit()


if __name__ == '__main__':
    # fill_data()
    main()
