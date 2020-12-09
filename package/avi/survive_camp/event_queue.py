from time import sleep
from time import gmtime, strftime
from datetime import datetime

from ..strikeball.event_queue import EventQueue as baseEventQueue
from ..mine.enums import *
from ..mine.data import user
from ..mine import map

class EventQueue(baseEventQueue):
    def __init__(self, server):
        super().__init__(server)

    def find_empty_place(self, user_rec):
        location = self.server.locations[user_rec['team']]
        
        rows = (location[0] - 4, location[0] + 4)
        cols = (location[1] - 4, location[1] + 4)

        return map.find_empty_place(self.server.server, rows, cols, con=self.server.con)

    def score_pick(self, user_rec, chest):
        user_params = user.read_params(user_rec['params'])
        user_params['hands'] += 1 if chest == ava_chest.chest1 else 2 if chest == ava_chest.chest2 else 3
        user_params['spaces'] -= 1
        user_rec['params'] = user.write_params(user_params)        

    def score_kill(self, user_rec, cell):
        cell['obj'] = obj.chest
        cell['userid'] = -1
        cell['image'] = ava_chest.bulk

    def shot(self, user_rec):
        user_params = user.read_params(user_rec['params'])
        if user_params['bullets'] > 0:
            user_params['bullets'] -= 1
            user_rec['params'] = user.write_params(user_params)
            return True
        else:
            return False

    def check_space(self, user_rec):
        user_params = user.read_params(user_rec['params'])
        return user_params['spaces'] > 0


    def process_event(self, event_rec):
        # выгрузить товар на склад
        if event_rec['action'] == action.put:
            user_rec = user.find_user(event_rec['userid'], con=self.server.con)
            if user_rec['state'] in [player_state.active, player_state.hide]:
                objs = map.get_objs(self.server.server, user_rec['row'], user_rec['col'], self.server.con)
                if not obj.building in objs.values():
                    event_rec['state'] = action_state.rejected
                else:
                    user_params = user.read_params(user_rec['params'])
                    user_rec['score'] += user_params['hands']
                    user_params = user.init_params()
                    user_rec['params'] = user.write_params(user_params)
                    user_rec['state'] = player_state.active
                    user.update_user(user_rec, con=self.server.con)
            else:
                event_rec['state'] = action_state.rejected
        else:
            event_rec = super().process_event(event_rec)
        return event_rec