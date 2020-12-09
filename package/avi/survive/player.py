from ..strikeball.player import Player as basePlayer
from ..mine.enums import *
from .server import Server
from .client import Client
import getpass

# Создадим словарь направлений для обхода по часовой стрелке:
next_dir = {'up':'right', 'right':'down', 'down':'left', 'left':'up'}
prev_dir = {'up':'left', 'right':'up', 'down':'right', 'left':'down'}

class Player(basePlayer):
    def __init__(self, server_name, ava=None, user_name=None, team=0):
        self.client = Client(user_name)
        self.client.connect(server_name, ava=ava, team=team)

    def get_goals(self, goals):
        """ Функция определения координат подходящих целей
        Параметры:
        pos_user - кортеж с координатой игрока
        goals - список кортежей с координатами вероятных целей
        Возвращаемое значение:
        list - список кортежей, по которым можно стрелять. 
        """
        pos_user = self.get_pos()
        dict_goals = {goal:abs(goal[0] - pos_user[0]) + abs(goal[1] - pos_user[1]) for goal in goals if goal[0] == pos_user[0] or goal[1] == pos_user[1]}

        ret_goals = list(dict(sorted(dict_goals.items(), key=lambda item: item[1])).keys())
        
        if pos_user in ret_goals:
            ret_goals.remove(pos_user)
        
        return ret_goals

    def distance(self, pos1, pos2):
        """ Расчитать расстояние между позициями """
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def move_to(self, pos_to):
        """ Дойти до позиции"""
        pos_history = []
        pos = self.get_pos()
        while self.distance(pos_to, pos) > 1:
            goal_dir = self.get_dir(pos_to)  # получить направление
            if goal_dir:                     # проверить, что направление выбрано
                objs = self.get_objs()  # осмотреться
                if objs[goal_dir] == obj.guard:   # проверить, есть ли страж на пути - спрятаться
                    self.hide()                  # если есть, то взять сокровище                
                    continue # не учитываем эту позицию в прошлую
                else:
                    if objs[goal_dir] in [obj.wall, obj.player, obj.chest, obj.building]:  # если в выбранном направлении стоит враг / игрок
                        if not self.move(next_dir[goal_dir]):   # выбрать следующее направление по часовой стрелке
                            self.move(prev_dir[goal_dir]) # выбрать следующее направление против часовой стрелке
                    self.move(goal_dir)          # выполнить движение
            if pos in pos_history:
                return False
            pos_history.append(pos)
            pos = self.get_pos() # обновить свою позицию
        return True

    ####################################
    def bot_collector(self, chests, rows=None, cols=None):
        """ Бот собирателя"""
        if not cols is None:
            chests = [chest for chest in chests if chest[1] >= cols[0] and chest[1] <= cols[1]]
        if not rows is None:
            chests = [chest for chest in chests if chest[0] >= rows[0] and chest[0] <= rows[1]]

        chest = self.get_nearest(chests)  # найти самое близкое сокровище от игрока
        if chest is None: return

        goal_dir = self.get_dir(chest)  # получить направление
        if goal_dir:                     # проверить, что направление выбрано
            objs = self.get_objs()  # осмотреться
            if objs[goal_dir] == obj.chest:   # проверить, есть ли сокровище по близости. 
                self.pick()                  # если есть, то взять сокровище
            elif objs[goal_dir] == obj.guard:   # проверить, есть ли сокровище по близости. 
                self.hide()                  # если есть, то взять сокровище                
            else:
                if objs[goal_dir] in [obj.player]:  # если в выбранном направлении стоит враг / игрок
                    goal_dir = next_dir[goal_dir]   # выбрать следующее направление по часовой стрелке
                self.move(goal_dir)          # выполнить движение

        objs = self.get_objs()  # осмотреться

        if obj.chest in objs:   # проверить, есть ли сокровище по близости. 
            self.pick()                  # если есть, то взять сокровище
        if obj.guard in objs:   # проверить, есть ли сокровище по близости. 
            self.hide()                  # если есть, то взять сокровище  


    def bot_hunter(self, guards, rows=None, cols=None):
        """ Бот охотника"""
        objs = self.get_objs()  # осмотреться

        if obj.guard in objs.values():   # проверить, есть ли страж по близости. 
            self.hide()  # если да, спрятаться
            return
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
                self.move(step_dir)    # движение в нужном направлении
        goals = self.get_goals(guards) # здесь игрок должен быть уже на позиции, проверим, есть ли цели для стрельбы
        if goals:  # если цели есть (список не пустой)
            dir = self.get_dir(goals[0])  # получить направление выстрела для первой по близости цели
            if dir:                     # проверить, что направление выбрано
                self.shoot(dir)          # выполнить выстрел        


    def bot_bodyguard(self, player, guards):
        """ Бот телохранителя.
            Телохранитель должен следить за координатами своего друга, следовать за ним и убивать всех стражников"""
        next_dir = {'up':'right', 'right':'down', 'down':'left', 'left':'up'}

        pos = self.get_pos()     # получить свои координаты
        player_pos = self.get_player(player)     # получить координаты игрока
                
        # проверим, что телохранитель находится не дальше 2 клеток от друга:
        if (abs(pos[0] - player_pos[0]) > 2 or  abs(pos[0] - player_pos[0]) > 2):
            goal_dir = self.get_dir(player_pos)  # получить направление
            if goal_dir:                     # проверить, что направление выбрано
                objs = self.get_objs()  # осмотреться
                if objs[goal_dir] == obj.guard:   # проверить, есть ли враг по близости. 
                    self.hide()                  # если есть, то спрятаться
                else:
                    if objs[goal_dir] in [obj.player]:  # если в выбранном направлении стоит враг / игрок
                        goal_dir = next_dir[goal_dir]   # выбрать следующее направление по часовой стрелке
                    self.move(goal_dir)          # выполнить движение
        else:  # после того, как мы подошли, проверим и зачистим стражей вокруг
            self.bot_hunter(guards)


def play_server(config, ava=None):
    servername = getpass.getuser() + '_server'
    server = Server.create(servername)
    server.init_map(config)
    server.launch()
    
    player = Player(servername, ava)
    player.client.server_obj = server
    return player