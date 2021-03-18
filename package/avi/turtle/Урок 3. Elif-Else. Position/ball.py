import time
import turtle as tt

# Нарисовать игровое окно
screen = tt.Screen()
screen.title('Рисующий мяч')
screen.bgcolor('orange')
size = 300
screen.setup(size * 2, size * 2)
screen.tracer(0)

# Нарисовать границу:
tt.hideturtle()
tt.color("blue")
tt.penup()
tt.goto(-size, size)
tt.pendown()
tt.goto(size, size)
tt.goto(size, -size)
tt.goto(-size, -size)
tt.goto(-size, size)

# Вернуть черепаху домой
tt.penup()
tt.home()
tt.pendown()
tt.showturtle()
tt.shape("circle") # зададим форму мяча

key = '' # название нажатой клавиши

def onkeypress(_key):
    global key
    key = _key
    print(key)

screen.onkeypress(lambda: onkeypress('b'), 'b') # Стрелка Вверх
screen.onkeypress(lambda: onkeypress('g'), 'g') # Стрелка Вниз
screen.onkeypress(lambda: onkeypress('r'), 'r') # Стрелка Влево
screen.onkeypress(lambda: onkeypress('y'), 'y') # Стрелка Вправо
#screen.onkeypress(lambda: onkeypress('space'), 'space') # Пробел
screen.listen()

tt.color('green', 'red')

tt.seth(30) # выбери начальный угол наклона
tt.begin_fill()
while True:
    if key == 'b':
        tt.color('green', 'blue')
        tt.end_fill()
        tt.begin_fill()
        key = ''
    # TODO: добавь сюда код обработки нажатия клавиш r, g, y -->    

    # <--    

    tt.forward(10)
    
    if tt.xcor()>size:
        tt.seth(2*270 - tt.heading())
    # TODO: добавь сюда код проверки касания одной из границ и отскока мяча -->        
    
    # <--            

    screen.update()
    time.sleep(0.1)
