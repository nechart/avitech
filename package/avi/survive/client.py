from ..mine.client import Client as baseClient
from ..mine.client import Drawer as baseDrawer
from ..mine.enums import *
from ..mine.data import user
from ..mine.data import server
from .server import Server

import pathlib
from time import sleep
from datetime import datetime
from ipywidgets import widgets, Label, HTML, HBox, Image, VBox, Box, HBox, Layout, Button, GridBox
from ipycanvas import Canvas, MultiCanvas, hold_canvas

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

    def set_params(self):
        self.serv_params = server.read_params(self.server)
        super().set_params()

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
        team_scores = {}
        user_ava = {}
        for user_rec in self.users:
            user_scores[user_rec['name']] = user_rec['score'] - user_rec['kills']*3
            user_ava[user_rec['name']] = user_rec['avatar']
            team_scores[user_rec['team']] = team_scores.get(user_rec['team'], 0) + user_scores[user_rec['name']]
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
        #foods = sum(user_scores.values()) - secs * self.client.server['food_per_sec'] * len(user_scores.keys())

        if self.client.server['state'] == server_state.active:
            state_caption = '  |  '.join(['К{0}:{1}'.format(k, team_scores[k]) for k in range(len(team_scores.keys()))])
        else:
             state_caption = 'Остановлен'

        if self.label_game_status.value != state_caption:
            self.label_game_status.value = state_caption

        params = user.read_params(self.client.user['params'])
        feature_str = 'Патроны:{0} | Места:{1}'.format(params['bullets'], params['spaces'])

        if self.feature_label.value != feature_str:
            self.feature_label.value = feature_str

    def redraw(self):
        if self.update_map():
            with hold_canvas(self.canvas):
                for row in range(len(self.map)):
                    for col in range(len(self.map[row])):
                        cell = self.map[row][col]
                        if cell['obj'] == obj.player:
                            for user_i in self.users:
                                if user_i['id'] == cell['userid']:
                                    if user_i['state'] == player_state.hide:
                                        self.canvas.clear_rect(col * CELL_PIXELS, row * CELL_PIXELS, CELL_PIXELS, CELL_PIXELS)
                                        self.canvas.draw_image(self.images_ava_hide[cell['image']], col * CELL_PIXELS, row * CELL_PIXELS)
                                    elif user_i['state'] == player_state.active:
                                        self.canvas.clear_rect(col * CELL_PIXELS, row * CELL_PIXELS, CELL_PIXELS, CELL_PIXELS)
                                        self.canvas.draw_image(self.images_ava[(cell['obj'], cell['image'])], col * CELL_PIXELS, row * CELL_PIXELS)            
                                    elif user_i['state'] == player_state.killed:
                                        self.canvas.draw_image(self.image_killed, col * CELL_PIXELS, row * CELL_PIXELS)            
                                    elif user_i['state'] == player_state.inactive:
                                        self.canvas.clear_rect(col * CELL_PIXELS, row * CELL_PIXELS, CELL_PIXELS, CELL_PIXELS)
                                    #params = user.read_params(user_i['params'])
                                    self.canvas.fill_style =  self.client.serv_params['teams'][user_i['team']]['color']
                                    self.canvas.fill_rect(col * CELL_PIXELS, row * CELL_PIXELS, 5, 5)

                        elif cell['obj'] in [obj.chest, obj.guard, obj.ball, obj.building]:
                            self.canvas.draw_image(self.images_ava[(cell['obj'], cell['image'])], col * CELL_PIXELS, row * CELL_PIXELS)
                            if cell['obj'] == obj.building:
                                teams = self.client.serv_params['teams']
                                for team in teams:
                                    if team['location'] == [row, col]:
                                        self.canvas.fill_style =  team['color']
                                        self.canvas.fill_rect(col * CELL_PIXELS, row * CELL_PIXELS, 8, 8)
                                        break
                                # todo: add building table and fill building types, team and so on
                        elif cell['obj'] == obj.space:                                                                
                            self.canvas.clear_rect(col * CELL_PIXELS, row * CELL_PIXELS, CELL_PIXELS, CELL_PIXELS)
            self.update_panel()

