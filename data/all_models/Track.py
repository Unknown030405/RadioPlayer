import datetime
import sqlalchemy
from data.db_session import SqlAlchemyBase


class Track(SqlAlchemyBase):
    __tablename__ = 'tracks'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    author = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    srce = sqlalchemy.Column(sqlalchemy.String, nullable=True)
