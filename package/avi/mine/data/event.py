"""
Работа с таблицей событий
"""
"""
        id    SERIAL PRIMARY KEY,
        serverid  integer REFERENCES servers,
        userid    integer REFERENCES users,    
        event_dt  timestamp,
        action    integer,
        state     integer
    """
from time import gmtime, strftime
from time import sleep


from .base import *
from ..enums import *
TABLE = 'events'
EVENT_WAIT_LAG = 0.2

def find_event(eventid, con=None):
    wheres = {'id': eventid}
    rec = find(table_name = TABLE, wheres = wheres, con=con)
    return rec


def find_events(serverid=0, state=action_state.to_process, con=None):
    wheres = {'serverid': serverid, 'state': state}
    recs = find_many(table_name = TABLE, wheres = wheres, orders='event_dt', con=con)
    return recs


def update_event(row={}, con=None):
    return update(table_name = TABLE, row=row, con=con)

def delete_events(serverid=0, con=None):
    wheres = {'serverid': serverid}
    return delete(table_name = TABLE, wheres=wheres, con=con)

def insert_event(serverid=0, userid=0, action=action.spawn, con=None):
    rec = {}
    rec['serverid']=serverid
    rec['userid']=userid
    rec['action']=action
    logintime = strftime("%Y-%m-%d %H:%M:%S", gmtime())    
    rec['event_dt'] =  logintime
    rec['state']=action_state.to_process

    return insert(table_name = TABLE, row=rec, con=con)

def send_event(serverid=0, userid=0, action=action.spawn, con=None):
    eventid = insert_event(serverid=serverid, userid=userid, action=action, con=con)
    event_rec = None
    while True:
        sleep(EVENT_WAIT_LAG)
        event_rec = find_event(eventid, con)
        if event_rec['state'] >= action_state.processed:
            break
    return event_rec['state']