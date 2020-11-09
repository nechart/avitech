from .enums import *
from .client import Client
from . import map
"""
game = Player(server_name) 
game.play() # отобразить игру. статус игрока меняется на 1
while game.active():  # active проверяет статус сервера и игрока. если сервер выключился - выходит, если игрок умер (статус 2, выполняем game.reconnect()
    objs = game.get_objs() # select from map
    game.move('right')
"""

class Player():
    def __init__(self, server_name, ava = avatar.cowboy):
        self.client = Client()
        self.client.connect(server_name, ava)

    def active(self):
        # проверить статус сервера и игрока
        self.client.refresh_user()
        self.client.refresh_server()
        return self.client.check_state()

    def play(self):
        # запустить игру
        self.client.start()

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

    def pick(self):
        # взять сокровище
        return self.client.make_action(action.pick) 

    def hide(self):
        # спрятаться
        return self.client.make_action(action.hide) 

    def get_pos(self):
        # получить координаты игрока (row,col)
        self.client.refresh_user()
        return (self.client.user['row'], self.client.user['col'])

    def get_objs(self):
        # осмотреться
        self.client.refresh_user()
        return map.get_objs(self.client.server, self.client.user['row'], self.client.user['col'], con=self.client.con)

    def get_chests(self):
        # получить список координат сокровищ [(row1, col1), (row2, col2)]
        cells = map.get_objs_by_type(serverid = self.client.server['id'], obj_type=obj.chest, con=self.client.con)
        chests = []
        for cell in cells:
            chests.append((cell['row'], cell['col']))
        return chests

    def get_guards(self):
        # получить список координат стражей [(row1, col1), (row2, col2)]
        cells = map.get_objs_by_type(serverid = self.client.server['id'], obj_type=obj.guard, con=self.client.con)
        chests = []
        for cell in cells:
            chests.append((cell['row'], cell['col']))
        return chests        

    def get_players(self):
        # получить список координат игроков [(row1, col1), (row2, col2)]
        cells = map.get_objs_by_type(serverid = self.client.server['id'], obj_type=obj.player, con=self.client.con)
        chests = []
        for cell in cells:
            chests.append((cell['row'], cell['col']))
        return chests                

    def get_walls(self):
        # получить список координат препятствий [(row1, col1), (row2, col2)]
        cells = map.get_objs_by_type(serverid = self.client.server['id'], obj_type=obj.wall, con=self.client.con)
        chests = []
        for cell in cells:
            chests.append((cell['row'], cell['col']))
        return chests                        