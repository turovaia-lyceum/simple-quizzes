import sqlalchemy as sa
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class Quiz(SqlAlchemyBase):
    __tablename__ = 'quiz'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String)

    questions = orm.relation("Question", back_populates='quiz')

    def __repr__(self):
        return f'<Quiz> {self.id} {self.name}'
