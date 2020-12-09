#import avi.dangerlab.game as game
from avi.mine.levels import levels as levels
import avi.mine.data.init as data_init
#import avi.survive.server as server
import avi.survive_camp.server as server
import avi.mine.player as player
import avi.mine.map as map
from avi.mine.data.base import connect as connect
from avi.mine.enums import *

"""
con = connect()
data_init.drop_tables(con)
data_init.create_tables(con)
con.close()
#server.Server.recreate_tables()
exit()
"""

"""
servername = 'survival' # #
server = server.Server.create(servername)
config=levels[servername] # 'empty']#]
config['food_per_sec'] = 0.3
#config['guards'] = 6
server.init_map(config)
server.launch()
"""
servername = 'camp' # #
server = server.Server.create(servername)
config=levels['camp'] 
config['food_per_sec'] = 0.3
server.init_map(config)
server.launch()