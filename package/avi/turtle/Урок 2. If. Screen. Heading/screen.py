import turtle as tt

# draw a window for the game
screen = tt.Screen()
screen.title('Экран')
screen.bgcolor('blue')
screen.setup (width=300, height=400)

tt.begin_fill()
tt.color("red", "yellow")
tt.forward(100)
tt.seth(240)
tt.forward(100)
tt.seth(120)
tt.forward(100)
tt.end_fill()