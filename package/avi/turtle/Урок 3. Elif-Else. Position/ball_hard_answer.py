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
    # TODO: добавь сюда код проверки и обработки нажатия клавиши -->    
    if key == 'b':
        tt.color('green', 'blue')
        tt.end_fill()
        tt.begin_fill()
        key = ''
    elif key == 'g':
        tt.color('green', 'green')
        tt.end_fill()
        tt.begin_fill()
        key = ''
    elif key == 'r':
        tt.color('green', 'red')
        tt.end_fill()
        tt.begin_fill()
        key = ''
    elif key == 'y':
        tt.color('green', 'yellow')
        tt.end_fill()
        tt.begin_fill()
        key = ''

    # <--
    tt.forward(10)
    if tt.xcor()>size:
        tt.seth(2*270 - tt.heading())
    elif tt.xcor()<-size:
        tt.seth(2*90 - tt.heading())
    elif tt.ycor()>size:
        tt.seth(2*360 - tt.heading())
    elif tt.ycor()<-size:
        tt.seth(2*180 - tt.heading())

    screen.update()
    time.sleep(0.1)
