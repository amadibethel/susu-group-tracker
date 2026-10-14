
from decimal import Decimal
from src.susu import SusuGroup


def display_report(group: SusuGroup) -> None:
    report = group.report()

    print(f"\n--- Week {report['current_week']} Report ---")
    print(f"Weekly contribution: GHS {report['weekly_contribution']:.2f}")
    print(f"Week closed: {'Yes' if report['week_closed'] else 'No'}")

    for name, details in report["members"].items():
        status = "Paid in full" if details["paid_in_full"] else "Outstanding"
        print(
            f"{name}: paid GHS {details['paid']:.2f}, "
            f"owes GHS {details['owed']:.2f} ({status})"
        )

    print(f"Next payout recipient: {report['next_recipient']}")

    print("\nPayout history:")
    if not report["payout_history"]:
        print("No payouts recorded.")
    else:
        for payout in report["payout_history"]:
            print(
                f"Week {payout['week']}: {payout['recipient']} "
                f"received GHS {payout['amount']:.2f}"
            )


def main() -> None:
    print("=== Susu Group Tracker ===")

    try:
        amount = input("Enter the weekly contribution in GHS: ").strip()
        group = SusuGroup(amount)

        while True:
            print(
                "\n1. Add member\n"
                "2. Record contribution\n"
                "3. Close week\n"
                "4. Start next week\n"
                "5. View report\n"
                "0. Exit"
            )

            choice = input("Choose an option: ").strip()

            try:
                if choice == "1":
                    name = input("Member name: ")
                    group.add_member(name)
                    print(f"Added {name.strip()}.")

                elif choice == "2":
                    name = input("Member name: ")
                    amount = input("Contribution amount in GHS: ")
                    remaining = group.record_contribution(name, amount)
                    print(f"Outstanding balance: GHS {remaining:.2f}")

                elif choice == "3":
                    result = group.close_week()

                    if result["closed"]:
                        payout = result["payout"]
                        print(
                            f"Week {payout['week']} closed successfully. "
                            f"{payout['recipient']} receives "
                            f"GHS {payout['amount']:.2f}."
                        )
                    else:
                        print("Week cannot close. Outstanding balances:")
                        for name, owed in result["outstanding"].items():
                            print(f"{name}: GHS {owed:.2f}")

                elif choice == "4":
                    group.start_next_week()
                    print(f"Week {group.current_week} started.")

                elif choice == "5":
                    display_report(group)

                elif choice == "0":
                    print("Goodbye!")
                    break

                else:
                    print("Invalid option. Choose 0–5.")

            except ValueError as error:
                print(f"Error: {error}")

    except ValueError as error:
        print(f"Unable to create group: {error}")


if __name__ == "__main__":
    main()
