import getpass
from time import sleep
from threading import Thread
import pathlib
from datetime import datetime

from ipywidgets import widgets, Label, HTML, HBox, Image, VBox, Box, HBox, Layout, Button, GridBox
from ipycanvas import Canvas, MultiCanvas, hold_canvas
from IPython.display import display, clear_output

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
REDRAW_LAG = 0.2
KILL_LAG = 2
CELL_PIXELS = 40

path_file = str(pathlib.Path(__file__).parent.absolute())

class Client():
    def __init__(self, user_name=None):
        self.user_name = getpass.getuser() if not user_name else user_name
        self.drawer = None
        self.server_obj = None

    def connect(self, server_name, ava=None):
        self.con = base.connect()
        self.server = server.find_server(server_name, self.con)
        if self.server is None:
            raise ValueError('Сервер {} не найден'.format(server_name))

        if ava is None:
            user_setup = find_user_setup(self.user_name, self.con)
            if not user_setup is None:
                ava = user_setup['avatar']
            else:
                raise Exception('Надо выбрать аватар')
        else:
            set_user_setup(self.user_name, ava, self.con)

        self.user = find_or_create_user(self.server['id'], self.user_name, ava, self.con)
        self.userid = self.user['id']

        if self.send_event(action.spawn) == action_state.processed:
            print('Ожидание подключения к серверу {}...'.format(server_name))
            self.user = find_user(self.userid)
            self.user['state'] = ava
            self.user['state'] = player_state.active
            self.user['score'] = 0
            self.user['kills'] = 0
            update_user(self.user, self.con)
            clear_output(wait=True)
            #print('Пользователь {} успешно подключен к серверу {}...'.format(self.user_name, server_name))
        else:
            raise ValueError('Не удалось подключить пользователя {}'.format(self.user_name))

    def refresh_user(self):
        self.user = find_user(self.userid, self.con)

    def refresh_server(self):
        self.server = server.find_server_id(self.server['id'], self.con)

    def check_state(self):
        return self.user['state'] != player_state.inactive and self.server['state'] == server_state.active

    def send_event(self, act=action.spawn):
        self.refresh_user()
        if self.user['state'] in [player_state.inactive, player_state.killed]  and act != action.spawn:
            return action_state.rejected

        return event.send_event(self.server['id'], self.userid, act, self.con)

    def make_action(self, act = action.spawn):
        state = self.send_event(act)
        #self.redraw()
        return state == action_state.processed

    def start(self, autostop = False):
        self.autostop = autostop
        if self.drawer != None:
            self.stop()    
        self.drawer = Drawer(self)
        self.drawer.display()
        self.drawer.draw_base()
        self.drawer.start()
        return True

    def stop(self, b = None):
        self.drawer.stop = True
        if not self.server_obj is None:
            self.server_obj.stop()
        if self.autostop:
            raise Exception('Game over')

########################################################################################################################
class Drawer(Thread):
    def __init__(self, client):
        self.client = client
        self.stop = False
        self.map = None
        self.users = None
        self.user_scores = None
        self.init_images()
        super(Drawer, self).__init__()

    def init_images(self, path=path_file):

        self.images_ava = {}
        self.images_ava_hide = {}        
        avatars = [avatar.cowboy, avatar.stan, avatar.rock, avatar.pig, avatar.glass, avatar.dipper, avatar.zoose, \
                    avatar.super, avatar.garry, avatar.chui, avatar.lord, avatar.bill,]

        for ava in avatars:
            self.images_ava[(obj.player, ava)] = Image.from_file(path + '/images/avatar/{}.png'.format(ava))
            self.images_ava_hide[ava] = Image.from_file(path + '/images/avatar/{}_h.png'.format(ava))            

        for ava in ava_guard.items():
            self.images_ava[(obj.guard, ava)] = Image.from_file(path + '/images/{}.png'.format(ava))
        self.images_ava[(obj.guard, ava_guard.killed)] = Image.from_file(path + '/images/{}.png'.format(ava_guard.killed))

        for ava in ava_chest.items():
            self.images_ava[(obj.chest, ava)] = Image.from_file(path + '/images/{}.png'.format(ava))
        self.images_ava[(obj.wall, '')] = Image.from_file(path + '/images/wall.png')
        self.images_ava[(obj.ball, ava_ball.ball)] = Image.from_file(path + '/images/ball.png')
        self.image_killed = Image.from_file(path + '/images/player_loss.png')
        self.image_space = Image.from_file(path + '/images/space.jpg')

    def create_panel(self):
        # images button https://fontawesome.com/v4.7.0/icons/
        items_layout = Layout( width='80px')     # override the default width of the button to 'auto' to let the button grow

        box_layout = Layout(display='flex',
                            flex_flow='column',
                            align_items='stretch',
                            border='solid')
                            #,width='30%')

        self.label_game_status = Label('Подключение к серверу...')
        
        self.panel_users = GridBox(children=[], layout=Layout(grid_template_columns="80px 80px 30px"))

        # панель запуска-остановки-паузы
        #b_play = Button(description='ИГРА',icon = 'fa-play', layout = items_layout)
        b_stop = Button(description='СТОП',icon = 'fa-stop', layout = items_layout)
        
        #b_play.on_click(self.client.start) # client.start) 
        b_stop.on_click(self.client.stop) 

        panel = VBox([HBox([Label('Сервер:'), Label(self.client.server['name'])]),
                          self.label_game_status,
                          HBox([Label('Игрок:'),Label(self.client.user_name), b_stop]),
                          self.panel_users],
                      layout=box_layout)    
        return panel          
        
    def update_panel(self, b=None):
        state_caption = 'Активен' if self.client.server['state'] == server_state.active else 'Остановлен'
        if self.label_game_status.value != state_caption:
            self.label_game_status.value = state_caption
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
                
    def display(self):
        multi = MultiCanvas(2, width=self.client.server['mapsize_x'] * CELL_PIXELS, height=self.client.server['mapsize_y'] * CELL_PIXELS)
        #multi[0].fill_style = 'black'
        #multi[0].fill_rect(0, 0, multi.size[0], multi.size[1])
        self.canvas_base = multi[0]
        self.canvas = multi[1]
        
        panel = self.create_panel()
        
        self.output = widgets.Output()
        self.output.clear_output()
        #display(VBox([Image.from_file(path + '/images/header.jpg', width=200,height=40), HBox([multi])]), self.output)        
        display(HBox([multi, panel]), self.output)        

    def draw_base(self, color='black'):
        self.update_map()
        with hold_canvas(self.canvas_base):
            self.canvas_base.clear()
            self.canvas_base.fill_style = color
            self.canvas_base.fill_rect(0, 0, self.canvas_base.size[0], self.canvas_base.size[1])
            for row in range(len(self.map)):
                for col in range(len(self.map[row])):
                    cell = self.map[row][col]
                    if cell['obj'] == obj.wall:
                        self.canvas_base.draw_image(self.images_ava[(obj.wall, '')], col * CELL_PIXELS, row * CELL_PIXELS)
        
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
                        elif cell['obj'] in [obj.chest, obj.guard, obj.ball]:
                            self.canvas.draw_image(self.images_ava[(cell['obj'], cell['image'])], col * CELL_PIXELS, row * CELL_PIXELS)
                        elif cell['obj'] == obj.space:                                                                
                            self.canvas.clear_rect(col * CELL_PIXELS, row * CELL_PIXELS, CELL_PIXELS, CELL_PIXELS)
            self.update_panel()
                                       
    def update_map(self):
        changed = False
        new_map = map.get_all(self.client.server, self.client.con)
        if self.map is None or self.map != new_map:
            self.map = new_map
            changed = True

        new_users = find_all_users(self.client.server['id'], self.client.con)
        if self.users is None or self.users != new_users:
            self.users = new_users
            changed = True
        self.client.refresh_user()
        self.client.refresh_server()
        return changed
    
    def run(self):
        while(True):
            try:
                if not self.client.check_state() or self.stop: 
                    self.label_game_status.value = 'Остановлен'
                    self.output.clear_output()
                    return
                self.redraw()

                if self.client.user['state'] == player_state.killed:
                    if (datetime.utcnow() - self.client.user['kill_dt']).total_seconds() >= KILL_LAG:
                        event.send_event(self.client.server['id'], self.client.userid, action.spawn, self.client.con)

                sleep(REDRAW_LAG)
            except Exception as e: 
                pass
