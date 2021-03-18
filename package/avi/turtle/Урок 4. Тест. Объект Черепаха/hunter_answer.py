import time
import turtle as tt
import random

# Нарисовать игровое окно
screen = tt.Screen()
screen.title('Поймай рыбку')
screen.bgcolor('aqua')
size = 300
border = 8
delta = 6

screen.setup((size + border)* 2, (size + border)*2)
screen.tracer(0)

# Нарисовать границу:
tt.hideturtle()
tt.color("blue")
sizeborder = size + border/2
tt.pensize(border)
tt.penup()
tt.goto(sizeborder - delta, -sizeborder + delta)
tt.pendown()
tt.goto(sizeborder - delta, sizeborder)
tt.goto(-sizeborder, sizeborder)
tt.goto(-sizeborder, -sizeborder  + delta)
tt.goto(sizeborder - delta, -sizeborder  + delta)
size = size - border

# Создать рыбку
fish = tt.Turtle()
fish.shape("arrow") # зададим форму стрелки
fish.color("yellow", "red")
fish.shapesize(1, 2, 6)
fish.penup()
fish.hideturtle()
# координаты и угол движения рыбки
fish.goto(random.randint(-size, size), random.randint(-size, size))
fish.seth(random.randint(0, 359)) # начальный угол наклона рыбы
fish.showturtle()

# Создать черепаху-охотника
hunt = tt.Turtle()
hunt.shape("turtle") # зададим форму мяча
hunt.color("grey", "black")
hunt.penup()
hunt.shapesize(2, 2, 6)

# Обработка нажатия клавиш
key = '' # название нажатой клавиши

def onkeypress(_key):
    global key
    key = _key

screen.onkeypress(lambda: onkeypress('Up'), 'Up') # Стрелка Вверх
screen.onkeypress(lambda: onkeypress('Down'), 'Down') # Стрелка Вниз
screen.onkeypress(lambda: onkeypress('Left'), 'Left') # Стрелка Влево
screen.onkeypress(lambda: onkeypress('Right'), 'Right') # Стрелка Вправо
screen.onkeypress(lambda: onkeypress('space'), 'space') # Пробел
screen.listen()


while True:
    # TODO: добавь сюда код проверки и обработки нажатия клавиши -->    
    if (key == 'space'):
        # print(hunt.distance(fish))
        if hunt.distance(fish) < 30:
            print('Win!')
            screen.bgcolor('red')
            break
            
    if (key == 'Up'):
        hunt.seth(90)
    if (key == 'Down'):
        hunt.seth(270)
    if (key == 'Left'):
        hunt.seth(180)
    if (key == 'Right'):
        hunt.seth(0)
    # TODO: добавь сюда код проверки и обработки нажатия клавиши -->

    # <--
    fish.forward(10)
    hunt.forward(5)
    
    # отражение рыбы
    if fish.xcor()>size:
        fish.seth(2*270 - fish.heading())
    elif fish.xcor()<-size:
        fish.seth(2*90 - fish.heading())
    elif fish.ycor()>size:
        fish.seth(2*360 - fish.heading())
    elif fish.ycor()<-size:
        fish.seth(2*180 - fish.heading())
    
    # отражение черепахи
    if hunt.xcor()>size:
        hunt.seth(2*270 - hunt.heading())
    elif hunt.xcor()<-size:
        hunt.seth(2*90 - hunt.heading())
    elif hunt.ycor()>size:
        hunt.seth(2*360 - hunt.heading())
    elif hunt.ycor()<-size:
        hunt.seth(2*180 - hunt.heading())        

    screen.update()
    time.sleep(0.1)

