from ..survive.server import Server as baseServer
from ..mine.enums import *
#from .client import Client
from .event_queue import EventQueue as EventQueue

class Server(baseServer):
    def __init__(self, server_name, teams=2):
        self.teams = 2
        super().__init__(server_name)

    def getEventQueue(self):
        return EventQueue

    def start_guards(self):
        super().start_guards()
        self.balls = {}
        self.userballs = {}
        self.ball_last_id = 0  # код последнего патрона (инкрементный)

        # инициализировать склады
        self.locations = {}
        for team in range(self.teams):
            self.locations[team] = self.config['teams'][team]['location']

    def stop_guards(self):
        super().stop_guards()
        for ball in self.balls.values():
            ball.stop = True        

    def init_params(self):
        self.params['teams'] = self.config['teams']


    @staticmethod
    def create(server_name):
        return Server(server_name)            