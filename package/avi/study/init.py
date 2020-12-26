"""
Создание таблиц учебного модуля в БД

"""

from ..mine.data.base import *

@connection_commit
def drop_tables(cursor, con=None):
    drop_table_servers = '''DROP TABLE IF EXISTS quizzes;'''
    cursor.execute(drop_table_servers)
    return

@connection_commit
def create_tables(cursor, con=None):
    create_table_servers = '''CREATE TABLE quizzes (
        id SERIAL PRIMARY KEY,
        quizname  varchar(20) NOT NULL,
        username  varchar(20) NOT NULL,
        topic     varchar(20) NOT NULL,
        rate      float
        );
    '''
    cursor.execute(create_table_servers)

    cursor.execute('CREATE UNIQUE INDEX quiz_name_idx ON quizzes (quizname, username, topic);')    
    return


    print("Tables created successfully in dbase {}".format(DB))
