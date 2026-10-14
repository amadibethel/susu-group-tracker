# Design Notes and Assumptions

## Assumptions

1. Members can be added only before the first contribution is recorded.
2. Member names are unique, ignoring case and surrounding whitespace.
3. Every member owes the same fixed contribution each week.
4. Partial payments accumulate toward the weekly contribution.
5. Payments that are zero, negative, or greater than the outstanding balance are rejected.
6. Monetary values must be finite and have no more than two decimal places.
7. An incomplete week cannot close. No payout is recorded, and the week remains open.
8. Successful payouts follow member join order. After every member has received a payout, the order repeats.
9. The next week begins explicitly after a successful week closure.
10. A group must contain at least one member to close a week.
11. Data is held in memory and is lost when the application exits.

## Design decisions

- Python's `Decimal` is used instead of floating-point arithmetic for monetary calculations.
- `SusuGroup` encapsulates the business rules and group state.
- The command-line interface delegates business operations to the core class.
- Python's built-in `unittest` framework provides automated regression tests.
- Failed operations raise `ValueError` with explanatory messages.

## Improvements with more time

- Persist group, contribution, and payout data in SQLite or PostgreSQL.
- Add immutable transaction records and audit logging.
- Introduce stable member IDs and support multiple groups.
- Add stronger validation of group lifecycle and concurrent transactions.
- Support reconciliation and recovery after application restarts.
- Expand testing with property-based tests and additional edge cases.

## Limitations

This is an educational command-line application, not a production financial platform. It does not implement authentication, durable storage, payment integrations, or concurrent transaction handling.