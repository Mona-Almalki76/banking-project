import unittest
from classes.bank import Bank

class TestTransfer(unittest.TestCase):
    def setUp(self):
        self.bank = Bank()
        self.c1 = self.bank.add_customer("Mona", "Almalki", "pass123")
        self.c1.balance_checking = 500
        self.c1.balance_savings = 300

        self.c2 = self.bank.add_customer("Sara", "Ali", "word321")
        self.c2.balance_checking = 200
        self.c2.balance_savings = 100

        self.bank.login(self.c1.account_id, "pass123")

    def test_transfer_savings_to_checking(self):
        txn = self.bank.transfer(100, "savings", "checking")
        self.assertEqual(self.c1.balance_savings, 200)
        self.assertEqual(self.c1.balance_checking, 600)
        self.assertEqual(txn.status, "SUCCESS")

    def test_transfer_checking_to_savings(self):
        txn = self.bank.transfer(200, "checking", "savings")
        self.assertEqual(self.c1.balance_checking, 300)
        self.assertEqual(self.c1.balance_savings, 500)
        self.assertEqual(txn.status, "SUCCESS")

    def test_transfer_insufficient_funds(self):
        with self.assertRaises(ValueError):
            self.bank.transfer(1000, "checking", "savings")

    def test_transfer_to_another_customer(self):
        txn = self.bank.transfer(100, "checking", "checking", recipient_account_id=self.c2.account_id)
        self.assertEqual(self.c1.balance_checking, 400)
        self.assertEqual(self.c2.balance_checking, 300)
        self.assertEqual(txn.status, "SUCCESS")

if __name__ == "__main__":
    unittest.main()
