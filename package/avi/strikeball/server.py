from ..mine.server import Server as mineServer
from ..mine.enums import *
#from .client import Client
from .event_queue import EventQueue as EventQueue

class Server(mineServer):
    def __init__(self, server_name):
        super().__init__(server_name)

    def getEventQueue(self):
        return EventQueue

    def start_guards(self):
        super().start_guards()
        self.balls = {}
        self.userballs = {}
        self.ball_last_id = 0  # код последнего патрона (инкрементный)

    def stop_guards(self):
        super().stop_guards()
        for ball in self.balls.values():
            ball.stop = True        

    @staticmethod
    def create(server_name):
        return Server(server_name)            