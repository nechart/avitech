from .enums import *
from .client import Client
from .server import Server
from . import map
from .data import user

import getpass
"""
game = Player(server_name) 
game.play() # отобразить игру. статус игрока меняется на 1
while game.active():  # active проверяет статус сервера и игрока. если сервер выключился - выходит, если игрок умер (статус 2, выполняем game.reconnect()
    objs = game.get_objs() # select from map
    game.move('right')
"""

class Player():
    def __init__(self, server_name, ava=None, user_name = None):
        self.client = Client(user_name)
        self.client.connect(server_name, ava)

    def active(self):
        # проверить статус сервера и игрока
        self.client.refresh_user()
        self.client.refresh_server()
        return self.client.check_state()

    def play(self, autostop = False):
        # запустить игру
        self.client.start(autostop)

    def move_right(self):
        # идти вправо
        return self.client.make_action(action.move_right)

    def move_left(self):
        # идти влево
        return self.client.make_action(action.move_left) 

    def move_up(self):
        # идти вверх
        return self.client.make_action(action.move_up) 

    def move_down(self):
        # идти вниз
        return self.client.make_action(action.move_down) 

    def move(self, dir):
        try:
            # двигаться. dir: right, left, down, up
            if dir == 'up':
                return self.move_up()
            elif dir == 'down':
                return self.move_down()
            elif dir == 'left':
                return self.move_left()
            elif dir == 'right':
                return self.move_right()
            return False
        except:
            raise Exception("Игра прервана")

    def pick(self):
        try:
        # взять сокровище
            return self.client.make_action(action.pick) 
        except:
            raise Exception("Игра прервана")

    def hide(self):
        # спрятаться
        return self.client.make_action(action.hide) 

    def get_pos(self):
        try:
            # получить координаты игрока (row,col)
            self.client.refresh_user()
            return (self.client.user['row'], self.client.user['col'])
        except:
            raise Exception("Игра прервана")

    def get_objs(self):
        try:
            # осмотреться
            self.client.refresh_user()
            return map.get_objs(self.client.server, self.client.user['row'], self.client.user['col'], con=self.client.con)
        except:
            raise Exception("Игра прервана")

    def get_chests(self):
        try:
            # получить список координат сокровищ [(row1, col1), (row2, col2)]
            cells = map.get_objs_by_type(serverid = self.client.server['id'], obj_type=obj.chest, con=self.client.con)
            chests = []
            for cell in cells:
                chests.append((cell['row'], cell['col']))
            return chests
        except:
            raise Exception("Игра прервана")

    def get_guards(self):
        try:        
            # получить список координат стражей [(row1, col1), (row2, col2)]
            cells = map.get_objs_by_type(serverid = self.client.server['id'], obj_type=obj.guard, con=self.client.con)
            chests = []
            for cell in cells:
                if cell['image'] != ava_guard.killed:
                    chests.append((cell['row'], cell['col']))
            return chests        
        except:
            raise Exception("Игра прервана")

    def get_players(self):
        # получить список координат игроков [(row1, col1), (row2, col2)]
        cells = map.get_objs_by_type(serverid = self.client.server['id'], obj_type=obj.player, con=self.client.con)
        chests = []
        for cell in cells:
            user_rec = user.find_user(cell['userid'], con=self.client.con)
            if user_rec['state'] == player_state.active:
                chests.append((cell['row'], cell['col']))
        return chests    

    def get_player(self, name):
        # получить координату игрока (row1, col1)
        user_loc = user.find_user_by_name(name, con=self.client.con)
        return None if not user_loc else (user_loc['row'], user_loc['col'])

    def get_walls(self):
        # получить список координат препятствий [(row1, col1), (row2, col2)]
        cells = map.get_objs_by_type(serverid = self.client.server['id'], obj_type=obj.wall, con=self.client.con)
        chests = []
        for cell in cells:
            chests.append((cell['row'], cell['col']))
        return chests                        

    def get_dir(self, pos_goal):
        """ Функция определения направления движения игрока
        Параметры:
        pos_user - кортеж с координатой игрока
        pos_goal - кортеж с координатой цели
        Возвращаемое значение:
        dir - строка с кодом направления "up", "down", "left", "right"
        """
        try:        
            pos_user = (self.client.user['row'], self.client.user['col'])
            delta_row = pos_goal[0] - pos_user[0]    # вычислить разницу строк
            delta_col = pos_goal[1] - pos_user[1]    # вычислить разницу столбцов
            dir = ""
            
            if abs(delta_row) > abs(delta_col):  # если по вертикали идти больше, чем по горизонтали - идем вверх или вниз
                if delta_row < 0:
                    dir = "up"
                elif delta_row > 0:
                    dir = "down"
            else:
                if delta_col < 0:
                    dir = "left"
                elif delta_col > 0:
                    dir = "right"
            return dir    
        except:
            raise Exception("Игра прервана")
    
    def get_path(self, pos_goal = (0,0)):
        """найти кратчайший путь с учетом препятствий
        params:
        pos_goal - координаты цели
        return:
        список ячеек, по которым следует идти
        """
        try:                
            return map.find_path(self.client.server, (self.client.user['row'], self.client.user['col']), pos_goal, con=self.client.con)
        except:
            raise Exception("Игра прервана")

    def get_nearest(self, objects):
        "Найти ближайший объект из списка"
        try:                
            import numpy
            import builtins
            pos = (self.client.user['row'], self.client.user['col'])
            delta_pos = list(builtins.map(lambda x: tuple(numpy.subtract(x, pos)), objects))
            deltas = list(builtins.map(lambda x:abs(x[0]) + abs(x[1]), delta_pos))
            return objects[deltas.index(min(deltas))]
        except:
            raise Exception("Игра прервана")


def play_server(config, ava=None):
    servername = getpass.getuser() + '_server'
    server = Server.create(servername)
    server.init_map(config)
    server.launch()
    player = Player(servername, ava)
    player.client.server_obj = server
    return player