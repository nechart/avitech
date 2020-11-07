import getpass
from time import sleep
from threading import Thread
import pathlib

from ipywidgets import widgets, Label, HTML, HBox, Image, VBox, Box, HBox, Layout, Button
from ipycanvas import Canvas, MultiCanvas, hold_canvas
from IPython.display import display

from .enums import *
from .server import Server
from .data import server
from .data.user import *
from .data import event
from . import map
from .data import base

"""
Класс client как перегрузка DLGameTask в котором перегружаем работу с картой.
Вместо списка levelmap обращаемся к базе
Вместо выполнения действия пишем в очередь и ждем
Остальное все сохраняется
+ добавляем координаты сокровищ (зажигать на карте?)
+ добавляем справа список пользователей со счетом
+ статус подключения. кнопка стоп. кнопка реконнект
+ если умер, то киллс + 1 и на воскрешение
"""
EVENT_WAIT_LAG = 0.2
REDRAW_LAG = 0.2
CELL_PIXELS = 40

path = str(pathlib.Path(__file__).parent.absolute())

class Client():
    def __init__(self):
        self.user_name = getpass.getuser()

    def connect(self, server_name, ava = avatar.cowboy):
        self.con = base.connect()
        self.server = server.find_server(server_name, self.con)
        if self.server is None:
            raise ValueError('Сервер {} не найден'.format(server_name))
        self.user = find_or_create_user(self.server['id'], self.user_name, ava, self.con)
        self.userid = self.user['id']

        if self.send_event(action.spawn) == action_state.processed:
            self.user = find_user(self.userid)
            self.user['avatar'] = ava
            self.user['state'] = player_state.active
            self.user['score'] = 0
            self.user['kills'] = 0
            update_user(self.user, self.con)
        else:
            raise ValueError('Не удалось подключить пользователя {}'.format(self.user_name))

    def refresh_user(self):
        self.user = find_user(self.userid, self.con)

    def refresh_server(self):
        self.server = server.find_server_id(self.server['id'], self.con)

    def check_state(self):
        return self.user['state'] == player_state.active and self.server['state'] == server_state.active

    def send_event(self, act=action.spawn):
        self.refresh_user()
        if self.user['state'] != player_state.active and act != action.spawn:
            return action_state.rejected
        eventid = event.insert_event(self.server['id'], self.userid, act, self.con)
        # wait response: ping when event status
        while True:
            sleep(EVENT_WAIT_LAG)
            event_rec = event.find_event(eventid, self.con)
            if event_rec['state'] >= action_state.processed:
                break
        return event_rec['state']

    def make_action(self, act = action.spawn):
        state = self.send_event(act)
        #self.redraw()
        return state == action_state.processed

    def start(self):
        self.drawer = Drawer(self)
        self.drawer.display()
        self.drawer.draw_base()
        self.drawer.start()
        return True

    def stop(self):
        self.drawer.stop = True


class Drawer(Thread):
    def __init__(self, client):
        self.client = client
        self.stop = False
        self.map = None
        super(Drawer, self).__init__()

    def init_images(self):
        self.images_base = {obj.wall: Image.from_file(path + '/images/wall.jpg'), 
                            obj.space: Image.from_file(path + '/images/space.jpg'), 
                            obj.chest: Image.from_file(path + '/images/chest1.jpg')}

        self.images_ava = {}
        self.images_ava_hide = {}        
        avatars = [avatar.cowboy, avatar.stan, avatar.rock, avatar.pig, avatar.glass, avatar.dipper, avatar.zoose, \
                    avatar.super, avatar.garry, avatar.chui, avatar.lord, avatar.bill,]
        for ava in avatars:
            self.images_ava[ava] = Image.from_file(path + '/images/{}.png'.format(ava))
            self.images_ava_hide[ava] = Image.from_file(path + '/images/{}_h.png'.format(ava))

    def display(self):
        multi = MultiCanvas(2, width=self.client.server['mapsize_x'] * CELL_PIXELS, height=self.client.server['mapsize_y'] * CELL_PIXELS)
        multi[0].fill_style = 'black'
        multi[0].fill_rect(0, 0, multi.size[0], multi.size[1])
        self.canvas_base = multi[0]
        self.canvas = multi[1]
        self.output = widgets.Output()
        #display(VBox([Image.from_file(path + '/images/header.jpg', width=200,height=40), HBox([multi])]), self.output)        
        display(multi, self.output)        

    def draw_base(self):
        with hold_canvas(self.canvas_base):
            self.canvas_base.clear()
            for row in range(len(self.map)):
                for col in range(len(self.map[row])):
                    cell = self.map[row][col]
                    if cell['obj'] == obj.wall:
                        self.canvas.draw_image(self.images_base[obj.wall], col * CELL_PIXELS, row * CELL_PIXELS)
    
    def redraw(self):
        new_map = map.get_all(self.client.server)
        if self.map is None or self.map != new_map:
            self.map = new_map
            with hold_canvas(self.canvas):
                self.canvas.clear()
                for row in range(len(self.map)):
                    for col in range(len(self.map[row])):
                        cell = self.map[row][col]
                        if cell['obj'] == obj.player:
                            self.canvas.draw_image(self.images_ava[cell['image']], col * CELL_PIXELS, row * CELL_PIXELS)
                        elif cell['obj'] == obj.chest:
                            self.canvas.draw_image(self.images_base[obj.chest], col * CELL_PIXELS, row * CELL_PIXELS)

    def run(self):
        while(True):
            if not self.client.check_state() or self.stop: 
                return
            self.redraw()
            sleep(REDRAW_LAG)