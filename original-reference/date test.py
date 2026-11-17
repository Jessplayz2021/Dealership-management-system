import time
from datetime import datetime
from datetime import date
today = date.today()
def ask_yes_or_no(prompt):
    while True:
        answer = input(prompt).strip().upper()
        if answer == "YES":
            return True
        elif answer == "NO":
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
   
purchase_date = ask_warranty_purchase("When was the warranty purchased? (DD/MM/YYYY) ")
warranty_value = ask_warranty_years("How many years did you purchase the warranty for? ")
expiry_date = add_years_safe(purchase_date, warranty_value)
if expiry_date < today:
    print("Sorry but your warranty is expired on", expiry_date)
elif expiry_date == today:
    print("Your warranty expires today. Please apply for extended warranty or we may have to include a price.")
else:
    if ask_yes_or_no("Would you like to know your expiry date? "):
        print("Your expiry date is", expiry_date)
    else:
        print("No worries, Let's continue.")
