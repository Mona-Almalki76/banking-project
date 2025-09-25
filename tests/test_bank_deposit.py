import unittest
from classes.bank import Bank
from classes.customer import Customer

class TestBankDeposit(unittest.TestCase):
    def setUp(self):
        self.bank = Bank()
        self.customer = self.bank.add_customer("Mona", "Almalki", "pass123")
        self.bank.login(self.customer.account_id, "pass123")

    def test_deposit_checking_success(self):
        transaction = self.bank.deposit(500, "checking")
        self.assertEqual(self.customer.balance_checking, 500.0)
        self.assertEqual(transaction.account_id, self.customer.account_id)
        self.assertEqual(transaction.transaction_type, "deposit")
        self.assertEqual(transaction.amount, 500)
        self.assertEqual(transaction.account_type, "checking")
        self.assertEqual(transaction.status, "SUCCESS")

    def test_deposit_savings_success(self):
        transaction = self.bank.deposit(300, "savings")
        self.assertEqual(self.customer.balance_savings, 300.0)
        self.assertEqual(transaction.account_type, "savings")
        self.assertEqual(transaction.amount, 300)
        self.assertEqual(transaction.status, "SUCCESS")

if __name__ == "__main__":
    unittest.main()
