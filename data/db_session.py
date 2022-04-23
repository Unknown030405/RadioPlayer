import sqlalchemy
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Invalid database file name")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Connection to data base via {conn_str}")

    engine = sqlalchemy.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from data import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> sqlalchemy.orm.Session:
    global __factory
    return __factory()
