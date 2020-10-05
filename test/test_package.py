import dangerlab.game as game
import dangerlab.levels as levels

import playsound
playsound.playsound('win.mp3')

labgame = game.DangerLabirintGame()
labgame.set_levels(levels.levels)
labgame.launch()