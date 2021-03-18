import turtle as tt

# draw a window for the game
screen = tt.Screen()
screen.title('Граница')
screen.bgcolor('orange')
screen.setup (width=250, height=250)

# draw a game field border
tt.hideturtle()
tt.color("blue")
tt.penup()
tt.goto(-100, 100)
tt.pendown()
tt.forward(200)
tt.seth(270)
tt.forward(200)
tt.seth(180)
tt.forward(200)
tt.seth(90)
tt.forward(200)

tt.color("green")
tt.penup()
tt.goto(-50, 50)
tt.pendown()
tt.goto(50, 50)
tt.goto(50, -50)
tt.goto(-50, -50)
tt.goto(-50, 50)