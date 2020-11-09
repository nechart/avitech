from time import sleep
import datetime
from threading import Thread
import numpy as np
import random

from . import server
from .enums import *
from . import map
from .data import event
from .data import user

EVENT_TIME_LAG = 1.5
dir2action = {  'up':action.guard_move_up, 
                'down':action.guard_move_down, 
                'left':action.guard_move_left, 
                'right':action.guard_move_right,                                 
            }

class Guard(Thread):
    def __init__(self, server, guardid):
        self.server = server
        self.guardid = guardid
        self.stop = False
        super(Guard, self).__init__()

    def do_action(self):
        self.cell = map.get_guard_cell(self.server.id, self.guardid, self.server.con)

        objs = map.get_objs(self.server.server, self.cell['row'], self.cell['col'], self.server.con)
        
        state = None
        if obj.player in objs.values(): #1 проверить, что игрок рядом. если да - съесть
            for cell in map.find_round(self.server.id, self.cell['row'], self.cell['col'], self.server.con):
                if cell['obj'] == obj.player:
                    user_rec = user.find_user(cell['userid'], self.server.con)
                    if user_rec['state'] == player_state.active: # ловим только видимого
                        state = event.send_event(self.server.id, self.guardid, action.guard_kill, self.server.con)
                        break
        if state is None:  # пойти рандомом в любую возможную сторону
            dirs = [k for k,v in objs.items() if v == obj.space]
            if len(dirs) > 0: # некуда ходить (из-за других стражей например)
                dir_plan = random.choice(dirs)
                state = event.send_event(self.server.id, self.guardid, dir2action[dir_plan], self.server.con)

        return state
    def run(self):
        while(True):
            if not self.server.check_state() or self.stop: 
                return
            self.do_action()

            sleep(EVENT_TIME_LAG)