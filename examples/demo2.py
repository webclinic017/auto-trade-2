import turtle
import random
import math

# 初始化
turtle.setup(1280, 720)
t = turtle.Pen()
t.ht()

# 颜色
colors = []
t_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]

for i in t_list:
    t_str = "#ff00"
    for j in t_list:
        colors.append(t_str+i+j)


class Love():
    def __init__(self):
        # 定义变量
        self.r = random.randint(4, 10)
        self.x = random.randint(-900, 700)
        self.y = random.randint(-400, 400)
        self.i = random.randint(0, 10)
        self.color = random.choice(colors)
        self.speed = random.randint(1, 8)

    def move(self):
        # 通过y坐标来控制爱心
        if self.y <= 500:
            self.y += 2.5*self.speed
            self.x = self.x + 1.5*math.sin(self.i)*math.sqrt(self.i)*self.speed
            self.i = self.i + 0.1
        else:
            self.y = -700
            self.r = random.randint(5, 20)
            self.x = random.randint(-900, 700)
            self.i = 0
            self.color = random.choice(colors)
            self.speed = random.randint(1, 8)

    def draw(self):
        # 绘制爱心
        t.pensize(self.r/2)
        t.penup()
        t.color(self.color, self.color)
        t.goto(self.x, self.y)
        t.pendown()
        # 设置角度
        t.setheading(60)
        t.circle(self.r, 255)
        t.fd(2.4*self.r)
        t.left(90)
        t.fd(2.4*self.r)
        t.circle(self.r, 255)


love = []
for i in range(100):
    love.append(Love())
turtle.bgcolor("#000000")


while 1:
    turtle.tracer(0)
    t.clear()
    for i in range(80):
        love[i].move()
        love[i].draw()
    turtle.tracer(1)