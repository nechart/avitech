import time
import turtle as tt
import random
import pathlib
path_file = str(pathlib.Path(__file__).parent.absolute()) + "\\"

# Нарисовать игровое окно
screen = tt.Screen()
screen.title('Стрелок')
screen.bgcolor('white')
size_x = 400
size_y = 400
delta = 30

enemy_count = 5

playersize = 10
enemysize = 10
playerspeed = 5
enemyspeed = 10
bulletspeed = 10

font=("Arial", 16, "normal")

screen.setup((size_x + delta)* 2, (size_y + delta)*2)
screen.tracer(0)

# Нарисовать границу:
tt.hideturtle()
tt.color("blue")
#tt.pensize(1)
tt.penup()
tt.goto(-size_x, size_y)
tt.pendown()
tt.goto(size_x, size_y)
tt.goto(size_x, -size_y)
tt.goto(-size_x, -size_y)
tt.goto(-size_x, size_y)

# Создать стрелка
#screen.register_shape("player", "chui.gif") # "images\chui.gif"
# "images\chui.gif"
shapes = tt.getshapes()
player = tt.Turtle()
#player.shape("player") 
tt.register_shape(path_file + "images\\chui.gif") 
player.shape(path_file + "images\\chui.gif")
player.penup()
player.home()
player.showturtle()

# Создать несколько Зомби
tt.register_shape(path_file + "images\\guard1.gif")
enemies = []
enemy_i = 0
while enemy_i < enemy_count:
    enemy = tt.Turtle()
    enemy.penup()
    enemy.shape(path_file + "images\\guard1.gif") 
    enemy.goto(random.randint(-size_x, size_x), random.randint(-size_y, size_y))
    enemy.setheading(random.randint(0, 360))
    enemy.showturtle()
    enemy_i += 1
    enemies.append(enemy)

# Создать список пуль
bullets = []

"""
# Создать несколько кустов
screen.register_shape("wall", "images\wall.png")
walls = {}
wall_count = 10
wall_i = 0
while wall_i < wall_count:
    wall = tt.Turtle()
    wall.penup()
    wall.shape("wall") 
    wall.goto(random.randint(-size_x, size_x), random.randint(-size_y, size_y))
    wall.showturtle()
"""
# Обработка нажатия клавиш
key = '' # название нажатой клавиши

def onkeypress(_key):
    global key
    key = _key

screen.onkeypress(lambda: onkeypress('space'), 'space') # Пробел
screen.onkeypress(lambda: onkeypress('Up'), 'Up') # Стрелка Вверх
screen.onkeypress(lambda: onkeypress('Down'), 'Down') # Стрелка Вниз
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
    if (key == 'Up'):
        player.seth(90)
    elif (key == 'Down'):
        player.seth(270)
    elif (key == 'Left'):
        player.seth(180)
    elif (key == 'Right'):
        player.seth(0)
    elif (key == 'space'):
        bullet = tt.Turtle()
        bullet.penup()
        bullet.shape("circle") 
        bullet.color("red", "green")
        bullet.shapesize(0.3)
        bullet.setpos(player.pos())
        bullet.setheading(player.heading())
        bullet.showturtle()
        bullets.append(bullet)

    key = ""

    # отражение игрока от границы
    if player.xcor()>size_x-playersize:
        player.seth(180)
    elif player.xcor()<-size_x+playersize:
        player.seth(0)
    elif player.ycor()>size_y-playersize:
        player.seth(270)
    elif player.ycor()<-size_y+playersize:
        player.seth(90)

    player.fd(playerspeed)

    # движение зомби
    for enemy in enemies:
        # отражение зомби от границы
        if enemy.xcor()>size_x-enemysize and (enemy.heading() < 90 or enemy.heading() > 270):
            enemy.seth(2*270 - enemy.heading())
        elif enemy.xcor()<-size_x+enemysize and (enemy.heading() > 90 or enemy.heading() < 270):
            enemy.seth(2*90 - enemy.heading())
        elif enemy.ycor()>size_y-enemysize and enemy.heading() < 180:
            enemy.seth(2*360 - enemy.heading())
        elif enemy.ycor()<-size_y+enemysize and enemy.heading() > 180:
            enemy.seth(2*180 - enemy.heading())

        enemy.fd(enemyspeed)

        if enemy.distance(player) < playersize + enemysize:
            screen.bgcolor("red")
            board.clear()
            board.write("LOSS", font=font)
            exit()
    
    # движение пуль
    bullets_remove = []
    for bullet in bullets:
        bullet.fd(bulletspeed)
        if bullet.xcor()>size_x or bullet.xcor()<-size_x or bullet.ycor()>size_y or bullet.ycor()<-size_y:
            bullet.hideturtle()
            del bullet
            continue
        for enemy in enemies:
            if enemy.distance(bullet) <= enemysize:
                bullet.hideturtle()
                del bullet
                enemies.remove(enemy)
                enemy.hideturtle()
                del enemy
                score += 1
                board.clear()
                board.write(str(score), font=font)

                if len(enemies) == 0:
                    screen.bgcolor("green")                    
                    board.clear()
                    board.write("WIN", font=font)
                    exit()
                break 
    
    for bullet in bullets_remove:
        bullets.remove(bullet)
    del bullets_remove
        
    screen.update()
    time.sleep(0.02)