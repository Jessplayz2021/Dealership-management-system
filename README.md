# Dealership Management System

A command-line front-desk assistant for a car dealership. It greets a customer,
works out why they've come in, and walks them through the right set of
questions — sales, warranty, repair, or browsing the stock.

Early stage: the conversation flow is built and validated, but there's no
inventory database behind it yet.

## Requirements

Python 3.8 or newer. No third-party packages.

## Running it

```bash
python dealership.py
```

## What it does

The main menu offers four paths:

| Option | Screen | What happens |
| --- | --- | --- |
| 1 | Car sales | Takes a car or lot number to look up |
| 2 | Repairs/Warranty | Branches to a warranty check or repair triage |
| 3 | Just browsing | Collects budget, gearbox, use case, fuel and colour |
| 4 | Exit | Ends the session |

**Warranty check** takes the purchase date and compares it against a
three-year term (`WARRANTY_TERM_YEARS` at the top of the file), reporting how
many days are left or how long ago it lapsed.

**Repair triage** asks the four first-line diagnostic questions — does it
start, any unusual noise, does it pull to one side, does it feel rough — plus
roughly what the customer paid, so the job can be sized before a technician
looks at it.

Every completed interaction is collected into a `session` list returned by
`main()`, ready to be written somewhere once storage exists.

## How it's structured

Each screen is a function that returns when it's done, which drops the customer
back at the main menu. `main()` holds the only loop; a dictionary maps the menu
choice to the screen that handles it, so adding a fifth option means writing one
function and adding one dictionary entry.

Input is gathered through four helpers, all of which re-ask rather than crash on
a bad answer:

- `ask_int` — strips commas and currency symbols, rejects anything non-numeric
- `ask_yes_no` — accepts yes/y/no/n in any case
- `ask_choice` — matches against a dictionary of accepted answers, so several
  spellings ("auto" and "automatic") can map to one value
- `ask_past_date` — parses `DD/MM/YYYY` and rejects dates in the future

`add_years` handles the 29 February case, where advancing the year would
otherwise land on a date that doesn't exist.

## Still to do

- Inventory database, so sales lookups and browsing filters return real cars
  (the two `TODO` markers in the file mark where it plugs in)
- Persist the session records instead of dropping them on exit
- Customer and job records, so a repair can be tracked after triage
- Tests around the warranty date maths

## Notes

The deliberate `time.sleep` pauses are there to make the assistant feel like it's
thinking rather than dumping every prompt at once. The five-second wait during
the warranty check is the longest one if it ever starts to grate.****
