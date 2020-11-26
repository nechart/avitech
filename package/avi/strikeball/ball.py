from time import sleep
import datetime
from threading import Thread
import numpy as np
import random

from . import server
from ..mine.enums import *
from ..mine import map
from ..mine.data import event

EVENT_TIME_LAG = 0.1

action2dir = {  action.fire_up:"up", 
                action.fire_down:"down", 
                action.fire_left:"left", 
                action.fire_right:"right",                                 
            }

dir2action = {  "up":action.ball_move_up, 
                "down":action.ball_move_down, 
                "left":action.ball_move_left, 
                "right":action.ball_move_right,                                 
            }

class Ball(Thread):
    def __init__(self, server, ballid, userid, fire_action):
        self.server = server
        self.ballid = ballid
        self.userid = userid
        self.dir = action2dir[fire_action]
        self.stop = False
        super(Ball, self).__init__()

    def do_action(self):
        self.cell = map.get_ball_cell(self.server.id, self.ballid, self.server.con)
        if self.cell: # and map.check_coords(self.server.server, self.cell['row'], self.cell['col']):
            state = event.send_event(self.server.id, self.ballid, dir2action[self.dir], self.server.con, wait_lag = 0.05) #EVENT_TIME_LAG//2) 
        else:
            state = None
            #raise ValueError('cell is none')

        return state
    def run(self):
        while(True):
            if not self.server.check_state() or self.stop: 
                return
            self.do_action()
            #print(datetime.datetime.now())

            sleep(EVENT_TIME_LAG)