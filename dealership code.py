import time
from datetime import date

today = date.today()
d1 = today.strftime("%d")
m1 = today.strftime("%m")
y1 = today.strftime("%Y")
D1=int(d1)
M1=int(m1)
Y1=int(y1)
def ask_price(prompt):
    while True:
        value = input(prompt).replace(",", "").replace("£", "").strip()

        if "." in value:
            try:
                pounds, pence = value.split(".")

                if len(pence) != 2:
                    print("Please enter exactly two digits after the decimal point.")
                    continue

                if not pounds.isdigit() or not pence.isdigit():
                    print("Numbers only, please.")
                    continue

                return float(value)

            except ValueError:
                print("Please enter a valid price.")
        else:
            try:
                return float(value)
            except ValueError:
                print("Numbers only, please.")

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
        Option1=input("From out options, What would you like to pick? ")
        if Option1 == "1":
            input("Okay, What car or lot number do you wish for? ")
            exit() #I need to create a data base for this
        elif Option1 == "2":
            goto(2)
    if line == 2:
        WarrantyOrRepair = input("Are you in for Warranty or Repair? (If you need to go back just say return). ").upper()
        if WarrantyOrRepair == "WARRANTY":
            print("Okay, I'm just going to get a few details. Please read these questions carefully.")
            time.sleep(1)
            DayOfwarrantyPurchased = int(input("What day (DD) did you purchase the warranty? "))
            time.sleep(0.5)
            MonthOfWarrantyPurchased = int(input("Which month (MM) was it purchased in? "))
            time.sleep(0.5)
            YearOfWarrantyPurchased = int(input("Now finally what year (YYYY) was it purchased in? "))
            time.sleep(1)
            print("Thank you, let me just check if your warranty is valid.")
            time.sleep(5)
            exit() #I need to create a date verification for this
        elif WarrantyOrRepair == "REPAIR":
            print("I'm sorry for the issue, let me get it resolved for you as best I can!")
            time.sleep(2)
            print("I'm going to need a few details describing the issue.")
            time.sleep(2)
            CarValue = ask_price("How much did you pay for the vehicle? ")
            time.sleep(1)
            print("Please answer these following questions via. Yes/No")
            time.sleep(1)
            carstart = input("Does the car start? ").upper()
            time.sleep(0.2)
            Soundsofissue = input("Is there any sound coming from this issue? ").upper()
            time.sleep(0.2)
            Allignment = input("Does the vehicle pull to one side? ").upper()
            time.sleep(0.2)
            smoothness = input("Does the vehicle feel rough when driving? ").upper()
            time.sleep(0.2)
            print("Thank you, you may sit down and I will call you up when we know the issue.")
            exit()#this bit will rely on future code
        elif WarrantyOrRepair == "RETURN":
            time.sleep(1)
            goto(1)
        else:
            print("Please pick a listed option.")
            time.sleep(1)
            goto(2) 
    elif Option1 == "3":
        print("Okay... Here's a few questions I'd like to ask to narrow down your choices.")
        time.sleep(1)
        budget = int(input("Firstly I need to know your budget? (No commas or full stops). "))
        time.sleep(0.5)
        Gearbox = input("What is your prefered gearbox type? ").upper()
        time.sleep(0.5)
        Use = input("Next up what is the intended use: commuting, family use, performance, offroading, or mixed? ").upper()
        time.sleep(0.5)
        Fuel = input("What do you want your car to use? AKA petrol, diesel, hybrid, electric or NA. ").upper()
        time.sleep(0.5)
        Colour = input("Do you have a colour in mind? (If not then just put no). ").upper()
        time.sleep(0.5)
        print("Thank you, let me just get that list for you now. ")
        exit() #again needs data base to continue
            
    else:
        print("Sorry, please try again")
        time.sleep(5)
        goto(1)#fail safe