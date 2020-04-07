from flask import Flask

app = Flask('Quiz app')


def main():
    @app.route('/')
    @app.route('/quizzes')
    def index():
        return ''

    app.run()


if __name__ == '__main__':
    main()
