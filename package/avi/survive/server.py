from ..strikeball.server import Server as baseServer

class Server(baseServer):
    def __init__(self, server_name):
        super().__init__(server_name)
        self.resources = 0

    def init_map(self, config={}, mapname=''):
        self.server['food_per_sec'] = config.get('food_per_sec', 0.1)
        super().init_map(config, mapname)


    @staticmethod
    def create(server_name):
        return Server(server_name)            