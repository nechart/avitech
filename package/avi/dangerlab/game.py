import datetime
import random
from time import sleep
from threading import Thread
import numpy as np
import pathlib

from ipywidgets import widgets, Label, HTML, HBox, Image, VBox, Box, HBox, Layout, Button
from ipycanvas import Canvas, MultiCanvas, hold_canvas
from IPython.display import display

from .enums import * #obj as obj
#from .enums import player_state as player_state
from .guard import Guard as Guard
from .bot import Bot as Bot
from .bot import BotMap as BotMap
from .levels import levels as levels
from .levels import levels_task as levels_task

path = str(pathlib.Path(__file__).parent.absolute())
class DangerLabirintGame:
    def __init__(self):
        self.best_steps  = 100 # лучший результат!
        self.bot = None
        self.player_steps = 0
        self.bot_mode = False
        self.bot_object = None
            
    def init_images(self):   
        self.im_player = Image.from_file(path + '/images/player.jpg')
        self.im_player_hide = Image.from_file(path + '/images/player_hide.jpg') 
        self.im_player_win = Image.from_file(path + '/images/player_win.jpg')
        self.im_player_loss = Image.from_file(path + '/images/player_loss.png')
        self.im_space = Image.from_file(path + '/images/space.jpg')
        self.im_chest = Image.from_file(path + '/images/chest_m.jpg')
        self.im_guards = [Image.from_file(path + '/images/guard1.jpg'),Image.from_file(path + '/images/guard2.jpg'), Image.from_file(path + '/images/guard3.jpg')]
        self.im_wall = Image.from_file(path + '/images/wall.jpg')
        
        self.imagedict = {obj.wall: self.im_wall, #0
                          obj.space: self.im_space, #1 
                          (obj.player, player_state.show) : self.im_player, #2
                          (obj.player, player_state.hide) : self.im_player_hide, #2
                          (obj.player, player_state.win) : self.im_player_win, #2
                          (obj.player, player_state.loss) : self.im_player_loss, #2
                          obj.guard: self.im_guards, #3 
                          obj.chest: self.im_chest}  #4      
        
    
    def set_levels(self, levels):
        self.levels = levels
    
    def init_map(self):
        self.level_map, self.guard_count = self.levels[self.cur_level]
        self.map_size = len(self.level_map)
        self.time_lag = 0.5 # sec
        self.guard_time_lag = 1 # sec
        self.n_pixels = 40
        """
        self.colordict = {obj.wall: 'brown', #0
                          obj.space: '#333333', #1 
                          (obj.player, player_state.show) : 'green', #2
                          (obj.player, player_state.hide) : 'darkgreen', #2
                          (obj.player, player_state.win) : 'white', #2
                          (obj.player, player_state.loss) : 'darkred', #2
                          obj.guard: 'red', #3 
                          obj.chest: 'blue'}  #4      
        """
         # 0 - стены 1 - коридор, 2 - игрок, 3 - спаун/страж 4 - сокровища (будут появляться рандомно) 
        x = np.zeros((self.map_size, self.map_size), dtype=int)
        x[0 : self.map_size, 0 : self.map_size] = self.level_map
        self.lab_map = x        
       
    def spawn(self):
        # найти места спаунсов и рендом расставить сокровища и стражей
        x_spawns = np.where(self.lab_map == obj.guard)
        len_spawns = len(x_spawns[0])
        list_spawns = [i for i in range(0, len_spawns)]
        chest_spawn = random.choice(list_spawns)
        list_spawns = list(set(list_spawns) - set([chest_spawn]))
        guard_spawns = []
        if (self.guard_count > len(list_spawns)): 
            raise ValueError("Ошибка в настройках уровня {}. Слишком много стражей".format(self.cur_level))
        for _ in range(0, self.guard_count):
            guard_spawn = random.choice(list_spawns)
            list_spawns = list(set(list_spawns) - set([guard_spawn]))
            guard_spawns.append(guard_spawn)

        self.guards = []            
        for i_spawn in range(0, len_spawns):
            x_spawn = np.array([x_spawns[0][i_spawn], x_spawns[1][i_spawn]])
            if i_spawn == chest_spawn:
                self.lab_map[x_spawn[0], x_spawn[1]] = obj.chest
            elif i_spawn in guard_spawns:
                self.lab_map[x_spawn[0], x_spawn[1]] = obj.guard
                self.guards.append(x_spawn)
            else:
                self.lab_map[x_spawn[0], x_spawn[1]] = obj.space
        
    def create_panel(self):
        # images button https://fontawesome.com/v4.7.0/icons/
        items_layout = Layout( width='40px')     # override the default width of the button to 'auto' to let the button grow

        b_up   = Button(description='',icon = 'fa-arrow-up', layout = items_layout)
        b_down = Button(description='',icon = 'fa-arrow-down', layout = items_layout)
        b_left = Button(description='',icon = 'fa-arrow-left', layout = items_layout)
        b_right= Button(description='',icon = 'fa-arrow-right', layout = items_layout)
        b_hide = Button(description='',icon = 'fa-low-vision', layout = items_layout)
        b_pick = Button(description='',icon = 'fa-hand-paper-o', layout = items_layout)
        b_dummy = Label(layout = items_layout) #Button(description='', layout = items_layout)

        box_layout = Layout(display='flex',
                            flex_flow='column',
                            align_items='stretch',
                            border='solid')
                            #,width='30%')

        hor1 = HBox([b_dummy, b_up, b_dummy])
        hor2 = HBox([b_left, b_dummy, b_right])
        hor3 = HBox([b_dummy, b_down, b_dummy])
        hor4 = HBox([b_hide, b_dummy, b_pick])
        
        self.label_step_counter = Label('')
        self.label_best_steps = Label('')
        self.label_game_status = Label('Идет игра')
        
        hor5 = HBox([Label("Число шагов:"), self.label_step_counter])
        hor6 = HBox([self.label_game_status])
        hor7 = HBox([Label("Best steps:"), self.label_best_steps])        
        items = [hor1, hor2, hor3, hor4, hor5, hor6, hor7]
        self.manage_panel = Box(children=items, layout=box_layout)

        b_right.on_click(self.on_b_right_clicked)
        b_left.on_click(self.on_b_left_clicked)
        b_up.on_click(self.on_b_up_clicked)
        b_down.on_click(self.on_b_down_clicked) 
        b_hide.on_click(self.on_b_hide_clicked)
        b_pick.on_click(self.on_b_pick_clicked) 
        
        # панель запуска-остановки-паузы
        #b_restart = Button(description='ИГРА',icon = 'fa-refresh', layout = items_layout)
        b_play = Button(description='ИГРА',icon = 'fa-play')#, layout = items_layout)
        b_stop = Button(description='СТОП',icon = 'fa-stop')#, layout = items_layout)
        b_play_bot = Button(description='БОТ ',icon = 'fa-android')#, layout = items_layout)
        self.label_level = Label('1')
        #b_pause = Button(description='',icon = 'fa-pause', layout = items_layout)
        
        b_play.on_click(self.start) 
        b_stop.on_click(self.stop) 
        b_play_bot.on_click(self.start_bot) 

        self.start_stop_panel = VBox([b_play, b_stop, b_play_bot, HBox([Label('Уровень:'),self.label_level])], layout=box_layout)        
            
    def on_b_right_clicked(self, b):
        x_player_plan = self.get_x_player()
        x_player_plan[1] += 1
        self.player_move(x_player_plan)

    def on_b_left_clicked(self, b):
        x_player_plan = self.get_x_player()
        x_player_plan[1] -= 1
        self.player_move(x_player_plan)

    def on_b_up_clicked(self, b):
        x_player_plan = self.get_x_player()
        x_player_plan[0] -= 1
        self.player_move(x_player_plan)

    def on_b_down_clicked(self, b):
        x_player_plan = self.get_x_player()
        x_player_plan[0] += 1
        self.player_move(x_player_plan)

    def on_b_hide_clicked(self, b):
        self.player_hide()

    def on_b_pick_clicked(self, b):
        self.player_pick()
        
    def get_x_player(self):
        x_player = np.where(self.lab_map == obj.player)
        x_player = np.array([x_player[0][0], x_player[1][0]])
        return x_player

    def get_x_chest(self):
        x_player = np.where(self.lab_map == obj.chest)
        x_player = np.array([x_player[0][0], x_player[1][0]])
        return x_player

    def get_x_guard(self):
        x_player = np.where(self.lab_map == obj.guard)
        x_player = np.array([x_player[0][0], x_player[1][0]])
        return x_player
    
    def check_state(self):
        return not self.state in [player_state.win, player_state.loss]
    
    def check_time(self):
        if (datetime.datetime.now() - self.last_click).total_seconds() < self.time_lag: return False
        self.last_click = datetime.datetime.now()    
        return True
    
    def check_x(self, x_player_plan, wall_only = False):
        if x_player_plan[0] < 0 or x_player_plan[0] > self.map_size - 1: return False
        if x_player_plan[1] < 0 or x_player_plan[1] > self.map_size - 1: return False
        if (not wall_only):
            old_value = self.lab_map[x_player_plan[0], x_player_plan[1]]
            if old_value != obj.space: return False
        return True  
    
    def player_move(self, x_player_plan):
        if not self.check_time(): return False
        if not self.check_x(x_player_plan): return False
        if not self.check_state(): return False        
        self.state = player_state.show
        x_player = self.get_x_player()
        self.lab_map[x_player[0], x_player[1]] = obj.space
        self.lab_map[x_player_plan[0], x_player_plan[1]] = obj.player
        x_player = x_player_plan
        self.draw_map_fog()
        self.player_steps += 1
        self.update_game_status()

    def player_hide(self):
        if not self.check_time(): return False
        if not self.check_state(): return False                
        self.state = player_state.hide
        self.draw_map_fog()

    def player_pick(self):
        if not self.check_time(): return False
        if not self.check_state(): return False                
        x_player = self.get_x_player()
        x_chest = self.get_x_chest()
        if np.sum(np.abs(x_player - x_chest)) == 1:
            self.lab_map[x_player[0], x_player[1]] = obj.space        
            self.lab_map[x_chest[0], x_chest[1]] = obj.player
            self.player_steps += 1
            self.state = player_state.win
            self.draw_map_fog()            
            self.update_game_status()
        
    def draw_map_fog(self):
        """Рисуем вокруг игрока все на одну ячейку, учитывая границу лабиринта"""
        x_player = self.get_x_player()
        with hold_canvas(self.canvas):
            self.canvas.clear()
            for row in range(max(x_player[0] - 1, 0), min(x_player[0] + 1, self.map_size - 1)+1):
                for col in range(max(x_player[1] - 1, 0), min(x_player[1] + 1, self.map_size - 1)+1):
                    value = self.lab_map[row, col]
                    """
                    if value == obj.player:
                        self.canvas.fill_style = self.colordict[(value, self.state)]
                    else:
                        self.canvas.fill_style = self.colordict[value]
                    self.canvas.fill_rect(col * self.n_pixels, row * self.n_pixels, self.n_pixels, self.n_pixels)
                    """
                    if value == obj.player:
                        self.canvas.draw_image(self.imagedict[(value, self.state)], col * self.n_pixels, row * self.n_pixels)
                    elif value == obj.guard:
                        for i_guard in range(0, len(self.guard_objects)):
                            if np.array_equal(self.guard_objects[i_guard].x_guard, np.array([row, col])):
                                self.canvas.draw_image(self.imagedict[value][i_guard], col * self.n_pixels, row * self.n_pixels)
                                break
                    else:
                        self.canvas.draw_image(self.imagedict[value], col * self.n_pixels, row * self.n_pixels)

    def update_game_status(self):
        if not self.check_state():
            self.stop_threads()

        self.label_step_counter.value = str(self.player_steps)
        if self.state == player_state.win:
            self.label_game_status.value = 'Победа!'
            if self.player_steps < self.best_steps: self.best_steps = self.player_steps
            self.label_best_steps.value = str(self.best_steps)
            sleep(3)
            self.new_level()
        elif self.state == player_state.loss:       
            self.label_game_status.value = 'Проигрыш (('
        else:       
            self.label_game_status.value = 'Идет игра...'

    def stop_threads(self):
        if self.bot_object is not None:
            self.bot_object.stop = True

        for guard in self.guard_objects:
            guard.stop = True
                    
    def launch(self):
        self.cur_level = 1
        self.init_map()
        self.init_images()
        self.create_panel()

        multi = MultiCanvas(2, width=self.map_size * self.n_pixels, height=self.map_size * self.n_pixels)
        multi[0].fill_style = 'black'
        multi[0].fill_rect(0, 0, multi.size[0], multi.size[1])
        self.canvas = multi[1]
        self.output = widgets.Output()
        display(VBox([Image.from_file(path + '/images/header.jpg', width=200,height=40), HBox([multi, self.manage_panel, self.start_stop_panel])]), self.output)
        
    def new_level(self):
        if (len(levels) > self.cur_level):
            self.cur_level += 1
            self.label_level.value = str(self.cur_level)
            self.start()
        else:
            self.label_game_status.value = "Ты прошел все!"

    def start(self, b = True):
        self.last_click = datetime.datetime.now()
        self.time_start = datetime.datetime.now()
        self.init_map()
        self.spawn()

        self.state = player_state.show
        self.player_steps = 0
        self.update_game_status()
        
        self.guard_objects = []
        for x_guard in self.guards:
            guard = Guard(self, x_guard)
            self.guard_objects.append(guard)
            guard.start()
        self.draw_map_fog()    

        if self.bot_mode:
            if (self.bot is None):
                print('Бот не активирован!')
                self.stop(b)
                return
            self.create_bot()

        self.output.clear_output()

    def start_bot(self, b):
        self.bot_mode = True
        self.start(b)

    def create_bot(self):
        self.bot_object = Bot(self)
        self.bot_object.start()

    def stop(self, b):        
        self.state = player_state.loss
        self.update_game_status()        
        
    def set_bot(self, bot, debug_bot = False):
        "передача функции с ботом типа bot(obj_up, obj_down, obj_left, obj_right)"
        self.bot = bot
        self.debug_bot = debug_bot


class DangerLabirintGameMap(DangerLabirintGame):
    def create_bot(self):
        self.bot_object = BotMap(self)
        self.bot_object.start()

    def set_bot(self, bot, debug_bot = False):
        "передача функции с ботом типа bot(obj_up, obj_down, obj_left, obj_right, level_map, row, col)"
        self.bot = bot
        self.debug_bot = debug_bot

class DLGameTask(DangerLabirintGameMap):
    def move(self, dir):
        # dir: right, left, down, up
        sleep(0.5)
        x_player = self.get_x_player()
        if dir == 'up':
            x_player[0] -= 1
        elif dir == 'down':
            x_player[0] += 1
        elif dir == 'left':
            x_player[1] -= 1
        elif dir == 'right':
            x_player[1] += 1
        return self.player_move(x_player)
    
    def hide(self):
        sleep(0.5)
        self.player_hide()

    def pick(self):
        sleep(0.5)
        self.player_pick()

    def get_guard_pos(self):
        # позиция стража
        return tuple(self.get_x_guard())

    def get_chest_pos(self):
        # позиция сокровища
        return tuple(self.get_x_chest())

    def get_pos(self):
        # позиция игрока
        return tuple(self.get_x_player())

    def get_obj_dict(self):
        # осмотреться
        objs = {}
        x_player = self.get_x_player()
        x_player_dir = x_player.copy()
        x_player_dir[0] -= 1
        objs['up'] = obj.wall if not self.check_x(x_player_dir, True) else self.lab_map[x_player_dir[0], x_player_dir[1]]
        
        x_player_dir = x_player.copy()
        x_player_dir[0] += 1
        objs['down'] = obj.wall if not self.check_x(x_player_dir, True) else self.lab_map[x_player_dir[0], x_player_dir[1]]

        x_player_dir = x_player.copy()
        x_player_dir[1] -= 1
        objs['left'] = obj.wall if not self.check_x(x_player_dir, True) else self.lab_map[x_player_dir[0], x_player_dir[1]]

        x_player_dir = x_player.copy()
        x_player_dir[1] += 1
        objs['right'] = obj.wall if not self.check_x(x_player_dir, True) else self.lab_map[x_player_dir[0], x_player_dir[1]]

        return objs


    def get_objs(self):
        x_player = self.get_x_player()
        x_player_dir = x_player.copy()
        x_player_dir[0] -= 1
        obj_up = obj.wall if not self.check_x(x_player_dir, True) else self.lab_map[x_player_dir[0], x_player_dir[1]]
        
        x_player_dir = x_player.copy()
        x_player_dir[0] += 1
        obj_down = obj.wall if not self.check_x(x_player_dir, True) else self.lab_map[x_player_dir[0], x_player_dir[1]]

        x_player_dir = x_player.copy()
        x_player_dir[1] -= 1
        obj_left = obj.wall if not self.check_x(x_player_dir, True) else self.lab_map[x_player_dir[0], x_player_dir[1]]

        x_player_dir = x_player.copy()
        x_player_dir[1] += 1
        obj_right = obj.wall if not self.check_x(x_player_dir, True) else self.lab_map[x_player_dir[0], x_player_dir[1]]

        return [obj_up, obj_down, obj_left, obj_right]

    def run_task(self, task):
        # загрузить карту задачи (по справочнику)
        _level_task = levels_task[task]
        _levels = {1:_level_task}
        self.set_levels(_levels)
        # запустить задачу без меню справа (кнопок)
        self.launch()
        self.start()
        # выдать: задача пройдена!

    def update_game_status(self):
        if not self.check_state():
            self.stop_threads()

        if self.state == player_state.win:
            print('Задача решена! Переходи к следующей...')
        elif self.state == player_state.loss:       
            print('Не получилось... Попробуй еще раз?')
        else:       
            self.label_game_status.value = 'Идет игра...'

    def launch(self):
        self.cur_level = 1
        self.init_map()
        self.init_images()
        self.create_panel()

        multi = MultiCanvas(2, width=self.map_size * self.n_pixels, height=self.map_size * self.n_pixels)
        multi[0].fill_style = 'black'
        multi[0].fill_rect(0, 0, multi.size[0], multi.size[1])
        self.canvas = multi[1]
        self.output = widgets.Output()
        display(VBox([Image.from_file(path + '/images/header.jpg', width=200,height=40), HBox([multi])]), self.output)        

if __name__ == "__main__":
    game = DangerLabirintGame()
    game.set_levels(levels)
    #game.set_bot(bot, True)
    game.launch()
