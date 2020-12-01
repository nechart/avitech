from ..strikeball.player import Player as basePlayer
from ..mine.enums import *
from .server import Server
from .client import Client
import getpass


class Player(basePlayer):
    def __init__(self, server_name, ava=None, user_name = None):
        self.client = Client(user_name)
        self.client.connect(server_name, ava)


def play_server(config, ava=None):
    servername = getpass.getuser() + '_server'
    server = Server.create(servername)
    server.init_map(config)
    server.launch()
    
    player = Player(servername, ava)
    player.client.server_obj = server
    return player