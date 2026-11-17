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
test = ask_price("How much is it? ")
print(test)