# JS Spec Dealership — v2

An updated, terminal-based dealership simulator based on Jess's original Python program. Built with Python's standard library only; no pip packages required.

## Run

Install Python 3.10+ and open a terminal in this folder:

```bash
python main.py
```

On Windows you can also use `py main.py`. On Fedora use `python3 main.py`.

**Your old database is not included.** Running the program creates a fresh `dealership.db` next to the code. It starts empty: select **Staff tools → Add vehicle** to create your first listing. You can add any car or even a Scania if you're so inclined.

If you already have a populated `dealership.db` made by the original program, **back it up first**. This version retains the original `vehicles` table layout and creates two additional tables for completed sales and workshop tickets, but isn't a migration utility for every possible older schema. To test safely, run it with a separate database path: `python main.py --db test_dealership.db`.

## Features

- Find vehicles by lot number, make or model (case-insensitive)
- Search available stock by maximum price, fuel, gearbox, colour and intended use
- Complete purchases with confirmation, track sale history and automatically mark cars Sold
- Add vehicles through a staff menu; retains original fields and **no registration plates**
- Log repair answers as workshop tickets without generating fake mechanical diagnoses
- Calculate warranty dates, including leap-day purchases
- Store prices as integer pence, preventing floating-point currency errors
- Parameterised SQLite statements and atomic sales

## Layout

- `main.py`: customer and staff menus, input validation, and warranty functions
- `database.py`: persistence, searches, sales, workshop records
- `tests/`: automated regression tests
- `dealership.db`: created on first run (not included)

Run tests:

```bash
python -m unittest discover -s tests -v
```

## Limitations / future improvements

**Staff tools are deliberately not protected by authentication.** This release is suitable for a local demonstration, not a publicly hosted multi-user dealership. Customer names are stored in the local SQLite database; avoid using real personal information when sharing the project.

Potential next steps: vehicle reservation/cancellation, editable stock, detailed workshop workflows, customer receipt printing, a web/GUI front end, and role-based login for staff.

## AI development disclosure

Original project: Jess. V2 refactor and extensions: AI-assisted. The original `date test.py` and `test for value error.py` were treated as exploratory prototypes rather than shipped as executable application modules.
