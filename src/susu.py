
from decimal import Decimal, InvalidOperation
from typing import Any


def parse_money(value: Any) -> Decimal:
    """Validate and convert a positive monetary amount."""
    if isinstance(value, (bool, float)):
        raise ValueError("Use a string, integer, or Decimal for money.")

    try:
        amount = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError("Invalid monetary amount.") from None

    if not amount.is_finite():
        raise ValueError("Amount must be finite.")

    if amount <= Decimal("0"):
        raise ValueError("Amount must be greater than zero.")

    if amount.as_tuple().exponent < -2:
        raise ValueError("Maximum precision is two decimal places.")

    return amount.quantize(Decimal("0.01"))


class SusuGroup:
    """Manage members, weekly contributions, and rotating payouts."""

    def __init__(self, weekly_contribution: Any):
        self.weekly_contribution = parse_money(weekly_contribution)
        self.members: list[str] = []
        self._member_keys: set[str] = set()
        self.current_week = 1
        self._contributions: dict[str, Decimal] = {}
        self.payout_history: list[dict[str, Any]] = []
        self._closed = False

    @staticmethod
    def _normalize_name(name: str) -> str:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Member name must not be empty.")
        return name.strip().casefold()

    def _find_member(self, name: str) -> str:
        key = self._normalize_name(name)
        for member in self.members:
            if member.casefold() == key:
                return member
        raise ValueError(f"Unknown member: {name}")

    def add_member(self, name: str) -> None:
        """Add members before any contribution has been recorded."""
        key = self._normalize_name(name)

        if self._closed or self.payout_history or any(
            amount > Decimal("0.00")
            for amount in self._contributions.values()
        ):
            raise ValueError(
                "Members cannot be added after contributions begin."
            )

        if key in self._member_keys:
            raise ValueError(f"Duplicate member: {name}")

        member = name.strip()
        self.members.append(member)
        self._member_keys.add(key)
        self._contributions[key] = Decimal("0.00")

    def record_contribution(
        self, member_name: str, amount: Any
    ) -> Decimal:
        """Record a contribution and return the outstanding balance."""
        if self._closed:
            raise ValueError("The current week is already closed.")

        member = self._find_member(member_name)
        payment = parse_money(amount)
        key = member.casefold()

        paid = self._contributions[key]
        owed = self.weekly_contribution - paid

        if payment > owed:
            raise ValueError(
                f"{member} owes {owed:.2f}; "
                f"payment of {payment:.2f} exceeds the balance."
            )

        self._contributions[key] += payment
        return self.weekly_contribution - self._contributions[key]

    def close_week(self) -> dict[str, Any]:
        """Pay the next member only when every member has paid in full."""
        if self._closed:
            raise ValueError("The current week is already closed.")

        if not self.members:
            raise ValueError("Add at least one member before closing.")

        outstanding = {
            member: self.weekly_contribution
            - self._contributions[member.casefold()]
            for member in self.members
            if self._contributions[member.casefold()]
            < self.weekly_contribution
        }

        if outstanding:
            return {
                "closed": False,
                "week": self.current_week,
                "payout": None,
                "outstanding": outstanding,
            }

        recipient_index = len(self.payout_history) % len(self.members)
        recipient = self.members[recipient_index]
        pot = self.weekly_contribution * len(self.members)

        payout = {
            "week": self.current_week,
            "recipient": recipient,
            "amount": pot,
        }
        self.payout_history.append(payout)
        self._closed = True

        return {
            "closed": True,
            "week": self.current_week,
            "payout": payout,
            "outstanding": {},
        }

    def start_next_week(self) -> None:
        """Start a new week after a successful payout."""
        if not self._closed:
            raise ValueError(
                "Close the current week successfully before advancing."
            )

        self.current_week += 1
        self._contributions = {
            member.casefold(): Decimal("0.00")
            for member in self.members
        }
        self._closed = False

    def report(self) -> dict[str, Any]:
        """Return current balances, next recipient, and payout history."""
        balances = {}

        for member in self.members:
            paid = self._contributions[member.casefold()]
            owed = self.weekly_contribution - paid
            balances[member] = {
                "paid": paid,
                "owed": owed,
                "paid_in_full": owed == Decimal("0.00"),
            }

        next_recipient = (
            self.members[len(self.payout_history) % len(self.members)]
            if self.members
            else None
        )

        return {
            "current_week": self.current_week,
            "week_closed": self._closed,
            "weekly_contribution": self.weekly_contribution,
            "members": balances,
            "next_recipient": next_recipient,
            "payout_history": list(self.payout_history),
        }
