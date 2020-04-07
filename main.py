from flask import Flask

from data import db_session

app = Flask('Quiz app')


def main():
    db_session.global_init("db/quizzes.sqlite")

    @app.route('/')
    @app.route('/quizzes')
    def index():
        return ''

    app.run()


if __name__ == '__main__':
    main()
