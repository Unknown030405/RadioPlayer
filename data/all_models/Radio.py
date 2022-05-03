import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase

association_table = sqlalchemy.Table(
    'association',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('radios', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('radios.id')),
    sqlalchemy.Column('users'
                      , sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id'))
)


class Radio(SqlAlchemyBase):
    __tablename__ = 'radios'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    source = sqlalchemy.Column(sqlalchemy.String, nullable=True)
