from sqlalchemy import create_engine
from machine.analysis import DatabaseConnectionSettings


def get_db_connection(AI_CURSOR=False, BRAINDATA_CURSOR=False):
    """ Return DB connection for insert data to SQLite/MySQL. default: sqlite
        :return: SqlAlchemy connection object
        See also: settings.DB_CONNECTION_STRING
    """

    # settings.DB_AI_CONNECTION_STRING is a string for connction
    # Example: mysql://user:password@host/data_base_name?charset=utf8
    if AI_CURSOR:
        engine = create_engine(DatabaseConnectionSettings.DB_AI_CONNECTION_STRING)
    elif BRAINDATA_CURSOR:
        engine = create_engine(DatabaseConnectionSettings.DB_BRAINDATA_CONNECTION_STRING)
    else:
        raise Exception("Choose one flag AI_CURSOR or BRAINDATA_CURSOR")

    connection = engine.connect()

    # setup UTF-8 support
    setup_utf8_support(connection)

    return connection


def setup_utf8_support(dbc):
    """ Setup UTF-8 support
    :param dbc DBConnection
    """
    # dbc.set_character_set('utf8')
    dbc.execute('SET NAMES utf8;')
    dbc.execute('SET CHARACTER SET utf8;')
    dbc.execute('SET character_set_connection=utf8;')
