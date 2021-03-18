import time
import turtle as tt

# Нарисовать игровое окно
screen = tt.Screen()
screen.title('Накорми черепаху')
screen.bgcolor('orange')
screen.setup(650, 650)
screen.tracer(0)

key = '' # название нажатой клавиши

def onkeypress(_key):
    global key
    key = _key
    print(key)

screen.onkeypress(lambda: onkeypress('Up'), 'Up') # Стрелка Вверх
screen.onkeypress(lambda: onkeypress('Down'), 'Down') # Стрелка Вниз
screen.onkeypress(lambda: onkeypress('Left'), 'Left') # Стрелка Влево
screen.onkeypress(lambda: onkeypress('Right'), 'Right') # Стрелка Вправо
screen.onkeypress(lambda: onkeypress('space'), 'space') # Пробел
screen.listen()

tt.shape('turtle')
tt.color('green', 'red')

tt.begin_fill()
while True:
    if (key == 'space'):
        tt.end_fill()
        tt.begin_fill()                
    # TODO: добавь сюда код проверки и обработки нажатия клавиши -->
    # <--
    tt.forward(10)
    screen.update()
    time.sleep(0.1)

