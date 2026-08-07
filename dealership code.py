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
        Option1=int(input("From out options, What would you like to pick? "))
        if Option1 == 1:
            exit()
        elif Option1 == 2:
            exit()
        elif Option1 == 3:
            exit()
        else:
            print("Sorry, please try again")
            time.sleep(5)
            goto(1)