"""JS Spec Dealership — terminal edition. Run: python main.py"""
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
import argparse
import sqlite3
import database as store

BANNER = '''
╔══════════════════════════════════════════════╗
║        JS SPEC  /  DEALERSHIP SYSTEM         ║
║        Front grip. Rear problems.            ║
║        Financial records: hopefully stable.  ║
╚══════════════════════════════════════════════╝'''

def money(pence):
    return f'£{pence / 100:,.2f}'

def ask_yes_or_no(prompt):
    while True:
        answer = input(prompt + ' (yes/no): ').strip().lower()
        if answer in ('yes','y','yea','yeah'): return True
        if answer in ('no','n','nah'): return False
        print('Please answer yes or no.')

def parse_money(value):
    """Convert pounds to integer pence without floating-point rounding errors."""
    raw = value.replace('£', '').replace(',', '').strip()
    try:
        amount = Decimal(raw)
    except InvalidOperation:
        raise ValueError('Please enter a valid amount, such as 12500 or 12500.50.')
    if not amount.is_finite() or amount <= 0 or amount.as_tuple().exponent < -2:
        raise ValueError('Price must be positive and have at most two decimal places.')
    return int(amount * 100)

def ask_price(prompt, allow_skip=False):
    while True:
        value = input(prompt).strip()
        if allow_skip and value.lower() in ('return','exit','back'):
            return None
        try:
            result = parse_money(value)
            if ask_yes_or_no(f'Confirm {money(result)}?'):
                return result
        except ValueError as e:
            print(e)

def ask_date(prompt):
    while True:
        value = input(prompt).strip()
        try:
            purchased = datetime.strptime(value, '%d/%m/%Y').date()
            if purchased > date.today():
                print('The purchase date cannot be in the future.')
                continue
            return purchased
        except ValueError:
            print('Please enter a real date in DD/MM/YYYY format.')

def add_years_safe(original, years):
    try:
        return original.replace(year=original.year + years)
    except ValueError:
        return original.replace(year=original.year + years, day=28)

def warranty():
    bought = ask_date('When was the warranty purchased? (DD/MM/YYYY) ')
    while True:
        try:
            years = int(input('How many warranty years (1–5)? '))
        except ValueError:
            print('Please enter a whole number.')
            continue
        if 1 <= years <= 5: break
        print('We offer warranties from one to five years. Please try again.')
    expiry = add_years_safe(bought, years)
    if expiry < date.today():
        print(f'Sorry, your warranty expired on {expiry:%d/%m/%Y}.')
    elif expiry == date.today():
        print('Your warranty expires today. Extended coverage may be available.')
    else:
        print('Your warranty is currently valid.')
        if ask_yes_or_no('Would you like to know the expiry date?'):
            print(f'Your expiry date is {expiry:%d/%m/%Y}.')
    print('Coverage dates alone do not confirm the repair is covered.')

def repair(db_path):
    print('We will forward the answers to the workshop. No random fault generator here. XD')
    price = ask_price('How much did you pay for the vehicle? (or back) ', allow_skip=True)
    if price is None: return
    answers = (
        ask_yes_or_no('Does the car start?'),
        ask_yes_or_no('Is there any sound from the issue?'),
        ask_yes_or_no('Does the vehicle pull to one side?'),
        ask_yes_or_no('Does it feel rough when driving?'),
    )
    ticket = store.record_repair(price, *answers, path=db_path)
    print(f'Repair request #{ticket} recorded. The workshop will investigate and get back to you.')

def service(db_path):
    while True:
        option = input('\nWarranty / Repair / Return: ').strip().lower()
        if option == 'warranty': warranty()
        elif option == 'repair': repair(db_path)
        elif option in ('return','back','exit'): return
        else: print('Please choose a listed option.')

def show_car(car):
    print(f"[{car['lot_number']}] {car['year']} {car['make']} {car['model']} | {car['mileage']:,} miles")
    print(f"  {car['fuel']} · {car['gearbox']} · {car['colour']} · {car['intended_use']} | {money(car['price_pence'])} | {car['status']}")
    if car.get('engine_size') or car.get('drivetrain'):
        print(f"  Engine: {car.get('engine_size') or 'N/A'} · Drivetrain: {car.get('drivetrain') or 'N/A'}")

def car_sales(db_path):
    term = input('Which car or lot number? (blank to show stock) ').strip()
    matches = store.find_vehicles(term, path=db_path)
    if not matches:
        print('No matching vehicles in stock. Try another search.')
        return
    for car in matches: show_car(car)
    if not ask_yes_or_no('Would you like to purchase a vehicle?'):
        return
    if len(matches) == 1:
        lot = matches[0]['lot_number']
    else:
        lot = input('Enter the exact lot number: ').strip()
    car = store.get_vehicle(lot, path=db_path)
    if car is None:
        print('Lot number not found.')
        return
    if len(matches) > 1:
        show_car(car)
    if car['status'] != 'Available':
        print('This vehicle cannot currently be purchased.')
        return
    if not ask_yes_or_no('Confirm purchase of this vehicle?'):
        print('Purchase cancelled — nothing has been changed.')
        return
    name = input('Customer name (for the dealership record): ').strip()
    try:
        sale_id = store.sell_vehicle(lot, name, path=db_path)
        print(f'Sale #{sale_id} completed. {lot} is now marked Sold. Yes officer, it was stock. XD')
    except ValueError as exc:
        print('Unable to complete sale:', exc)

def browse(db_path):
    print('Answer a few questions. Press Enter to skip any preference except the budget.')
    budget = ask_price('Maximum budget in £ (or back): ', allow_skip=True)
    if budget is None: return
    filters = {'max_price_pence': budget}
    for key, question in (
        ('gearbox','Gearbox (manual/automatic): '),
        ('intended_use','Use (commuting/family/performance/offroading/mixed): '),
        ('fuel','Fuel (petrol/diesel/hybrid/electric): '),
        ('colour','Colour: '),
    ):
        value = input(question).strip()
        if value.lower() not in ('', 'no', 'na', 'n/a', 'any'):
            filters[key] = value
    matches = store.find_vehicles(path=db_path, available_only=True, filters=filters)
    if not matches:
        print('No exact matches this time. Try widening your preferences.')
        return
    print(f'Found {len(matches)} matching vehicle(s):')
    for car in matches: show_car(car)

def admin(db_path):
    while True:
        print('\n--- Staff tools (local demo; not access-controlled) ---')
        print('1 Add vehicle | 2 Sales report | 3 Workshop queue | 4 Back')
        option = input('Select: ').strip()
        if option == '4': return
        if option == '1':
            data = {}
            for key in ('lot_number','make','model','fuel','gearbox','colour','intended_use'):
                while not (data.get(key) or '').strip():
                    data[key] = input(f'{key.replace("_", " ").title()}: ').strip()
            for key, minimum, maximum in [('year',1886,date.today().year+1),('mileage',0,10_000_000)]:
                while True:
                    try:
                        number = int(input(f'{key.title()}: '))
                        if not minimum <= number <= maximum: raise ValueError
                        data[key] = number
                        break
                    except ValueError:
                        print(f'Enter a whole number between {minimum} and {maximum}.')
            data['engine_size'] = input('Engine size (optional): ').strip() or None
            data['drivetrain'] = input('Drivetrain (optional): ').strip() or None
            data['price_pence'] = ask_price('Asking price in £: ')
            try:
                store.add_vehicle(data, path=db_path)
                print('Vehicle added. No registration plate required. XD')
            except sqlite3.IntegrityError as exc:
                print('Could not add vehicle (possibly duplicate lot number):', exc)
        elif option == '2':
            stats, rows = store.sales_summary(db_path)
            print(f"Completed sales: {stats['sales']} | Total revenue: {money(stats['revenue_pence'])}")
            for row in rows:
                print(f"  #{row['id']}: {row['lot_number']} {row['make']} {row['model']} — {money(row['sale_price_pence'])} — {row['customer_name']} ({row['sold_at']})")
        elif option == '3':
            for item in store.repair_summary(db_path):
                print(f"  #{item['id']}: {item['created_at']} | {item['status']} | Starts: {bool(item['starts'])} | Noise: {bool(item['makes_noise'])} | Pulls: {bool(item['pulls_to_side'])} | Rough: {bool(item['drives_rough'])}")
        else:
            print('Pick a listed option.')

def main(db_path=store.DEFAULT_DB):
    store.setup_database(db_path)
    print(BANNER)
    while True:
        print('\n1 Car sales | 2 Repairs/Warranty | 3 Just browsing | 4 Staff tools | 5 Exit')
        choice = input('Where to, chief? ').strip().lower()
        if choice in ('1','car sales'): car_sales(db_path)
        elif choice in ('2','repairs','warranty','repairs/warranty'): service(db_path)
        elif choice in ('3','just browsing','browse'): browse(db_path)
        elif choice in ('4','staff','staff tools'): admin(db_path)
        elif choice in ('5','exit','quit'):
            print('Thanks for visiting JS Spec. Try not to tree anything on the way out. XD')
            return
        else: print('Sorry, please pick a listed option.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='JS Spec Dealership')
    parser.add_argument('--db', type=Path, default=store.DEFAULT_DB, help='Path to SQLite database')
    args = parser.parse_args()
    try:
        main(args.db)
    except (KeyboardInterrupt, EOFError):
        print('\nDealership closed safely.')
