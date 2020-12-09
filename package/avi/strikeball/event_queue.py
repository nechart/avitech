from time import sleep
from time import gmtime, strftime
from datetime import datetime

from ..mine.event_queue import EventQueue as mineEventQueue
from ..mine.enums import *
from .ball import Ball
from ..mine.data import user
from ..mine import map

class EventQueue(mineEventQueue):
    def __init__(self, server):
        super().__init__(server)

    def score_kill(self, user_rec, cell):
        user_rec['score'] += 3

    def shot(self, user_rec):
        return True

    def process_event(self, event_rec):
        #print(datetime.now())
        # выстрел шариком
        if event_rec['action'] in [action.fire_down, action.fire_up, action.fire_left, action.fire_right]:
            user_rec = user.find_user(event_rec['userid'], con=self.server.con)
            if user_rec['state'] in [player_state.active, player_state.hide]:
                row = user_rec['row']+1 if event_rec['action'] == action.fire_down else user_rec['row']-1 if event_rec['action'] == action.fire_up else user_rec['row']
                col = user_rec['col']+1 if event_rec['action'] == action.fire_right else user_rec['col']-1 if event_rec['action'] == action.fire_left else user_rec['col']
                if not map.check_coords(self.server.server, row, col):
                    event_rec['state'] = action_state.rejected
                elif map.find_cell(self.server.id, row, col, con=self.server.con)['obj'] != obj.space: # нельзя стрелять в упор
                    event_rec['state'] = action_state.rejected
                elif self.server.userballs.get(event_rec['userid'], 0) > 0:  # шар уже выстрелил у данного пользователя
                    event_rec['state'] = action_state.rejected
                else:
                    if self.shot(user_rec):
                        user.update_user(user_rec, con=self.server.con)
                        ballid = self.server.ball_last_id
                        self.server.ball_last_id += 1

                        cell = map.find_cell(self.server.id, row, col, con=self.server.con)
                        cell['obj'] = obj.ball
                        cell['userid'] = ballid
                        cell['image'] = ava_ball.ball
                        map.update_cell(cell, self.server.con)

                        ball = Ball(self.server, ballid, event_rec['userid'], event_rec['action'])
                        ball.start()
                        self.server.balls[ballid] = ball
                        self.server.userballs[event_rec['userid']] = self.server.userballs.get(event_rec['userid'], 0) + 1

        # движение шарика
        elif event_rec['action'] in [action.ball_move_down, action.ball_move_up, action.ball_move_left, action.ball_move_right]:
            ball = self.server.balls.get(event_rec['userid'], None)
            if ball is None or ball.stop:
                event_rec['state'] = action_state.rejected
            else:
                user_orig_rec = user.find_user(ball.userid, con=self.server.con)
                row = ball.cell['row']+1 if event_rec['action'] == action.ball_move_down else ball.cell['row']-1 if event_rec['action'] == action.ball_move_up else ball.cell['row']
                col = ball.cell['col']+1 if event_rec['action'] == action.ball_move_right else ball.cell['col']-1 if event_rec['action'] == action.ball_move_left else ball.cell['col']
                cell = map.find_cell(self.server.id, row, col, con=self.server.con)
                # если вылетели за границу или врезались в кого-то, то уничтожаем шарик
                if not map.check_coords(self.server.server, row, col) or cell['obj'] != obj.space:
                    ball.stop = True
                    self.server.userballs[ball.userid] = self.server.userballs.get(event_rec['userid'], 1) - 1
                    del self.server.balls[event_rec['userid']]
                    cell_orig = map.find_cell(self.server.id, ball.cell['row'], ball.cell['col'], con=self.server.con)
                    cell_orig['obj'] = obj.space
                    cell_orig['userid'] = -1
                    cell_orig['image'] = ''
                    map.update_cell(cell_orig, self.server.con)
                    # попали в игрока
                    if cell and cell['obj'] == obj.player:
                        user_rec = user.find_user(cell['userid'], self.server.con)
                        if user_rec['state'] == player_state.active:
                            user_rec['kills'] += 1
                            user_rec['kill_dt'] = strftime("%Y-%m-%d %H:%M:%S", gmtime()) 
                            user_rec['state'] = player_state.killed
                            user.update_user(user_rec, con=self.server.con)
                            #user_orig_rec['score'] -= 10
                            user.update_user(user_orig_rec, con=self.server.con)
                    # попали в стража
                    elif cell and cell['obj'] == obj.guard:
                        guard = self.server.guards[cell['userid']]
                        if not guard.killed:
                            guard.killed = True
                            guard.kill_dt =  datetime.utcnow()
                            cell['image'] = ava_guard.killed
                            self.score_kill(user_orig_rec, cell)                            
                            map.update_cell(cell, self.server.con)
                            user.update_user(user_orig_rec, con=self.server.con)
                    # попали в мяч
                    elif cell and cell['obj'] == obj.ball:
                        ball = self.server.balls.get(cell['userid'], None)
                        if ball:
                            ball.stop = True
                            del self.server.balls[cell['userid']]
                            self.server.userballs[ball.userid] = self.server.userballs.get(ball.userid, 1) - 1
                        cell['obj'] = obj.space
                        cell['userid'] = -1
                        cell['image'] = ''
                        map.update_cell(cell, self.server.con)
                else:
                    map.change_cells(self.server.id, (ball.cell['row'], ball.cell['col']), (row, col), self.server.con)

        # если событие еще не обработано, обработать его
        else:
            event_rec = super().process_event(event_rec)
        return event_rec