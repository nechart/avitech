from time import sleep
from time import gmtime, strftime
import datetime
from threading import Thread
import numpy as np
import random

from . import server
from .data import user
from . import map
from .data import event
from .enums import *
EVENT_LAG_TIME = 0.02

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
            #print(datetime.datetime.now())
            self.set_processed(self.process_event(event_rec))

    def process_event(self, event_rec):
        if event_rec['action'] == action.spawn:
            row, col = map.find_empty_place(self.server.server, con=self.server.con)
            if row < 0:
                event_rec['state'] = action_state.rejected
            else:
                user_rec = user.find_user(event_rec['userid'], con=self.server.con)
                if not user_rec['row'] is None: # юзер был в прошлый раз и перезашел
                    cell_last = map.find_cell(self.server.id, user_rec['row'], user_rec['col'], con=self.server.con)
                    if cell_last['userid'] == user_rec['id']:
                        cell_last['obj'] = obj.space
                        cell_last['userid'] = -1
                        cell_last['image'] = ''
                        map.update_cell(cell_last, self.server.con)

                user_rec['row'] = row
                user_rec['col'] = col
                user_rec['state'] = player_state.active
                user.update_user(user_rec, con=self.server.con)
                cell = map.find_cell(self.server.id, row, col, con=self.server.con)
                cell['obj'] = obj.player
                cell['userid'] = user_rec['id']
                cell['image'] = user_rec['avatar']
                map.update_cell(cell, self.server.con)
                #print('Пользователь {} ID {} присоединился'.format(user_rec['name'], user_rec['id']))

        elif event_rec['action'] in [action.spawn_chest, action.spawn_guard]:
            row, col = map.find_empty_place(self.server.server, con=self.server.con)
            if row < 0:
                event_rec['state'] = action_state.rejected
            else:
                if event_rec['action'] == action.spawn_guard:
                    guard = self.server.guards.get(event_rec['userid'], None)
                    if not guard is None and not guard.cell is None:
                        cell_last = map.get_guard_cell(self.server.id, event_rec['userid'], con=self.server.con)
                        cell_last['obj'] = obj.space
                        cell_last['userid'] = -1
                        cell_last['image'] = ''
                        map.update_cell(cell_last, self.server.con)
                #elif event_rec['action'] == action.spawn_chest:

                cell = map.find_cell(self.server.id, row, col, con=self.server.con)
                cell['obj'] = obj.chest if event_rec['action'] == action.spawn_chest else obj.guard
                cell['userid'] = event_rec['userid']
                cell['image'] = random.choice(ava_chest.items()) if event_rec['action'] == action.spawn_chest else random.choice(ava_guard.items())
                map.update_cell(cell, self.server.con)
            

        elif event_rec['action'] in [action.move_down, action.move_right, action.move_left, action.move_up]:
            user_rec = user.find_user(event_rec['userid'], con=self.server.con)
            if user_rec['state'] in [player_state.active, player_state.hide]:
                row = user_rec['row']+1 if event_rec['action'] == action.move_down else user_rec['row']-1 if event_rec['action'] == action.move_up else user_rec['row']
                col = user_rec['col']+1 if event_rec['action'] == action.move_right else user_rec['col']-1 if event_rec['action'] == action.move_left else user_rec['col']
                if not map.check_coords(self.server.server, row, col):
                    event_rec['state'] = action_state.rejected
                elif map.find_cell(self.server.id, row, col, con=self.server.con)['obj'] != obj.space:
                    event_rec['state'] = action_state.rejected
                else:
                    map.change_cells(self.server.id, (user_rec['row'], user_rec['col']), (row, col), self.server.con)
                    user_rec['row'] = row
                    user_rec['col'] = col
                    user_rec['state'] = player_state.active
                    user.update_user(user_rec, con=self.server.con)
            else:
                event_rec['state'] = action_state.rejected
        
        elif event_rec['action'] == action.hide:
            user_rec = user.find_user(event_rec['userid'], con=self.server.con)
            if user_rec['state'] in [player_state.active]:
                user_rec['state'] = player_state.hide
                user.update_user(user_rec, con=self.server.con)
            else:
                event_rec['state'] = action_state.rejected
        
        elif event_rec['action'] == action.pick:
            user_rec = user.find_user(event_rec['userid'], con=self.server.con)
            if user_rec['state'] in [player_state.active, player_state.hide]:
                objs = map.get_objs(self.server.server, user_rec['row'], user_rec['col'], self.server.con)
                if not obj.chest in objs.values():
                    event_rec['state'] = action_state.rejected
                else:
                    for cell in map.find_round(self.server.id, user_rec['row'], user_rec['col']):
                        if cell['obj'] == obj.chest:
                            cell['obj'] = obj.space
                            map.update_cell(cell, self.server.con)
                            map.change_cells(self.server.id, (user_rec['row'], user_rec['col']), (cell['row'], cell['col']), self.server.con)
                            user_rec['row'] = cell['row']
                            user_rec['col'] = cell['col']
                            user_rec['score'] += 1 if cell['image'] == ava_chest.chest1 else 2
                            user_rec['state'] = player_state.active
                            user.update_user(user_rec, con=self.server.con)
                            #self.server.chests.remove((cell['row'], cell['col']))
                            event.insert_event(serverid=self.server.id, userid=-1, action=action.spawn_chest, con=self.server.con)
                            break
            else:
                event_rec['state'] = action_state.rejected
        
        ###### Guards actions:
        elif event_rec['action'] == action.guard_kill:
            guard = self.server.guards.get(event_rec['userid'], None)
            if not guard or guard.killed == True:
                event_rec['state'] = action_state.rejected
            else:
                objs = map.get_objs(self.server.server, guard.cell['row'], guard.cell['col'], self.server.con)
                if obj.player in objs.values(): #1 проверить, что игрок рядом. если да - съесть
                    for cell in map.find_round(self.server.id, guard.cell['row'], guard.cell['col'], self.server.con):
                        if cell['obj'] == obj.player:
                            user_rec = user.find_user(cell['userid'], self.server.con)
                            if user_rec['state'] == player_state.active:
                                user_rec['kills'] += 1
                                user_rec['kill_dt'] = strftime("%Y-%m-%d %H:%M:%S", gmtime()) 
                                user_rec['state'] = player_state.killed
                                user.update_user(user_rec, con=self.server.con)
                                break
                else:
                    event_rec['state'] = action_state.rejected

        elif event_rec['action'] in [action.guard_move_down, action.guard_move_right, action.guard_move_left, action.guard_move_up]:
            guard = self.server.guards.get(event_rec['userid'], None)
            if not guard or guard.killed == True:
                event_rec['state'] = action_state.rejected
            else:
                row = guard.cell['row']+1 if event_rec['action'] == action.guard_move_down else guard.cell['row']-1 if event_rec['action'] == action.guard_move_up else guard.cell['row']
                col = guard.cell['col']+1 if event_rec['action'] == action.guard_move_right else guard.cell['col']-1 if event_rec['action'] == action.guard_move_left else guard.cell['col']
                if not map.check_coords(self.server.server, row, col):
                    event_rec['state'] = action_state.rejected
                elif map.find_cell(self.server.id, row, col, con=self.server.con)['obj'] != obj.space:
                    event_rec['state'] = action_state.rejected
                else:
                    map.change_cells(self.server.id, (guard.cell['row'], guard.cell['col']), (row, col), self.server.con)
        
        return event_rec

    def run(self):
        while(True):
            if not self.server.check_state() or self.stop: 
                return
            #try:
            self.process_events()
            sleep(EVENT_LAG_TIME)
            #except Exception as e: 
                # logger.error('Failed to upload to ftp: '+ str(e))
            #    print(str(e))