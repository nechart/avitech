"""
Работа с таблицей серверов
"""
'''CREATE TABLE servers (
        id SERIAL PRIMARY KEY,
        name     varchar(10) NOT NULL,
        mapname  varchar(20)  NOT NULL,
        mapsize  integer,
        state    integer,
        start_dt timestamp,
        stop_dt  timestamp
        );
    '''

import json

from .base import *
TABLE = 'servers'
"""
@connection_commit
def create_server(cursor, servername=''):
    insert_table_servers = '''INSERT INTO servers (name, mapname, state, start_dt)  VALUES (%s,%s,%s,%s);'''
    from time import gmtime, strftime
    logintime = strftime("%Y-%m-%d %H:%M:%S", gmtime())    
    record_to_insert = (servername, servername, 0, logintime)
    cursor.execute(insert_table_servers, record_to_insert)
    server = cursor.fetchone()[0]
    return server

@connection_commit
def update_server_map(cursor, serverid=0, mapsize=0):
    insert_table_servers = '''UPDATE servers set mapsize = %s where serverid = %s'''
    cursor.execute(insert_table_servers, (mapsize, serverid))
    server = cursor.rowcount
    return server
"""
def find_or_create_server(servername='', con=None):
    wheres = {'name': servername}
    server_rec = find(table_name = TABLE, wheres = wheres, con = con)
    if server_rec is None:
        insert(table_name = TABLE, row = wheres, con = con)
        server_rec = find(table_name = TABLE, wheres = wheres, con = con)
    return server_rec


def find_server(servername='', con=None):
    wheres = {'name': servername}
    return find(table_name = TABLE, wheres = wheres, con = con)


def find_server_id(serverid=0, con=None):
    wheres = {'id': serverid}
    return find(table_name = TABLE, wheres = wheres, con = con)


def update_server(server_rec={}, con=None):
    server_rec = update(table_name = TABLE, row = server_rec, con = con)
    return server_rec

def read_params(server_rec):
    params = json.loads(server_rec['params'])
    return params 