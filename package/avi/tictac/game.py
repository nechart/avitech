"""
Game tic-tac-toe

"""


import datetime
import random
import copy
from time import sleep
import numpy as np
from ipywidgets import widgets, Label, HTML, HBox, Image, VBox, Box, HBox, Layout, Button
from ipycanvas import Canvas, MultiCanvas, hold_canvas
from IPython.display import display


class obj:
    space = 0
    robot = 1    
    player = 2


class player_state:
    show = 0
    loss = 2
    win = 3
    draw = 4


class TicGame:

    def __init__(self):
        self.bot = None
        self.map = list()
        self.buttons = list()
        self.state = player_state.show
            
    def init_images(self):   
        self.icons = {obj.space: 'fa-question', obj.robot: 'fa-circle-o', obj.player: 'fa-arrows-alt'}
        
    def init_map(self):
        self.map = [[0,0,0],
                    [0,0,0],
                    [0,0,0]]

    def create_panel(self):
        # images button https://fontawesome.com/v4.7.0/icons/
        items_layout = Layout( width='40px')     # override the default width of the button to 'auto' to let the button grow

        b_0_0  = Button(description='', layout = items_layout, icon = self.icons[obj.space])
        b_0_1  = Button(description='', layout = items_layout, icon = self.icons[obj.space])
        b_0_2  = Button(description='', layout = items_layout, icon = self.icons[obj.space])
        b_1_0  = Button(description='', layout = items_layout, icon = self.icons[obj.space])
        b_1_1  = Button(description='', layout = items_layout, icon = self.icons[obj.space])
        b_1_2  = Button(description='', layout = items_layout, icon = self.icons[obj.space])
        b_2_0  = Button(description='', layout = items_layout, icon = self.icons[obj.space])
        b_2_1  = Button(description='', layout = items_layout, icon = self.icons[obj.space])
        b_2_2  = Button(description='', layout = items_layout, icon = self.icons[obj.space])

        self.buttons = [[b_0_0, b_0_1, b_0_2],
                        [b_1_0, b_1_1, b_1_2],
                        [b_2_0, b_2_1, b_2_2],
                        ]
        
        box_layout = Layout(display='flex',
                            flex_flow='column',
                            align_items='stretch',
                            border='solid')
                            #,width='30%')

        hor1 = HBox([b_0_0, b_0_1, b_0_2])
        hor2 = HBox([b_1_0, b_1_1, b_1_2])
        hor3 = HBox([b_2_0, b_2_1, b_2_2])        
        
        #self.label_best_steps = Label('')
        self.label_game_status = Label('Идет игра')
        
        #hor5 = HBox([Label("Число шагов:"), self.label_step_counter])
        hor6 = HBox([self.label_game_status])
        #hor7 = HBox([Label("Best steps:"), self.label_best_steps])        
        items = [hor1, hor2, hor3, hor6] #, hor4, hor5, hor6, hor7]
        self.manage_panel = Box(children=items, layout=box_layout)

        b_0_0.on_click(self.on_b_0_0_clicked)
        b_0_1.on_click(self.on_b_0_1_clicked)
        b_0_2.on_click(self.on_b_0_2_clicked)
        b_1_0.on_click(self.on_b_1_0_clicked)
        b_1_1.on_click(self.on_b_1_1_clicked)
        b_1_2.on_click(self.on_b_1_2_clicked)
        b_2_0.on_click(self.on_b_2_0_clicked)
        b_2_1.on_click(self.on_b_2_1_clicked)
        b_2_2.on_click(self.on_b_2_2_clicked)
        
        # панель запуска-остановки-паузы
        #b_restart = Button(description='ИГРА',icon = 'fa-refresh', layout = items_layout)
        b_play = Button(description='ИГРА',icon = 'fa-play')#, layout = items_layout)
        b_stop = Button(description='СТОП',icon = 'fa-stop')#, layout = items_layout)
        #b_play_bot = Button(description='БОТ ',icon = 'fa-android')#, layout = items_layout)
        self.label_level = Label('1')
        #b_pause = Button(description='',icon = 'fa-pause', layout = items_layout)
        
        b_play.on_click(self.start) 
        b_stop.on_click(self.stop) 
        #b_play_bot.on_click(self.start_bot) 

        self.start_stop_panel = VBox([b_play, b_stop, HBox([Label('Уровень:'),self.label_level])], layout=box_layout)        
            
    def on_b_0_0_clicked(self, b):
        self.player_move((0,0))
    def on_b_0_1_clicked(self, b):
        self.player_move((0,1))
    def on_b_0_2_clicked(self, b):
        self.player_move((0,2))
    def on_b_1_0_clicked(self, b):
        self.player_move((1,0))
    def on_b_1_1_clicked(self, b):
        self.player_move((1,1))
    def on_b_1_2_clicked(self, b):
        self.player_move((1,2))
    def on_b_2_0_clicked(self, b):
        self.player_move((2,0))
    def on_b_2_1_clicked(self, b):
        self.player_move((2,1))
    def on_b_2_2_clicked(self, b):
        self.player_move((2,2))

    def player_move(self, cell):
        if self.check_cell(cell) is not True: return False
        if self.check_state() is not True: return False        
        self.map[cell[0]][cell[1]] = obj.player
        self.draw_map()
        self.check_game_status()
        self.update_game_status()
        
        if self.check_state() is not True: return True
        
        map_bot = copy.deepcopy(self.map)
        self.bot(map_bot, cell[0], cell[1])
        
        map_ar = np.array(self.map)
        bot_ar = np.array(map_bot)
        
        if sum(sum(bot_ar - map_ar)) != 1:
            raise Exception("Бот поставил нолик на занятый участок!")
        
        self.map = map_bot
        self.draw_map()
        self.check_game_status()        
        self.update_game_status()

    def check_state(self):
        return self.state not in [player_state.win, player_state.loss, player_state.draw]
  
    def check_cell(self, cell):
        return self.map[cell[0]][cell[1]] == obj.space
        
    def draw_map(self):
        with hold_canvas(self.canvas):
            self.canvas.clear()
            for row in range(len(self.map)):
                for col in range(len(self.map[0])):
                    value = self.map[row][col]
                    self.buttons[row][col].icon = self.icons[value]
                    self.buttons[row][col].disabled = value != obj.space

    def is_obj_win(self, obj_state = obj.player):
        win = False
        for irow in range(3):
            if (self.map[irow][0] == self.map[irow][1] == self.map[irow][2] == obj_state):
                win = True
                break
        for icol in range(3):
            if (self.map[0][icol] == self.map[1][icol] == self.map[2][icol] == obj_state):
                win = True
                break
        if self.map[0][0] == self.map[1][1] == self.map[2][2] == obj_state:
            win = True
        if self.map[0][2] == self.map[1][1] == self.map[2][0] == obj_state:
            win = True
        return win

    def check_game_status(self):
        if min(min(self.map[0]), min(self.map[1]), min(self.map[2])) > obj.space:
            self.state = player_state.draw
        if self.is_obj_win(obj.player):
            self.state = player_state.win
        if self.is_obj_win(obj.robot):
            self.state = player_state.loss
        return 
    
    def update_game_status(self):
        if self.state == player_state.win:
            self.label_game_status.value = 'Победа!'
        elif self.state == player_state.loss:       
            self.label_game_status.value = 'Проигрыш (('
        elif self.state == player_state.draw:       
            self.label_game_status.value = 'Ничья'
        else:       
            self.label_game_status.value = 'Идет игра...'
                    
    def launch(self):
        self.init_map()
        self.init_images()
        self.create_panel()
        n_pixels = 40
        multi = MultiCanvas(2,  width=3 * n_pixels, height=3 * n_pixels)
        multi[0].fill_style = 'black'
        multi[0].fill_rect(0, 0, multi.size[0], multi.size[1])
        self.canvas = multi[1]
        self.output = widgets.Output()
        display(VBox([HBox([self.manage_panel, self.start_stop_panel])]), self.output)
        
    def new_level(self):
        self.start()

    def start(self, b = True):
        self.last_click = datetime.datetime.now()
        self.time_start = datetime.datetime.now()
        self.init_map()
        
        #self.launch()
        self.state = player_state.show
        self.update_game_status()
        
        self.draw_map()    
        self.output.clear_output()


    def stop(self, b):        
        self.state = player_state.loss
        self.update_game_status()         
        
    def set_bot(self, bot, debug_bot=False):
        """
        задать функцию для бота с сигнатурой: bot(level_map)
        """
        self.bot = bot
        self.debug_bot = debug_bot

if __name__ == "__main__":
    game = TicGame()
    #game.set_levels(levels)
    #game.set_bot(bot, True)
    #game.launch()
