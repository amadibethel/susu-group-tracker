
import unittest
from decimal import Decimal

from src.susu import SusuGroup


class TestSusuGroup(unittest.TestCase):
    def setUp(self):
        self.group = SusuGroup("50.00")
        self.group.add_member("Ama")
        self.group.add_member("Kofi")
        self.group.add_member("Esi")

    def test_group_accepts_valid_contribution(self):
        self.assertEqual(
            self.group.weekly_contribution, Decimal("50.00")
        )

    def test_duplicate_members_are_rejected_case_insensitively(self):
        with self.assertRaises(ValueError):
            self.group.add_member("ama")

    def test_unknown_member_is_rejected(self):
        with self.assertRaises(ValueError):
            self.group.record_contribution("Yaw", "10.00")

    def test_zero_and_negative_payments_are_rejected(self):
        for amount in ("0", "-5.00"):
            with self.subTest(amount=amount):
                with self.assertRaises(ValueError):
                    self.group.record_contribution("Ama", amount)

    def test_partial_payments_accumulate(self):
        self.group.record_contribution("Esi", "30.00")
        remaining = self.group.record_contribution("Esi", "20.00")

        self.assertEqual(remaining, Decimal("0.00"))
        self.assertTrue(
            self.group.report()["members"]["Esi"]["paid_in_full"]
        )

    def test_overpayment_is_rejected(self):
        self.group.record_contribution("Ama", "40.00")

        with self.assertRaises(ValueError):
            self.group.record_contribution("Ama", "10.01")

        self.assertEqual(
            self.group.report()["members"]["Ama"]["paid"],
            Decimal("40.00"),
        )

    def test_week_cannot_close_with_outstanding_balance(self):
        self.group.record_contribution("Ama", "50.00")
        self.group.record_contribution("Kofi", "50.00")
        self.group.record_contribution("Esi", "30.00")

        result = self.group.close_week()

        self.assertFalse(result["closed"])
        self.assertIsNone(result["payout"])
        self.assertEqual(
            result["outstanding"]["Esi"], Decimal("20.00")
        )
        self.assertEqual(self.group.current_week, 1)
        self.assertEqual(self.group.payout_history, [])

    def test_fully_paid_week_pays_correct_pot(self):
        for member in self.group.members:
            self.group.record_contribution(member, "50.00")

        result = self.group.close_week()

        self.assertTrue(result["closed"])
        self.assertEqual(result["payout"]["recipient"], "Ama")
        self.assertEqual(
            result["payout"]["amount"], Decimal("150.00")
        )

    def test_next_week_rotates_to_next_member(self):
        for member in self.group.members:
            self.group.record_contribution(member, "50.00")

        self.group.close_week()
        self.group.start_next_week()

        self.assertEqual(self.group.current_week, 2)
        self.assertEqual(self.group.report()["next_recipient"], "Kofi")

    def test_payout_history_is_preserved(self):
        for member in self.group.members:
            self.group.record_contribution(member, "50.00")

        self.group.close_week()

        self.assertEqual(len(self.group.payout_history), 1)
        self.assertEqual(
            self.group.payout_history[0]["recipient"], "Ama"
        )

    def test_money_with_more_than_two_decimal_places_is_rejected(self):
        with self.assertRaises(ValueError):
            SusuGroup("50.001")

    def test_member_cannot_be_added_after_group_starts(self):
        self.group.record_contribution("Ama", "10.00")

        with self.assertRaises(ValueError):
            self.group.add_member("Yaw")


if __name__ == "__main__":
    unittest.main()
