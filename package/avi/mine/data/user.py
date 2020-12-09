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
import json

from .base import *
TABLE = 'users'
TABLE_SETUP = 'usersetup'

def find_user(userid=0, con=None):
    wheres = {'id': userid}
    user_rec = find(table_name = TABLE, wheres = wheres, con=con)
    return user_rec


def find_user_by_name(name='', serverid=0, con=None):
    wheres = {'name': name, 'serverid': serverid}
    user_rec = find(table_name = TABLE, wheres = wheres, con=con)
    return user_rec


def find_all_users(serverid=0, con=None):
    wheres = {'serverid': serverid}
    user_set = find_many(table_name = TABLE, wheres = wheres, con=con)
    return user_set


def find_or_create_user(serverid=0, username='', ava='', team=0, con=None):
    wheres = {'serverid': serverid, 'name': username}
    user_rec = find(table_name = TABLE, wheres = wheres, con=con)
    if user_rec is None:  
        row = wheres.copy()
        row['avatar'] = ava
        row['state'] = 0
        row['score'] = 0
        row['kills'] = 0
        row['team'] = team
        user_rec = insert(table_name = TABLE, row = row, con=con)
        user_rec = find(table_name = TABLE, wheres = wheres, con=con)
    elif ava != user_rec['avatar']:
        user_rec['avatar'] = ava
    elif team != user_rec['team']:
        user_rec['team'] = team
        update_user(user_rec, con)
    return user_rec


def update_user(user_rec={}, con=None):
    user_rec = update(table_name = TABLE, row = user_rec, con=con)
    return user_rec


def delete_users(serverid=0, con=None):
    wheres = {'serverid': serverid}
    return delete(table_name = TABLE, wheres = wheres, con=con)

# user setup
def set_user_setup(username='', ava='', con=None):
    user_setup = find_user_setup(username, con=con)
    if user_setup is None:  
        row = {}
        row['username'] = username
        row['avatar'] = ava
        user_setup = insert(table_name = TABLE_SETUP, row = row, con=con)
    else:
        user_setup['avatar'] = ava
        user_setup = update(table_name = TABLE_SETUP, row = user_setup, con=con)
    return user_setup


def find_user_setup(username='', con=None):
    wheres = {'username': username}
    user_setup = find(table_name = TABLE_SETUP, wheres = wheres, con=con)
    return user_setup

def read_params(params_field):
    params = json.loads(params_field)
    return params 

def write_params(params):
    return json.dumps(params)

BULLETS = 4
SPACES = 3

def init_params():
    user_params = {}
    user_params['hands'] = 0
    user_params['bullets'] = BULLETS
    user_params['spaces'] = SPACES
    return user_params