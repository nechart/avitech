"""
Создание БД

"""

from .base import *

@connection_commit
def drop_tables(cursor, con=None):
    drop_table_servers = '''DROP TABLE IF EXISTS maps;'''
    cursor.execute(drop_table_servers)
    drop_table_servers = '''DROP TABLE IF EXISTS events;'''
    cursor.execute(drop_table_servers)
    drop_table_servers = '''DROP TABLE IF EXISTS users;'''
    cursor.execute(drop_table_servers)
    drop_table_servers = '''DROP TABLE IF EXISTS servers;'''
    cursor.execute(drop_table_servers)


@connection_commit_test
def create_tables(cursor, con=None):
    create_table_servers = '''CREATE TABLE servers (
        id SERIAL PRIMARY KEY,
        name     varchar(20) NOT NULL,
        mapname  varchar(20),
        mapsize_x integer,
        mapsize_y integer,
        state    integer,
        start_dt timestamp,
        stop_dt  timestamp
        );
    '''
    cursor.execute(create_table_servers)

    create_table_users = '''CREATE TABLE users (
        id     SERIAL PRIMARY KEY,
        name   varchar(20) NOT NULL,
        serverid integer REFERENCES servers,
        avatar varchar(20),
        login_dt timestamp,
        score  integer,
        kills  integer,
        state  integer,
        row    integer,
        col    integer        
        );
    '''
    cursor.execute(create_table_users)

    cursor.execute('CREATE UNIQUE INDEX name_idx ON users (serverid, name);')

    create_table_maps = '''CREATE TABLE maps (
        id    SERIAL PRIMARY KEY,
        serverid  integer REFERENCES servers,
        userid    integer,          
        row    integer,
        col    integer,
        obj    integer,
        image  varchar(20)
        );
    '''
    cursor.execute(create_table_maps)

    cursor.execute('CREATE UNIQUE INDEX pos_idx ON maps (serverid, row, col);')

    cursor.execute('CREATE INDEX obj_idx ON maps (serverid, obj);')

    create_table_events = '''CREATE TABLE events (
        id    SERIAL PRIMARY KEY,
        serverid  integer REFERENCES servers,
        userid    integer,    
        event_dt  timestamp,
        action    integer,
        state     integer
        );
    '''
    cursor.execute(create_table_events)

    print("Tables created successfully in dbase {}".format(DB))
