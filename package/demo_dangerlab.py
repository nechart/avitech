import avi.dangerlab.game as game
import avi.dangerlab.levels as levels

labgame = game.DangerLabirintGame()
labgame.set_levels(levels.levels)
labgame.launch()
print(levels.level1_map)