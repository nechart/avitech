"""
Работа с таблицей тестов
"""
'''CREATE TABLE quizzes (
        id SERIAL PRIMARY KEY,
        quizname  varchar(20) NOT NULL,
        username  varchar(20) NOT NULL,
        topic     varchar(20) NOT NULL,
        rate      float
        );
    '''

from ..mine.data.base import *

TABLE = 'quizzes'

def find_quizzes(quizname, con=None):
    wheres = {'quizname': quizname}
    quiz_set = find_many(table_name = TABLE, wheres = wheres, con=con)
    return quiz_set

def insert_quiz(quizname, username, topicname, rate, con=None):
    wheres = {'quizname': quizname, 'username': username, 'topic': topicname, 'rate': rate}
    user_rec = insert(table_name = TABLE, row = wheres, con=con)
    return user_rec

def delete_quiz(quizname, con=None):
    wheres = {'quizname': quizname}
    user_rec = delete(table_name = TABLE, wheres = wheres, con=con)
    return user_rec

def delete_quiz_user(quizname, username, con=None):
    wheres = {'quizname': quizname, 'username': username}
    user_rec = delete(table_name = TABLE, wheres = wheres, con=con)
    return user_rec    