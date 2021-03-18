import time
import turtle as tt
import random

# Нарисовать игровое окно
screen = tt.Screen()
screen.title('Арканоид 2.0')
screen.bgcolor('aqua')
size_x = 400
size_y = 400
delta = 30
bitsize = 50
ballsize = 10
tilesize = 35
ballspeed = 10
bitspeed = 5
rows = 3
cols = 4
font=("Arial", 16, "normal")

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
bit.shape("circle") # зададим форму стрелки
bit.color("yellow", "red")
bit.shapesize(0.8, 5, 2)
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

# Создать список плиток
tiles = []
row = 0
while row <= rows:
    col = 0
    while col <= cols:
        tile = tt.Turtle()
        tile.shape("square") # зададим форму стрелки
        tile.color("green", "blue")
        tile.shapesize(1, 3, 3)
        tile.penup()
        x = -(size_x-tilesize) + (size_x-tilesize)*2*(col/cols)
        y = (size_y-ballsize) - size_y/2*(row/rows)
        tile.setpos(x, y)
        tile.showturtle()
        tiles.append(tile)
        col += 1
    row += 1
tile_count = len(tiles)
    
# Обработка нажатия клавиш
key = '' # название нажатой клавиши

def onkeypress(_key):
    global key
    key = _key

screen.onkeypress(lambda: onkeypress('Left'), 'Left') # Стрелка Влево
screen.onkeypress(lambda: onkeypress('Right'), 'Right') # Стрелка Вправо
screen.listen()

# Табло со счетом
score = 0 
board = tt.Turtle()
board.penup()
board.hideturtle()
board.setpos(size_x - 40, size_y)
board.write(str(score), font=font)

# игровой цикл
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

    # отражение биты от границы
    if bit.xcor()>size_x-bitsize:
        bit.seth(2*270 - bit.heading())
    elif bit.xcor()<-size_x+bitsize:
        bit.seth(2*90 - bit.heading())

    # отражение мяча от биты
    if ball.ycor()<bit.ycor()+2*ballsize and abs(ball.xcor() - bit.xcor()) < bitsize and ball.heading()>180:
        print(ball.heading())
        angle = 2*(180 - 15*(ball.xcor() - bit.xcor())/bitsize) - ball.heading()
        ball.seth(angle)
        print(ball.heading())

    # попадание мяча в плитки
    tile_i = 0
    while tile_i < tile_count:
        tile = tiles[tile_i]
        if abs(ball.ycor()-tile.ycor()) < 2*ballsize and abs(ball.xcor()-tile.xcor()) < tilesize:
            if (tile.ycor() > ball.ycor()): # мяч ударяет снизу
                ball.seth(2*360 - ball.heading())
            #TODO добавить отскок мяча, если он ударяет в плитку сверху -->
            
            #TODO добавить отскок мяча, если он ударяет в плитку сверху <--
            tile.hideturtle()
            tiles.remove(tile)
            tile_count -= 1
            
            #TODO добавить расчет очков и вывод их на табло -->
            
            #TODO добавить расчет очков и вывод их на табло <--
            break
        tile_i += 1
        
    # проверка на выигрыш
    if tile_count == 0:
        board.clear()
        board.write('WIN', font=font)
        screen.bgcolor('green')
        break

    # выход мяча за границу поля
    if ball.ycor() < -size_y:
        board.clear()
        board.write('LOSS', font=font)
        screen.bgcolor('red')
        break

    ball.fd(ballspeed)
    bit.fd(bitspeed)

    screen.update()
    time.sleep(0.02)