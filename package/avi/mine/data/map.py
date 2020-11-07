"""
Работа с таблицей карты уровня
"""
"""
 id    integer PRIMARY KEY,
        serverid  integer REFERENCES servers,
        userid    integer,          
        col    integer,
        row    integer,
        obj    integer
    """

from .base import *
TABLE = 'maps'

@connection_commit
def recreate_map(cursor='', serverid=0, levelmap=[], con=None):
    wheres = {'serverid': serverid}
    delete(TABLE, wheres, con=con)    

    mapsize = len(levelmap)

    records_to_insert = []
    for row in range(mapsize):
        for col in range(len(levelmap[0])):
            record_to_insert = (serverid, col, row, levelmap[row][col], -1)
            records_to_insert.append(record_to_insert)
    
    insert_table_maps = '''INSERT INTO maps (serverid, col, row, obj, userid)  VALUES %s;'''
    
    psycopg2.extras.execute_values (
        cursor, insert_table_maps, records_to_insert, template=None, page_size=100
    )    

    return cursor.rowcount


def find_cell(serverid=0, row=0, col=0, con=None):
    wheres = {'serverid': serverid, 'row': row, 'col': col}
    rec = find(table_name = TABLE, wheres = wheres, con=con)
    return rec


@connection
def find_round(cursor='', serverid=0, row=0, col=0, con=None):
    find_sql = '''SELECT * FROM maps WHERE serverid = {0} and row >= {1} and row <= {2} and col >= {3} and col <= {4};'''.format(serverid, row-1, row+1, col-1, col+1)
    cursor.execute(find_sql)
    dataset = cursor.fetchall()
    datalist = []
    for rec in dataset:
        datalist.append(dict(rec))    
    return datalist 


def find_all(serverid=0, con=None):
    return find_many(table_name=TABLE, wheres={'serverid':serverid}, con=con)


def update_cell(cell_rec={}, con=None):
    '''UPDATE maps set obj = %s where serverid = %s and row=%s and col=%s'''
    cell_rec = update(table_name = TABLE, row=cell_rec, con=con)
    return cell_rec

def update_cells(cell_recs=[], con=None):
    for rec in cell_recs:
        update_cell(rec, con)
    return cell_recs