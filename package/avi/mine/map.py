import random
from .data.map import *
from .enums import *

def get_all(server_rec, con=None):
    maprecs = find_all(server_rec['id'], con)
    maplist = [[0] * server_rec['mapsize_x'] for irow in range(server_rec['mapsize_y'])]
    for rec in maprecs:
        maplist[rec['row']][rec['col']] = rec #['obj']
    return maplist

def get_all_objs(server_rec, con=None):
    maprecs = find_all(server_rec['id'], con)
    maplist = [[0] * server_rec['mapsize_x'] for irow in range(server_rec['mapsize_y'])]
    for rec in maprecs:
        maplist[rec['row']][rec['col']] = rec['obj']
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
            maplist['right'] = rec['obj']

    return maplist

def find_empty_place(server_rec, con=None):
    attempt = 0
    x, y = -1, -1
    while attempt < 5:
        y = random.randint(0, server_rec['mapsize_y']-1)
        x = random.randint(0, server_rec['mapsize_x']-1)
        cell = find_cell(serverid=server_rec['id'], row=y, col=x, con=con)
        if cell['obj'] != obj.space:
            continue
        objs = get_objs(server_rec=server_rec, row=y, col=x, con=con)
        if max(objs.values()) == obj.space:
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
    return row  >= 0 and row < server_rec['mapsize_y'] and col  >= 0 and col < server_rec['mapsize_x']
    
def get_objs_by_type(serverid=0, obj_type=obj.space, con=None):
    cells = find_many(table_name='maps', wheres={'serverid':serverid, 'obj':obj_type}, con=con)
    return cells

def get_guard_cell(serverid=0, guardid=0, con=None):
    return find(table_name='maps', wheres={'serverid':serverid, 'obj':obj.guard, 'userid':guardid}, con=con)

def find_path(server_rec, pos, pos_goal, con=None):
    # https://www.cyberforum.ru/python/thread2021804.html
    def searсh_path(data, pos=(), pos_goal=(), server_rec={}, short_path={}, full_path={}, count=0): 
                                                               #data-лабиринт; х,у - точка, где мы сейчас находимся
                                                               #short_path - {key=точка куда идём: value=откуда идём}
                                                               #full_path - {key=точка : value=кол-во шагов до точки}
                                                               #count - номер шага
        full_path[pos] = count # Записываем точку и сколько шагов до неё на данном этапе
        if pos == pos_goal: # Точка выхода из лабиринта
            return full_path, short_path
        walks = [(-1,0),(0, 1),(1, 0),(0, -1)] 
        for walk_Y, walk_X in walks:
            row, col = pos[0] + walk_Y, pos[1] + walk_X
            if check_coords(server_rec, row, col) and data[row][col] != obj.wall: # Если ячейка свободна
                                                                                   # и мы не вышли за границы лабиринта
                check = full_path.get((row, col)) # Смотрим на точку, куда хотим пойти и сколько до неё шагов
                                                           # Если check=None, значит в точке ещё не были
                if check!=None and check>count: # Если мы были уже в этой точке и расстояние до неё больше, чем номер шага
                                                # на данном этапе
                    full_path[(row, col)] = count # Перезаписываем full_path, т.к нашли более короткую дистанцию
                    short_path[(row, col)] = (pos[0], pos[1]) # Пепрезаписываем short_path, потому что нашли точку, из
                                                              # которой в данную можно попасть короче
                    searсh_path(data, (row, col), pos_goal, server_rec, short_path, full_path, count+1) # Увеличиваем шаг и запускаем
                                                                                                        # рекурсивно функцию
                else:
                    if (row, col) not in full_path.keys(): # Если в токе, куда собираемся пойти еще не были
                        short_path[(row, col)] = (pos[0], pos[1]) # записываем {куда идём:откуда идём}
                        searсh_path(data, (row, col), pos_goal, server_rec, short_path, full_path, count+1) # запускаем рекурсию с шагом +1
   
        return full_path, short_path

    def short_path(data, path=[], start=(3,1), end=(3,7)): # Сюда прилетает short_path из search_path, когда нашли выход
                                                        # data=short_path, start - координата точки входа, end - выхода
                                                        # path - короткий путь в виде списка координат из лабиринта
        """Здесь мы рекурсивно пробегаемся из конечной точки в начальную, восстанавливая путь по лабиринту:
        берём {точка, куда пришли(допустим А) : точка откуда пришли (в точку А) - Б}"""
        if len(path)==0:
            path.append(end)
        path.append(data[end])
        if data[end]==start:
            return path
        else:
            short_path(data, path, start, data[end])
        return path
    
    paths = searсh_path(get_all_objs(server_rec, con=con), pos, pos_goal, server_rec)
    if paths is None:
        return []

    short = short_path(paths[1], start=pos, end=pos_goal)    
    short.reverse()
    return short


