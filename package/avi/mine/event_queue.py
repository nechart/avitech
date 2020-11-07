from time import sleep
import datetime
from threading import Thread
import numpy as np
import random

from . import server
from .data import user
from . import map
from .data import event
from .enums import *
EVENT_LAG_TIME = 0.1

class EventQueue(Thread):
    def __init__(self, server):
        self.server = server
        self.stop = False
        super(EventQueue, self).__init__()
    
    def set_processed(self, event_rec):
        if event_rec['state'] != action_state.rejected:
            event_rec['state'] = action_state.processed
        event.update_event(event_rec)
    
    def process_events(self):
        events = event.find_events(serverid=self.server.id, con=self.server.con)
        for event_rec in events:
            if event_rec['action'] == action.spawn:
                row, col = map.find_empty_place(self.server.server, con=self.server.con)
                if row < 0:
                    event_rec['state'] = action_state.rejected
                else:
                    user_rec = user.find_user(event_rec['userid'], con=self.server.con)
                    if not user_rec['row'] is None: # юзер был в прошлый раз и перезашел
                        cell_last = map.find_cell(self.server.id, user_rec['row'], user_rec['col'], con=self.server.con)
                        if cell_last['userid'] == user_rec['id']:
                            cell['obj'] = obj.space
                            cell['userid'] = -1
                            cell['image'] = ''
                            map.update_cell(cell)
                    else:
                        user_rec['row'] = row
                        user_rec['col'] = col
                        user.update_user(user_rec, con=self.server.con)
                        cell = map.find_cell(self.server.id, row, col, con=self.server.con)
                        cell['obj'] = obj.player
                        cell['userid'] = user_rec['id']
                        cell['image'] = user_rec['avatar']
                        map.update_cell(cell)
                        print('Пользователь {} ID {} присоединился'.format(user_rec['name'], user_rec['id']))

            elif event_rec['action'] == action.spawn_guard:
                #row, col = map.find_empty_place()
                pass

            elif event_rec['action'] == action.spawn_chest:
                row, col = map.find_empty_place(self.server.server, con=self.server.con)
                if row < 0:
                    event_rec['state'] = action_state.rejected
                else:
                    self.server.chests.append((row, col))
                    cell = map.find_cell(self.server.id, row, col, con=self.server.con)
                    cell['obj'] = obj.chest
                    map.update_cell(cell)

            elif event_rec['action'] in [action.move_down, action.move_right, action.move_left, action.move_up]:
                user_rec = user.find_user(event_rec['userid'], con=self.server.con)
                row = user_rec['row']+1 if event_rec['action'] == action.move_down else user_rec['row']-1 if event_rec['action'] == action.move_up else user_rec['row']
                col = user_rec['col']+1 if event_rec['action'] == action.move_right else user_rec['col']-1 if event_rec['action'] == action.move_left else user_rec['col']
                if not map.check_coords(self.server.server, row, col) or \
                        map.find_cell(self.server.id, row, col, con=self.server.con)['obj'] != obj.space:
                    test_obj = map.find_cell(self.server.id, row, col, con=self.server.con)
                    event_rec['state'] = action_state.rejected
                else:
                    map.change_cells(self.server.id, (user_rec['row'], user_rec['col']), (row, col))
                    user_rec['row'] = row
                    user_rec['col'] = col
                    user.update_user(user_rec, con=self.server.con)
            
            elif event_rec['action'] == action.pick:
                user_rec = user.find_user(event_rec['userid'], con=self.server.con)
                objs = map.get_objs(self.server.server, user_rec['row'], user_rec['col'])
                if not obj.chest in objs.values():
                    event_rec['state'] = action_state.rejected
                else:
                    for cell in map.find_round(self.server.id, user_rec['row'], user_rec['col']):
                        if cell['obj'] == obj.chest:
                            map.change_cells(self.server.id, (user_rec['row'], user_rec['col']), (cell['row'], cell['col']))
                            user_rec['row'] = cell['row']
                            user_rec['col'] = cell['col']
                            user_rec['score'] += 1
                            user.update_user(user_rec, con=self.server.con)
                            self.server.chests.remove((cell['row'], cell['col']))
                            event.insert_event(serverid=self.server.id, userid=-1, action=action.spawn_chest, con=self.server.con)
                            break

            self.set_processed(event_rec)

    def run(self):
        while(True):
            if not self.server.check_state() or self.stop: 
                return
            self.process_events()
            sleep(EVENT_LAG_TIME)