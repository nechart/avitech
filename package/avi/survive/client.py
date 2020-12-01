from ..mine.client import Client as baseClient
from ..mine.client import Drawer as baseDrawer
from ..mine.enums import *
from .server import Server

import pathlib
from time import sleep
from datetime import datetime
from ipywidgets import widgets, Label, HTML, HBox, Image, VBox, Box, HBox, Layout, Button, GridBox

REDRAW_LAG = 0.2
KILL_LAG = 2
CELL_PIXELS = 40

path_file = str(pathlib.Path(__file__).parent.absolute())

class Client(baseClient):
    def __init__(self, user_name = None):
        super().__init__(user_name)

    def start(self, autostop = False):
        self.autostop = autostop
        if self.drawer != None:
            self.stop()    
        self.drawer = Drawer(self)
        self.drawer.display()
        self.drawer.draw_base()
        self.drawer.start()
        return True

########################################################################################################################
class Drawer(baseDrawer):
    def __init__(self, client):
        super().__init__( client)

    def draw_base(self, color='orange'):
        super().draw_base(color)

    def init_images(self, path=path_file):
        super().init_images(path=path_file)

    def create_panel(self):
        return super().create_panel()

    def update_panel(self, b=None):
        user_scores = {}
        user_ava = {}
        for user_rec in self.users:
            user_scores[user_rec['name']] = user_rec['score'] - user_rec['kills']*3
            user_ava[user_rec['name']] = user_rec['avatar']
        changed = user_scores.values() != self.user_scores.values() if not self.user_scores is None else True

        if changed:
            items = []
            for user_name, score in sorted(user_scores.items(), key=lambda x: x[1], reverse = True) :
                items.append(Label(user_name))
                items.append(Label(user_ava[user_name]))
                items.append(Label(str(score)))
            self.panel_users.children = items
            self.user_scores = user_scores

        secs = (datetime.utcnow() -  self.client.server['start_dt']).total_seconds()
        #print(sum(user_scores), secs, self.client.server['food_per_sec'])
        foods = sum(user_scores.values()) - secs * self.client.server['food_per_sec'] * len(user_scores.keys())

        state_caption = 'Ресурсов: ' + str(round(foods)) if self.client.server['state'] == server_state.active else 'Остановлен'
        if self.label_game_status.value != state_caption:
            self.label_game_status.value = state_caption
