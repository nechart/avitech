"""
Цель класса:
- обработка очереди событий от агентов (пользователей и ботов)
- обновление карты уровня
- вывод панели - список пользователей.  инфа по пользователям. бан.
  - перезапуск сервера. сброс результатов у всех пользователей (или удаление)

использование
server = Server()
server.init(levelmap) # from level
server.launch()

# spawn user
    # random + add in map
    # Level table
    #   servername-levelid-?
    #   col
    #   row
    #   value 0, 1, 3, 4, (10...+)
# generate action
    # Action queue table
    #   servername
    #   username (guard 100+)
    #   datetime
    #   action

"""
import datetime
from time import gmtime, strftime
import random
from time import sleep
from threading import Thread
import numpy as np
import pathlib

from .enums import *
from .data.server import *
from .data import base
from .data import map
from .data import user
from .data import event
from .guard import Guard as Guard
from .event_queue import EventQueue as EventQueue

EVENT_WAIT_LAG = 0.2

class Server():
    def __init__(self, server_name):
        self.con = base.connect()
        self.server_name = server_name
        self.server = find_or_create_server(self.server_name, con=self.con)
        self.id = self.server['id']

    def init_map(self, config={}, mapname=''):
        self.server['mapname'] = mapname if mapname else self.server_name
        self.config = config
        self.server['mapsize_y'] = len(config['map'])
        self.server['mapsize_x'] = len(config['map'][0])
        self.server['state'] = server_state.inactive
        update_server(self.server, con=self.con)

        user.delete_users(self.id, con=self.con)

        event.delete_events(self.id)

        map.recreate_map(serverid=self.id, levelmap=self.config['map'], con=self.con)
        #self.map = self.get_map()
        self.chests = []
        self.guards = []

    def launch(self):
        self.server['state'] = server_state.active
        logintime = strftime("%Y-%m-%d %H:%M:%S", gmtime())    
        self.server['start_dt'] = logintime
        update_server(self.server, con=self.con)

        for _ in range(self.config['chests']):
            event.insert_event(serverid=self.id, userid=-1, action=action.spawn_chest, con=self.con)

        self.queue = EventQueue(self)

        self.queue.start()

        print('Сервер {} запущен c ID {}'.format(self.server_name, self.id))

        self.start_guards()

        return True

    def check_state(self):
        return self.server['state'] == server_state.active

    def pause(self):
        self.server['state'] = server_state.pause
        update_server(self.server, con=self.con)
        return True

    def stop(self):
        self.server['state'] = server_state.inactive
        logintime = strftime("%Y-%m-%d %H:%M:%S", gmtime())    
        self.server['stop_dt'] = logintime
        update_server(self.server, con=self.con)
        self.stop_guards()        
        self.queue.stop = True
        return True

    def start_guards(self):
        self.guards = []
        for guardid in range(self.config['guards']):
            state = event.send_event(serverid=self.id, userid=guardid, action=action.spawn_guard, con=self.con)
            if state == action_state.processed:
                guard = Guard(self, guardid)
                self.guards.append(guard)
                guard.start()

    def stop_guards(self):
        for guard in self.guards:
            guard.stop = True


    @staticmethod
    def create(server_name):
        return Server(server_name)