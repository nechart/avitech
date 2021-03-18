import turtle as tt

# Параметры
size = 120 # ширина - высота поля
rows = 24 # кол-во рядов
cols = 8 # кол-во столбцов


# Нарисовать игровое окно
screen = tt.Screen()
screen.title('Кирпичная стена')
screen.bgcolor('aqua')
screen.setup(2*size+100, 2*size+100)

rowsize = size // rows
colsize = size // cols
brick = tt.Turtle()
brick.color('lightgray', 'darkred')
brick.shape("square")
brick.shapesize(0.5, 1.6, 3)
brick.speed(10)
brick.up()

row = 0
while row < rows:
    col = 0
    while col < cols:
        y = -size + 2*size*row/rows
        x = -size + 2*size*col/cols
        brick.goto(x, y)
        brick.stamp()
        col += 1
    row += 1
