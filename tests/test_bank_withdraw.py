import unittest
from classes.bank import Bank
from classes.customer import Customer

class TestWithdraw(unittest.TestCase):
    def setUp(self):
        self.bank = Bank()
        self.c1 = Customer("10001", "Mona", "Almalki", "pass123", balance_checking=500, balance_savings=1000)
        self.bank.customers[self.c1.account_id] = self.c1
        self.bank.login("10001", "pass123")

    def test_withdraw_checking_success(self):
        transaction = self.bank.withdraw(200, account_type="checking")
        self.assertEqual(self.c1.balance_checking, 300)
        self.assertEqual(transaction.amount, 200)
        self.assertEqual(transaction.account_type, "checking")
        self.assertEqual(transaction.status, "SUCCESS")

    def test_withdraw_savings_success(self):
        transaction = self.bank.withdraw(500, account_type="savings")
        self.assertEqual(self.c1.balance_savings, 500)
        self.assertEqual(transaction.amount, 500)
        self.assertEqual(transaction.account_type, "savings")
        self.assertEqual(transaction.status, "SUCCESS")

    def test_withdraw_insufficient_funds(self):
        with self.assertRaises(ValueError):
            self.bank.withdraw(2000, account_type="checking")

    def test_withdraw_checking_overdraft_success(self):
        transaction = self.bank.withdraw(550, account_type="checking")
        self.assertEqual(self.c1.balance_checking, -85)
        self.assertEqual(transaction.amount, 550)
        self.assertEqual(transaction.status, "SUCCESS")

    def test_withdraw_checking_overdraft_limit_exceeded(self):
        with self.assertRaises(ValueError):
            self.bank.withdraw(700, account_type="checking")

if __name__ == "__main__":
    unittest.main()
