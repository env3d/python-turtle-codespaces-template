
# type: ignore
import turtle             

wn = turtle.Screen()

t = turtle.Turtle()

for i in range(20):   # repeat four times
    t.forward(50)
    t.left(30)

wn.exitonclick()
