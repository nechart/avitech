from ..survive.player import Player as basePlayer
from ..mine.enums import *
from .server import Server
#from .client import Client
import getpass
from ..mine import map

from ..mine.data import user

# Создадим словарь направлений для обхода по часовой стрелке:
next_dir = {'up':'right', 'right':'down', 'down':'left', 'left':'up'}

class Player(basePlayer):
    def __init__(self, server_name, ava=None, user_name=None, team=0):
        super().__init__(server_name, ava=ava, user_name=user_name, team=team)

    def put(self):
        # положить на склад
        return self.client.make_action(action.put)

    def get_bullets(self):
        """ Получить количество пуль
        """
        params = user.read_params(self.client.user['params'])
        return params['bullets']

    def get_spaces(self):
        """ Получить количество мест в рюкзаке
        """
        params = user.read_params(self.client.user['params'])
        return params['spaces']

    def get_location_pos(self, team=None):
        """ Получить координаты склада
        """
        if team is None:
            team = self.client.user['team']
        [row, col] = self.client.serv_params['teams'][team]['location'] 
        return (row, col)

    def get_zone_cols(self, team=None):
        """ Получить колонки зоны племени
        """
        if team is None:
            team = self.client.user['team']
        [col1, col2] = self.client.serv_params['teams'][team]['cols'] 
        return (col1, col2)


    def get_players(self, team=None):
        # получить координаты игроков команды {name1:(row1, col1), name2:(row2, col2)}
        cells = map.get_objs_by_type(serverid = self.client.server['id'], obj_type=obj.player, con=self.client.con)
        players = {}
        for cell in cells:
            if not team is None:
                if user_rec['team'] != team:
                    continue
            user_rec = user.find_user(cell['userid'], con=self.client.con)
            if user_rec['state'] == player_state.active:
                players[user_rec['name']] = (cell['row'], cell['col'])
        return players    

    def action_hunt(self, rows=None, cols=None):
        """ Охотиться на ближайшего моба"""
        objs = self.get_objs()  # осмотреться
        if obj.guard in objs.values():   # проверить, есть ли страж по близости. 
            self.hide()  # если да, спрятаться
            return

        guards = self.get_guards()
        pos = self.get_pos()
        # исключаем ближайших стражей - чтоб не подходить к ним вплотную:
        if not cols is None:
            guards = [chest for chest in guards if chest[1] >= cols[0] and chest[1] <= cols[1]]
        if not rows is None:
            guards = [chest for chest in guards if chest[0] >= rows[0] and chest[0] <= rows[1]]

        guards = [guard for guard in guards if (abs(guard[0] - pos[0]) > 1) or (abs(guard[1] - pos[1]) > 1)]
        steps = self.find_shoot_pos(guards) # получить ближайшие позиции для стрельбы
        if steps: # проверить, что список позиций непустой
            (step_num, step_dir) = steps[0] # взять первую позицию из списка (число шагов, направление)
            for _ in range(step_num): # цикл на число шагов
                if not self.move(step_dir):    # движение в нужном направлении
                    self.move(next_dir[step_dir])

        goals = self.get_goals(guards) # здесь игрок должен быть уже на позиции, проверим, есть ли цели для стрельбы
        if goals:  # если цели есть (список не пустой)
            dir = self.get_dir(goals[0])  # получить направление выстрела для первой по близости цели
            if dir:                     # проверить, что направление выбрано
                self.shoot(dir)          # выполнить выстрел        

    def action_collect(self, rows=None, cols=None):
        """ Cобрать ближайший ресурс"""
        objs = self.get_objs()  # осмотреться
        if obj.guard in objs.values():   # проверить, есть ли страж по близости. 
            self.hide()  # если да, спрятаться
            return

        chests = self.get_chests()
        if not cols is None:
            chests = [chest for chest in chests if chest[1] >= cols[0] and chest[1] <= cols[1]]
        if not rows is None:
            chests = [chest for chest in chests if chest[0] >= rows[0] and chest[0] <= rows[1]]

        chest = self.get_nearest(chests)  # найти самое близкое сокровище от игрока
        if chest is None: return
        self.move_to(chest)

        objs = self.get_objs()  # осмотреться
        if obj.chest in objs.values():   # проверить, есть ли сокровище по близости. 
            self.pick()                  # если есть, то взять сокровище

    def action_keep_to_location(self):
        """ Отнести ресурсы на склад"""
        pos_loc = self.get_location_pos()
        self.move_to(pos_loc)
        objs = self.get_objs()  # осмотреться
        if obj.building in objs.values():   # проверить, есть ли склад по близости. 
            self.put()                  # если есть, то складировать


def play_server(config, ava=None):
    servername = getpass.getuser() + '_server'
    server = Server.create(servername)
    server.init_map(config)
    server.launch()
    
    player = Player(servername, ava)
    player.client.server_obj = server
    return player