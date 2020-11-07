import random
from .data.map import *
from .enums import *

def get_all(server_rec, con=None):
    maprecs = find_all(server_rec['id'], con)
    maplist = [[0] * server_rec['mapsize_x'] for irow in range(server_rec['mapsize_y'])]
    for rec in maprecs:
        maplist[maprecs['row']][maprecs['col']] = maplist['obj']
    return maplist

def get_objs(server_rec, row=0, col=0, con=None):
    maprecs = find_round(serverid=server_rec['id'], row=row, col=col, con=con)
    maplist = {'left':0, 'up':0, 'down':0, 'right':0}
    for rec in maprecs:
        if rec['row'] == row and rec['col'] == col - 1:
            maplist['left'] = rec['obj']
        if rec['row'] == row-1 and rec['col'] == col:
            maplist['up'] = rec['obj']
        if rec['row'] == row+1 and rec['col'] == col:
            maplist['down'] = rec['obj']
        if rec['row'] == row and rec['col'] == col + 1:
            rec['right'] = rec['obj']

    return maplist

def find_empty_place(server_rec, con=None):
    attempt = 0
    x, y = -1, -1
    while attempt < 5:
        y = random.randint(0, server_rec['mapsize_y']-1)
        x = random.randint(0, server_rec['mapsize_x']-1)
        objs = get_objs(server_rec=server_rec, row=y, col=x, con=con)
        if max(objs.values()) == 1:
            break
        attempt += 1
    return (y,x)

def change_cells(serverid=0, cell_1=tuple(), cell_2=tuple(), con=None):
    cell1_rec= find_cell(serverid=serverid, row=cell_1[0], col=cell_1[1], con=con)
    cell2_rec= find_cell(serverid=serverid, row=cell_2[0], col=cell_2[1], con=con)
    cell1_rec['obj'], cell1_rec['userid'], cell2_rec['obj'], cell2_rec['userid'] = cell2_rec['obj'], cell2_rec['userid'], cell1_rec['obj'], cell1_rec['userid']
    cell1_rec['image'], cell2_rec['image'] = cell2_rec['image'], cell1_rec['image']
    update_cell(cell1_rec)
    update_cell(cell2_rec)


def check_coords(server_rec, row, col):
    return row  >= 0 and row < server_rec['mapsize_y'] and col  >= 0 and row < server_rec['mapsize_x']
    
def get_objs_by_type(serverid=0, obj_type=obj.space, con=None):
    cells = find_many(table_name='maps', wheres={'serverid':serverid, 'obj':obj_type}, con=con)
    return cells
