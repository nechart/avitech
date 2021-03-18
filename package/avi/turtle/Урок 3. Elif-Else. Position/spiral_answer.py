import turtle as tt

# draw a window for the game
screen = tt.Screen()
screen.title('Спираль')
screen.bgcolor('blue')
screen.setup (width=200, height=200)

step=0.2
while(True):
    tt.left(2)
    tt.forward(step)
    step+=0.01
    #TODO: добавить проверку на отход на расстояние 100 от (0,0) и возврат черепахи home()
    if tt.distance(0,0) > 100:
        tt.penup()
        tt.home()
        tt.pendown()
        step=0.1