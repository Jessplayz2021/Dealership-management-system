import time
from datetime import datetime, date

WARRANTY_YEARS = 3


def ask_int(prompt):
    while True:
        try:
            return int(input(prompt).replace(",", "").strip())
        except ValueError:
            print("Numbers only, please.")


def ask_date(prompt):
    while True:
        try:
            return datetime.strptime(input(prompt).strip(), "%d/%m/%Y").date()
        except ValueError:
            print("Please use DD/MM/YYYY, for example 14/03/2023.")


def sales():
    car_or_lot = input("Okay, What car or lot number do you wish for? ")
    return {"car_or_lot": car_or_lot}  # I need to create a data base for this


def service():
    while True:
        warranty_or_repair = input(
            "Are you in for Warranty or Repair? (If you need to go back just say return). "
        ).upper()

        if warranty_or_repair == "WARRANTY":
            print("Okay, I'm just going to get a few details. Please read these questions carefully.")
            time.sleep(1)
            purchased = ask_date("What date (DD/MM/YYYY) did you purchase the warranty? ")
            time.sleep(1)
            print("Thank you, let me just check if your warranty is valid.")
            time.sleep(5)
            try:
                expiry = purchased.replace(year=purchased.year + WARRANTY_YEARS)
            except ValueError:
                # 29 February landing on a non-leap year
                expiry = purchased.replace(year=purchased.year + WARRANTY_YEARS, day=28)
            valid = date.today() <= expiry
            if valid:
                print(f"Your warranty is valid until {expiry.strftime('%d/%m/%Y')}.")
            else:
                print(f"I'm sorry, that warranty expired on {expiry.strftime('%d/%m/%Y')}.")
            return {"purchased": purchased, "expiry": expiry, "valid": valid}

        elif warranty_or_repair == "REPAIR":
            print("I'm sorry for the issue, let me get it resolved for you as best I can!")
            time.sleep(2)
            print("I'm going to need a few details describing the issue.")
            time.sleep(2)
            car_value = ask_int("Roughly how much did you pay for the vehicle? ")
            time.sleep(1)
            print("Please answer these following questions via Yes/No")
            time.sleep(1)
            car_starts = input("Does the car start? ").upper()
            time.sleep(0.2)
            sound_of_issue = input("Is there any sound coming from this issue? ").upper()
            time.sleep(0.2)
            alignment = input("Does the vehicle pull to one side? ").upper()
            time.sleep(0.2)
            smoothness = input("Does the vehicle feel rough when driving? ").upper()
            print("Thank you, you may sit down and I will call you up when we know the issue.")
            return {  # this bit will rely on future code
                "car_value": car_value,
                "car_starts": car_starts,
                "sound_of_issue": sound_of_issue,
                "alignment": alignment,
                "smoothness": smoothness,
            }

        elif warranty_or_repair == "RETURN":
            time.sleep(1)
            return None

        else:
            print("Please pick a listed option.")
            time.sleep(1)


def browsing():
    print("Okay... Here's a few questions I'd like to ask to narrow down your choices.")
    time.sleep(1)
    budget = ask_int("Firstly I need to know your budget? (No commas or full stops). ")
    time.sleep(0.5)
    gearbox = input("What is your preferred gearbox type? ").upper()
    time.sleep(0.5)
    intended_use = input(
        "Next up what is the intended use: commuting, family use, performance, offroading, or mixed? "
    ).upper()
    time.sleep(0.5)
    fuel = input("What do you want your car to use? AKA petrol, diesel, hybrid, electric or NA. ").upper()
    time.sleep(0.5)
    colour = input("Do you have a colour in mind? (If not then just put no) ")
    time.sleep(0.5)
    print("Thank you, let me just get that list for you now. ")
    return {  # again needs data base to continue
        "budget": budget,
        "gearbox": gearbox,
        "intended_use": intended_use,
        "fuel": fuel,
        "colour": colour,
    }


def main():
    screens = {"1": sales, "2": service, "3": browsing}
    while True:
        print("Hello there, welcome to our dealership!")
        time.sleep(2)
        print("1 Car sales")
        print("2 Repairs/Warranty")
        print("3 Just browsing")
        screen = screens.get(input("From our options, What would you like to pick? ").strip())
        if screen is None:
            print("Sorry, please try again")
            time.sleep(5)
            continue
        screen()  # returning drops you back to the menu


if __name__ == "__main__":
    main()
