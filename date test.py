import time
from datetime import datetime
from datetime import date
today = date.today()

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
                cautious_1 = input("Are you sure you put the correct number? ").upper()
                if cautious_1 == "YES":
                    print("Sorry but we don't offer", warranty_value, "years.")
                elif cautious_1 == "NO":
                    print("No worries, please go back")
            elif warranty_value <= 5:
                print("Thank you")
            return warranty_value

        except ValueError:
            print("Please put the number of year/years as a number.")
            
            
purchase_date = ask_warranty_purchase("When was the warranty purchased? (DD/MM/YYYY)")
warranty_value = ask_warranty_years("How many years did you purchase the warranty for? ")

    
