from time import sleep
import datetime
from threading import Thread
import numpy as np
import random

from . import game
from .enums import *


class Guard(Thread):
    def __init__(self, game, x_guard):
        self.game = game
        self.x_guard = x_guard
        self.guard_time_lag = 1.5
        super(Guard, self).__init__()

    def guard_move(self):
        #1 проверить, что игрок рядом. если да - съесть
        x_player = self.game.get_x_player()
        if np.sum(np.abs(x_player - self.x_guard)) == 1 and self.game.state == player_state.show:
            # съесть можно только после 1 секунды от хода игрока
            if (datetime.datetime.now() - self.game.last_click).total_seconds() < self.guard_time_lag: return False
            # если спрятался, выграл или уже проиграл, то ничего не делать
            self.game.lab_map[self.x_guard[0], self.x_guard[1]] = obj.space
            self.game.state = player_state.loss
            self.game.update_game_status()
            return True
        # пойти рандомом в любую возможную сторону
        else:
            plans = []
            x_guard_plan = self.x_guard.copy()
            x_guard_plan[0] += 1
            if self.game.check_x(x_guard_plan):
                plans.append(x_guard_plan)
            x_guard_plan = self.x_guard.copy()
            x_guard_plan[0] -= 1
            if self.game.check_x(x_guard_plan):
                plans.append(x_guard_plan)
            x_guard_plan = self.x_guard.copy()
            x_guard_plan[1] += 1
            if self.game.check_x(x_guard_plan):
                plans.append(x_guard_plan)
            x_guard_plan = self.x_guard.copy()
            x_guard_plan[1] -= 1
            if self.game.check_x(x_guard_plan):
                plans.append(x_guard_plan)
            if len(plans) == 0: return False # некуда ходить (из-за других стражей например)
            
            plan_choiced = random.randint(0, len(plans) - 1)
            x_guard_plan = plans[plan_choiced]
            self.game.lab_map[self.x_guard[0], self.x_guard[1]] = obj.space
            self.game.lab_map[x_guard_plan[0], x_guard_plan[1]] = obj.guard
            self.x_guard = x_guard_plan.copy()
            #print(self.x_guard)
            return True
        
    def run(self):
        while(True):
            if self.game.check_state() is not True: 
                return
            #print('guard_move', self.game.state)
            if self.guard_move():
                self.game.draw_map_fog()
            sleep(self.guard_time_lag)