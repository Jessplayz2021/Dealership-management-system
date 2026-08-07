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
            input("Okay, What car or lot number do you wish for? ")
        elif Option1 == 2:
            print("I'm sorry for the issue, please allow me a few seconds to get someone over for you.")
            time.sleep(5)
            print("Thank you for waiting.")
            time.sleep(1)
        elif Option1 == 3:
            print("Okay... Here's a few questions I'd like to ask to narrow down your choices.")
            time.sleep(1)
            budget = int(input("Firstly I need to know your budget? (No commas or full stops)"))
            time.sleep(0.5)
            Gearbox = input("What is your prefered gearbox type? ").upper()
            time.sleep(0.5)
            Use = input("Next up what is the intended use: commuting, family use, performance, offroading, or mixed? ").upper()
            time.sleep(0.5)
            Fuel = input("What do you want your car to use? AKA petrol, diesel, hybrid, electric or NA.").upper()
            time.sleep(0.5)
            Colour = input("Do you have a colour in mind? (If not then just put no)")
            time.sleep(0.5)
            print("Thank you, let me just get that list for you now.")
            exit()
            
        else:
            print("Sorry, please try again")
            time.sleep(5)
            goto(1)