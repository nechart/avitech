"""
Работа с таблицей пользователей
"""
'''        id     SERIAL PRIMARY KEY,
        name   varchar(20) NOT NULL,
        serverid integer REFERENCES servers,
        login_dt timestamp,
        score  integer,
        kills  integer,
        state  integer,
        col    integer,
        row    integer,
    '''

from .base import *
TABLE = 'users'

def find_user(userid=0, con=None):
    wheres = {'id': userid}
    user_rec = find(table_name = TABLE, wheres = wheres, con=con)
    return user_rec


def find_all_users(serverid=0, con=None):
    wheres = {'serverid': serverid}
    user_set = find_many(table_name = TABLE, wheres = wheres, con=con)
    return user_set


def find_or_create_user(serverid=0, username='', con=None):
    wheres = {'serverid': serverid, 'name': username}
    user_rec = find(table_name = TABLE, wheres = wheres, con=con)
    if user_rec is None:
        user_rec = insert(table_name = TABLE, row = wheres, con=con)
        user_rec = find(table_name = TABLE, wheres = wheres, con=con)
    return user_rec


def update_user(user_rec={}, con=None):
    user_rec = update(table_name = TABLE, row = user_rec, con=con)
    return user_rec


def delete_users(serverid=0, con=None):
    wheres = {'serverid': serverid}
    return delete(table_name = TABLE, wheres = wheres, con=con)