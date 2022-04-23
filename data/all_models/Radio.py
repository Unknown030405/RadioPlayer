import datetime
import sqlalchemy
from data.db_session import SqlAlchemyBase


class Radio(SqlAlchemyBase):
    __tablename__ = 'radios'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    srce = sqlalchemy.Column(sqlalchemy.String, nullable=True)
