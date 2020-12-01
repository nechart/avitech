from ..mine.player import Player as minePlayer
from ..mine.enums import *
from .server import Server
#from .client import Client
#from . import map
import getpass


class Player(minePlayer):
    def __init__(self, server_name, ava=None, user_name = None):
        super().__init__(server_name, ava, user_name)

    def shoot(self, dir):
        # выстрелить
        dir_to_action = {'up':action.fire_up, 'left':action.fire_left, 'down':action.fire_down, 'right':action.fire_right}
        return self.client.make_action(dir_to_action[dir])

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

    def find_shoot_pos(self, goals):
        """найти ближайщую позицию для выстрела
        Параметры:
        pos_user - кортеж с координатой игрока
        goals - список кортежей с координатами вероятных целей
        Возвращаемое значение:
        dirs - список кортежей с числом шагов и направлением движения
        """
        pos_user = self.get_pos()
        steps = {}
        for goal in goals:
            if goal == pos_user:
                continue
            min_step = min(abs(goal[0] - pos_user[0]),abs(goal[1] - pos_user[1]))
            steps[min_step] = steps.get(min_step, []) + [goal]
        
        # найдем минимальное число шагов и расчитаем направления и число шагов для каждой из этих позиций
        dirs = []

        if len(steps) > 0:
            min_step = min(steps.keys())

            min_goals = steps[min_step]

            for goal in min_goals:
                if abs(goal[0] - pos_user[0]) <= abs(goal[1] - pos_user[1]):
                    step_num =  abs(goal[0] - pos_user[0])
                    dir = 'down' if goal[0] > pos_user[0] else 'up'
                else:
                    step_num =  abs(goal[1] - pos_user[1])
                    dir = 'right' if goal[1] > pos_user[1] else 'left'
                dirs.append((step_num, dir))
        
        return dirs


def play_server(config, ava=None):
    servername = getpass.getuser() + '_server'
    server = Server.create(servername)
    server.init_map(config)
    server.launch()
    player = Player(servername, ava)
    player.client.server_obj = server
    return player