import sqlalchemy as sa
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class Option(SqlAlchemyBase):
    __tablename__ = 'option'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    text = sa.Column(sa.String)

    question_id = sa.Column(sa.Integer, sa.ForeignKey('question.id'))
    question = orm.relation('Quiz')

    def __repr__(self):
        return f'<Option> {self.id} {self.text}'
