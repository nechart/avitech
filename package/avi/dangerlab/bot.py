from time import sleep
import datetime
from threading import Thread
import numpy as np

from .enums import *
from . import game


class Bot(Thread):

    def __init__(self, game):
        self.game = game
        self.bot_time_lag = 0.5
        super(Bot, self).__init__()

    def _run_bot_function(self, obj_up, obj_down, obj_left, obj_right):
        return self.game.bot(obj_up, obj_down, obj_left, obj_right, self.game.state == player_state.hide)
    
    def bot_move(self):
        x_player = self.game.get_x_player()
        dirs = {}
        
        x_player_dir = x_player.copy()
        x_player_dir[0] -= 1
        obj_up = obj.wall if not self.game.check_x(x_player_dir, True) else self.game.lab_map[x_player_dir[0], x_player_dir[1]]
        dirs['up'] = x_player_dir.copy()
        
        x_player_dir = x_player.copy()
        x_player_dir[0] += 1
        obj_down = obj.wall if not self.game.check_x(x_player_dir, True) else self.game.lab_map[x_player_dir[0], x_player_dir[1]]
        dirs['down'] = x_player_dir.copy()

        x_player_dir = x_player.copy()
        x_player_dir[1] -= 1
        obj_left = obj.wall if not self.game.check_x(x_player_dir, True) else self.game.lab_map[x_player_dir[0], x_player_dir[1]]
        dirs['left'] = x_player_dir.copy()

        x_player_dir = x_player.copy()
        x_player_dir[1] += 1
        obj_right = obj.wall if not self.game.check_x(x_player_dir, True) else self.game.lab_map[x_player_dir[0], x_player_dir[1]]
        dirs['right'] = x_player_dir.copy()
        
        try:
            action = self._run_bot_function(obj_up, obj_down, obj_left, obj_right)
        except Exception as e:
            print(e)
            action = ""
        
        if (action not in ['up', 'down', 'left', 'right', 'hide', 'pick', 'none']):
            print("Команда {} не распознана".format(action))
            return False
        
        if (self.game.debug_bot):
            print(x_player, action)
        
        if action == 'none': return False
        if action == 'hide': self.game.player_hide()
        elif action == 'pick': self.game.player_pick()
        else:
            self.game.player_move(dirs[action])
        
        return True
        
    def run(self):
        while(True):
            if self.game.check_state() is not True: 
                return
            self.bot_move()
            sleep(self.bot_time_lag)

class BotMap(Bot):
    def __init__(self, game):
        self.level_map = [  [0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0],                                                                                    
                         ]
        super(BotMap, self).__init__(game)

    def _run_bot_function(self, obj_up, obj_down, obj_left, obj_right):
        return self.game.bot(obj_up, obj_down, obj_left, obj_right, self.game.state == player_state.hide, self.level_map)
