# Susu Group Tracker

A Python command-line application for managing a rotating savings group (susu). Members contribute a fixed amount each week, and the entire pot is paid to the next member in join order only when all contributions are complete.

## Features

- Create a group with a fixed weekly contribution in GHS.
- Add members with unique names.
- Record full or partial contributions.
- Track outstanding balances.
- Prevent incomplete weeks from closing.
- Rotate payouts in member join order.
- View current balances and payout history.
- Handle money using Python's `Decimal` for exact arithmetic.

## Requirements

- Python 3.10 or later.
- No external dependencies.

## Run the application

Clone the repository and navigate to its root directory. Then run:

```bash
python -m src.main
```

Follow the interactive menu to add members, record contributions, close weeks, and view reports.

## Run the automated tests

From the project root, execute:

```bash
python -m unittest discover -s tests -v
```

## Example

For three members contributing GHS 50.00 each, the expected weekly pot is GHS 150.00. If one member has paid only GHS 30.00, the week cannot close until the outstanding GHS 20.00 is paid.

## Design

The core business logic is separated from the command-line interface. Automated tests cover validation, partial payments, incomplete week closures, payouts, and member rotation.