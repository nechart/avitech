import time
import turtle as tt
import random

# Нарисовать игровое окно
screen = tt.Screen()
screen.title('Арканоид')
screen.bgcolor('black')
size_x = 400
size_y = 300
delta = 30
bitsize = 50
ballsize = 10
tilesize = 30
ballspeed = 10
bitspeed = 5

screen.setup((size_x + delta)* 2, (size_y + delta)*2)
screen.tracer(0)

# Нарисовать границу:
tt.hideturtle()
tt.color("yellow")
#tt.pensize(1)
tt.penup()
tt.goto(-size_x, size_y)
tt.pendown()
tt.goto(size_x, size_y)
tt.goto(size_x, -size_y)
tt.goto(-size_x, -size_y)
tt.goto(-size_x, size_y)

# Создать биту
bit = tt.Turtle()
bit.shape("square") # зададим форму стрелки
bit.color("yellow", "red")
bit.shapesize(0.5, 5, 3)
bit.penup()
bit.goto(0, - size_y + ballsize)
bit.showturtle()

# Создать мяч
ball = tt.Turtle()
ball.shape("circle") # зададим форму стрелки
ball.color("red", "yellow")
#bit.shapesize(0.5, 5, 3)
ball.penup()
ball.seth(random.randint(20, 160)) # начальный угол наклона рыбы
ball.goto(0, bit.ycor() + 2 * ballsize)
ball.showturtle()

# Создать плитку
tile = tt.Turtle()
tile.shape("square") # зададим форму стрелки
tile.color("green", "aqua")
tile.shapesize(1, 3, 3)
tile.penup()
tile.goto(random.randint(-size_x, size_x), random.randint(0, size_y))
tile.showturtle()

# Обработка нажатия клавиш
key = '' # название нажатой клавиши

def onkeypress(_key):
    global key
    key = _key

screen.onkeypress(lambda: onkeypress('Up'), 'Up') # Стрелка Вверх
screen.onkeypress(lambda: onkeypress('Down'), 'Down') # Стрелка Вниз
screen.listen()


while True:
    if (key == 'Left'):
        bit.seth(180)
        key = ""
    elif (key == 'Right'):
        bit.seth(0)
        key = ""

    # отражение мяча от границы
    if ball.xcor()>size_x-ballsize:
        ball.seth(2*270 - ball.heading())
    elif ball.xcor()<-size_x+ballsize:
        ball.seth(2*90 - ball.heading())
    elif ball.ycor()>size_y-ballsize:
        ball.seth(2*360 - ball.heading())

    # попадание мяча в плитку
    if abs(ball.ycor()-tile.ycor()) < 2*ballsize and abs(ball.xcor()-tile.xcor()) < tilesize:
        tile.hideturtle()
        screen.update()
        screen.bgcolor('green')
        break

    # выход мяча за границу поля
    if ball.ycor() < -size_y:
        screen.bgcolor('red')
        break

    # TODO:  -->    
    # отражение биты от границы
    
    # отражение мяча от биты
    # TODO:  <--

    ball.fd(ballspeed)
    bit.fd(bitspeed)

    screen.update()
    time.sleep(0.05)