from enum import Enum

class obj:
    wall = 0
    space = 1
    player = 2
    guard = 3
    chest = 4

class player_state:
    show = 0
    hide = 1
    loss = 2
    win = 3