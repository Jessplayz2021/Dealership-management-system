import time
from datetime import date

today = date.today()
d1 = today.strftime("%d")
m1 = today.strftime("%m")
y1 = today.strftime("%Y")
D1=int(d1)
M1=int(m1)
Y1=int(y1)

def goto(linenum):
    global line
    line = linenum
line = 1 
while True:
    if line == 1:
        print("Hello there, welcome to our dealership!")
        time.sleep(2)
        print("1 Car sales")
        print("2 Repairs/Warranty")
        print("3 Just browsing")
        int(input("Out of our options, What do you need today"))
        