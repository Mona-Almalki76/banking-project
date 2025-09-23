import unittest
from classes.bank import Bank

class TestBank(unittest.TestCase):
    def setUp(self):
        self.bank = Bank()

    def test_add_customer_auto_id(self):
        c1 = self.bank.add_customer("Mona", "Almalki", "pass123")
        self.assertEqual(c1.account_id, "10001")
        self.assertEqual(c1.frst_name, "Mona")
        self.assertEqual(c1.last_name, "Almalki")
        self.assertEqual(c1.balance_checking, 0.0)
        self.assertEqual(c1.balance_savings, 0.0)

    def test_auto_increment_id(self):
        c1 = self.bank.add_customer("Mona", "Almalki", "pass123")
        c2 = self.bank.add_customer("Sara", "Ali", "pass123")
        self.assertEqual(c2.account_id, "10002")

    def test_add_customer_given_id(self):
        c2 = self.bank.add_customer("Ali", "Khalid", "pass123", given_id="20001")
        self.assertEqual(c2.account_id, "20001")

    def test_add_customer_checking_only(self):
        c3 = self.bank.add_customer("Sara", "Ali", "pass123", create_checking=True, create_savings=False)
        self.assertEqual(c3.balance_checking, 0.0)
        self.assertIsNone(c3.balance_savings)

    def test_add_customer_savings_only(self):
        c4 = self.bank.add_customer("Maya", "Ryan", "pass123", create_checking=False, create_savings=True)
        self.assertIsNone(c4.balance_checking)
        self.assertEqual(c4.balance_savings, 0.0)

if __name__ == "__main__":
    unittest.main()