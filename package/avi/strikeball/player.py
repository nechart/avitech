from ..mine.player import Player as minePlayer
from ..mine.enums import *
from .server import Server
#from .client import Client
#from . import map
import getpass


class Player(minePlayer):
    def __init__(self, server_name, ava=None):
        super().__init__(server_name, ava)

    def shoot(self, dir):
        # выстрелить
        dir_to_action = {'up':action.fire_up, 'left':action.fire_left, 'down':action.fire_down, 'right':action.fire_right}
        return self.client.make_action(dir_to_action[dir])

def play_server(config, ava=None):
    servername = getpass.getuser() + '_server'
    server = Server.create(servername)
    server.init_map(config)
    server.launch()
    player = Player(servername, ava)
    player.client.server_obj = server
    return player