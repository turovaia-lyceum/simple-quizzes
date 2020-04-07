import sqlalchemy as sa
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class Question(SqlAlchemyBase):
    __tablename__ = 'question'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    text = sa.Column(sa.String)

    quiz_id = sa.Column(sa.Integer, sa.ForeignKey('quiz.id'))
    quiz = orm.relation('Quiz')

    options = orm.relation("Option", back_populates='question')

    def __repr__(self):
        return f'<Question> {self.id} {self.text}'
