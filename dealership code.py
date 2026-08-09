import time
from datetime import datetime
from datetime import date

today = date.today()

def ask_yes_or_no(prompt):
    while True:
        answer = input(prompt).strip().upper()
        if answer in ("YES", "Y", "YEA", "YEAH"):
            return True
        elif answer in ("NO", "N", "NAH"):
            return False
        else:
            print("Please answer Yes or No.")

def ask_warranty_purchase(prompt):
    while True:
        try:
            value = input(prompt)
            purchase_date = datetime.strptime(value, "%d/%m/%Y").date()
            if purchase_date > today:
                print("Sorry, but the purchase date cant be in the future")
                continue
            return purchase_date
        except ValueError:
            print("Just do as it says")
def ask_warranty_years(prompt):
    while True:
        try:
            warranty_value = int(input(prompt))
            if warranty_value > 5:
                if ask_yes_or_no("Are you sure you put the correct number of years? "):
                    print("Sorry but we don't offer", warranty_value, "years.")
                    exit()# I want this section to go to another section where it checks suitability
                else:
                    print("No worries, Please put the correct number of years.")
                    continue
                
            elif warranty_value < 1:
                print("We don't sell warranty for under a year.")
                continue
            elif warranty_value <= 5:
                print("Thank you")
                return warranty_value


        except ValueError:
            print("Please put the number of year/years as a number.")
def add_years_safe(purchase_date, years):
    try:
        return purchase_date.replace(
            year=purchase_date.year + years
        )
    except ValueError:
        return purchase_date.replace(
            year=purchase_date.year + years,
            day=28
        )
   

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

def main():
    while True:
        print("Hello there, welcome to our dealership!")
        time.sleep(2)
        print("1 Car sales")
        print("2 Repairs/Warranty")
        print("3 Just browsing")
        print("4 Exit")
        Option1=input("From our options, What would you like to pick? ").upper()
        
        if Option1 in ("1", "CAR SALES"):
            input("Okay, What car or lot number do you wish for? ")
            
            exit() #I need to create a data base for this
            
        elif Option1 in ("2", "REPAIRS/WARRANTY", "WARRANTY", "REPAIRS"):
            service()
            
        elif Option1 in ("3", "JUST BROWSING"):
            print("Okay... Here's a few questions I'd like to ask to narrow down your choices.")
            
            time.sleep(1)
            budget = ask_price("Firstly I need to know your budget? ")
            
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
        elif Option1 in ("4", "EXIT"):
            exit()
            
        else:
            print("Sorry, please try again")
            
            time.sleep(0.5)
            
            
def service():
    
    WarrantyOrRepair = input("Are you in for Warranty or Repair? (If you need to go back just say return or exit). ").upper()
    
    if WarrantyOrRepair == "WARRANTY":
        print("Okay, I'm just going to get a few details. Please read these questions carefully.")
        
        time.sleep(1)
        purchase_date = ask_warranty_purchase("When was the warranty purchased? (DD/MM/YYYY) ")
        
        time.sleep(1)
        warranty_value = ask_warranty_years("How many years did you purchase the warranty for? ")
        
        time.sleep(0.5)
        expiry_date = add_years_safe(purchase_date, warranty_value)
        expiry_date_true = expiry_date.strftime("%d/%m/%Y")
        
        if expiry_date < today:
            print("Sorry but your warranty is expired on", expiry_date)
            
        elif expiry_date == today:
            print("Your warranty expires today. Please apply for extended warranty or we will have to include a price.")
            
        else:
            
            if ask_yes_or_no("Would you like to know your expiry date? "):
                print("Your expiry date is", expiry_date)
                
            else:
                print("No worries, Let's continue.")
    elif WarrantyOrRepair == "REPAIR":
        print("I'm sorry for the issue, let me get it resolved for you as best I can!")
        
        time.sleep(2)
        print("I'm going to need a few details describing the issue.")
        
        time.sleep(2)
        CarValue = ask_price("How much did you pay for the vehicle? ")
        
        time.sleep(1)
        print("Please answer these following questions via. Yes/No")
        
        time.sleep(1)
        carstart = ask_yes_or_no("Does the car start? ")
        
        time.sleep(0.2)
        Soundsofissue = ask_yes_or_no("Is there any sound coming from this issue? ")
        
        time.sleep(0.2)
        Allignment = ask_yes_or_no("Does the vehicle pull to one side? ")
        
        time.sleep(0.2)
        smoothness = ask_yes_or_no("Does the vehicle feel rough when driving? ")
        
        time.sleep(0.2)
        print("Thank you, you may sit down and I will call you up when we know the issue.")
        
        exit()#this bit will rely on future code
        
    elif WarrantyOrRepair == "RETURN":
        time.sleep(1)
        
        return
    elif WarrantyOrRepair == "EXIT":
        print("Thank you for your time and have a good day.")
        exit()
    
    else:
        print("Please pick a listed option.")
        
        time.sleep(1)

if __name__ == "__main__":
    main()