


                


@connection
def find_user(cursor, user_id=0, server_id=0):
    select_table_users = '''SELECT * FROM users WHERE id = %s and serverid = %s LIMIT 1;'''
    cursor.execute(select_table_users, (user_id, server_id))
    datarec =cursor.fetchone()
    return dict(datarec) if datarec else None

@connection_commit
def find_or_create_user(cursor, servername='', username=''):
    server = find_server(servername)
    if server is None:
        raise ValueError('Сервер {} не найден'.format(servername))
    
    def find():
        select_table_users = '''SELECT * FROM users WHERE name = %s and serverid = %s;'''
        cursor.execute(select_table_users, (username, server['serverid']))
        datarec =cursor.fetchone()
        return dict(datarec) if datarec else None

    user = find()
    if user is None:
        from time import gmtime, strftime
        logintime = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        insert_table_users = '''INSERT INTO users (name, serverid, state, login_dt)  VALUES (%s,%s,%s,%s);'''
        record_to_insert = (username, server['serverid'], 1, logintime)
        cursor.execute(insert_table_users, record_to_insert)
        cursor.connection.commit()
        
        user = find()

    return user

@connection_commit
def init_map(cursor, serverid=0, levelmap=[]):
    mapsize = len(levelmap)

    records_to_insert = []
    for row in range(mapsize):
        for col in range(mapsize):
            pos = row * 100 + col
            record_to_insert = (pos, serverid, col, row, levelmap[row][col])
            records_to_insert.append(record_to_insert)
    
    insert_table_maps = '''INSERT INTO maps (pos, serverid, col, row, obj)  VALUES %s;'''
    
    psycopg2.extras.execute_values (
        cursor, insert_table_maps, records_to_insert, template=None, page_size=100
    )    

    return True

@connection
def find_map_cell(cursor, serverid=0, row=0, col=0):
    select_table_maps = '''SELECT * FROM maps WHERE serverid = %s AND col = %s AND row = %s limit 1'''
    cursor.execute(select_table_maps, (serverid, col, row))
    datarec =cursor.fetchone()
    return dict(datarec) if datarec else None

@connection_commit
def update_map_cell(cursor, serverid=0, row=0, col=0, obj=0):
    insert_table_servers = '''UPDATE maps set obj = %s where serverid = %s and row=%s and col=%s'''
    cursor.execute(insert_table_servers, (obj, serverid, row, col))
    return cursor.rowcount