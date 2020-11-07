from enum import Enum

class obj:
    wall = 0
    space = 1
    player = 2
    guard = 3
    chest = 4

class server_state:
    inactive = 0
    active = 1
    pause = 2


class player_state:
    inactive = 0
    active = 1
    hide = 2


class action_state:
    to_process = 0
    in_working = 1
    processed = 2
    rejected = 3


class action:
    spawn = 0
    pick = 1
    hide = 2
    move_right = 3
    move_left = 4
    move_up = 5
    move_down = 6
    spawn_guard = 100
    spawn_chest = 101


class avatar:
    cowboy = 'cowboy'
    stan = 'stan'
    rock = 'rock'
    pig = 'pig'
    glass = 'glass'
    dipper = 'dipper'
    zoose  = 'zoose'
    super = 'super'
    garry = 'garry'
    chui = 'chui'
    lord = 'lord'
    bill = 'bill'