#import avi.dangerlab.game as game
from avi.mine.levels import levels as levels
import avi.mine.data.init as data_init
import avi.mine.server as server
import avi.mine.player as player
import avi.mine.map as map
from avi.mine.data import user
from avi.mine.data.base import connect as connect
from avi.mine.enums import *

#con = connect()
#user.set_user_setup('aaa', 'bbb', con)
from avi.mine.levels import levels as levels
from avi.mine.enums import *
import avi.strikeball.player as player
config=levels['crest']
AVATAR = avatar.bill
game = player.play_server(config, AVATAR)
exit()

#data_init.drop_tables(con)
#data_init.create_tables(con)
#con.close()
server.Server.recreate_tables()
exit()

servername = '4cubes'
server = server.Server.create(servername)
config=levels[servername]
config['guards'] = 1
server.init_map(config)
server.launch()

#m = map.find_all(server.id)
#print(m)
#exit(1)

def test_client():
    game = player.Player('empty', avatar.lord) 
    #game.play() # отобразить игру. статус игрока меняется на 1
    if game.active():  # active проверяет статус сервера и игрока. если сервер выключился - выходит, если игрок умер (статус 2, выполняем game.reconnect()
        pos = game.get_chests()[0]
        userpos = game.get_pos()
        deltapos = (pos[0] - userpos[0], pos[1] - userpos[1])
        if deltapos[0] > 0:
            for _ in range(deltapos[0]):
                if not game.move_down():
                    if  game.pick():
                        print('picked {}'.format( len(game.get_chests())))
                        break
        elif deltapos[0] < 0:
            for _ in range(-deltapos[0]):        
                if not game.move_up():
                    if  game.pick():
                        print('picked {}'.format( len(game.get_chests())))
                        break
        checkpos = game.get_pos()

        if deltapos[1] > 0:
            for _ in range(deltapos[1]):
                if not game.move_right():
                    if  game.pick():
                        print('picked {}'.format( len(game.get_chests())))
                        break
        elif deltapos[1] < 0:
            for _ in range(-deltapos[1]):        
                if not game.move_left():
                    if  game.pick():
                        print('picked {}'.format( len(game.get_chests())))
                        break
        checkpos = game.get_pos()

        objs = game.get_objs() # select from map
        if obj.chest in objs.values():
            if  game.pick():
                print('picked end {}'.format( len(game.get_chests())))
        print('stop main')

#test_client()