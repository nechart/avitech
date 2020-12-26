import psycopg2
import psycopg2.extras
from psycopg2.extensions import AsIs
DB = "labdb"

def connect(db=DB):
    return psycopg2.connect(user = "jupyter", password = "jupMaxim80", database = DB) 

def connection(func):
    def wrapper(*args, **kwargs):
        try:
            con = kwargs.get("con") if 'con' in kwargs else None
            if con is None:
                con = connect()
            cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
            ret = func(cursor, *args, **kwargs)
        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)
        finally:
            #closing database connection.
                if(con):
                    cursor.close()
                    #con.close()    
        return ret                    
    return wrapper


def connection_commit(func):
    def wrapper(*args, **kwargs):
        try:
            con = kwargs.get("con") if 'con' in kwargs else None
            if con is None:
                con = connect()
            cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
            ret = func(cursor, *args, **kwargs)
            con.commit()
        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)
        finally:
            #closing database connection.
                if(con):
                    cursor.close()
                    #con.close()    

        return ret                    
    return wrapper


def connection_test(func):
    def wrapper(*args, **kwargs):
        connection = connect()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        ret = func(cursor, *args, **kwargs)
        if(connection):
            cursor.close()
            connection.close()    
        return ret                    
    return wrapper


def connection_commit_test(func):
    def wrapper(*args, **kwargs):
        connection = connect()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        ret = func(cursor, *args, **kwargs)
        connection.commit()
        if(connection):
            cursor.close()
            connection.close()    
        return ret
    return wrapper

"""
def find(table_name='', wheres={}, con = None):
    if con is None:
        con = psycopg2.connect(user = "postgres", password = "nartPos_80", database = DB)
    cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    where_list = ["{0} = %s".format(k) for k in wheres.keys()]
    where_str = ' and '.join(where_list)
    find_sql = '''SELECT * FROM {0} WHERE {1};'''.format(table_name, where_str)
    cursor.execute(find_sql, tuple(wheres.values()) )
    datarec =cursor.fetchone()
    cursor.close()
    return dict(datarec) if datarec else None
"""

@connection
def find(cursor='', table_name='', wheres={}, con = None):
    where_list = ["{0} = %s".format(k) for k in wheres.keys()]
    where_str = ' and '.join(where_list)
    find_sql = '''SELECT * FROM {0} WHERE {1} LIMIT 1;'''.format(table_name, where_str)
    cursor.execute(find_sql, tuple(wheres.values()) )
    datarec =cursor.fetchone()
    return dict(datarec) if datarec else None


@connection
def find_many(cursor='', table_name='', wheres={}, orders=None, con = None):
    where_list = ["{0} = %s".format(k) for k in wheres.keys()]
    where_str = ' and '.join(where_list)
    find_sql = '''SELECT * FROM {0} WHERE {1}'''.format(table_name, where_str)
    find_sql += ' ORDER BY {};'.format(orders) if not orders is None else ';'
         
    cursor.execute(find_sql, tuple(wheres.values()) )
    dataset =cursor.fetchall()
    datalist = []
    for rec in dataset:
        datalist.append(dict(rec))    
    return datalist 

@connection_commit
def insert(cursor='', table_name='', row={}, con = None):
    # https://stackoverflow.com/questions/29461933/insert-python-dictionary-using-psycopg2
    """insert row"""
    columns = row.keys()
    values = row.values() #[row[column] for column in columns]
    insert_statement = 'insert into {0} (%s) values %s RETURNING id'.format(table_name)
    #print(cursor.mogrify(insert_statement, (AsIs(','.join(columns)), tuple(values))))
    cursor.execute(insert_statement, (AsIs(','.join(columns)), tuple(values)))
    return cursor.fetchone()[0]


@connection_commit
def update(cursor='', table_name='', row={}, con = None):
    """update row"""
    columns = row.keys()
    values = (tuple(row.values()),)
    update_statement = 'update {0} set ({1}) = %s where id = {2}'.format(table_name, ', '.join(columns), row['id']) # (AsIs(','.join(columns)), 
    cursor.execute(update_statement, values)
    return cursor.rowcount


@connection_commit
def delete(cursor='', table_name='', wheres={}, con = None):
    """delete rows"""
    where_list = ["{0} = %s".format(k) for k in wheres.keys()]
    where_str = ' and '.join(where_list)
#    values = (tuple(wheres.values()),)
    values = tuple(wheres.values())
    delete_query = 'DELETE FROM {0} WHERE {1};'''.format(table_name, where_str)
    cursor.execute(delete_query, values)
    return cursor.rowcount