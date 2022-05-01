import sqlalchemy
from data.db_session import SqlAlchemyBase

association_table = sqlalchemy.Table(
    'association',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('users', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('radios', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('radios.id'))
)


class Radio(SqlAlchemyBase):
    __tablename__ = 'radios'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    srce = sqlalchemy.Column(sqlalchemy.String, nullable=True)
