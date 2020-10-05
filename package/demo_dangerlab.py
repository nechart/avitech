import dangerlab.game as game
import dangerlab.levels as levels

labgame = game.DangerLabirintGame()
labgame.set_levels(levels.levels)
labgame.launch()
#print(levels.level1_map)