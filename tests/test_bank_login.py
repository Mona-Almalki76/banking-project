import unittest
from classes.bank import Bank

class TestBankLogin(unittest.TestCase):
    def setUp(self):
        self.bank = Bank()
        self.customer = self.bank.add_customer("Mona", "Almalki", "pass123")

    def test_login_success(self):
        result = self.bank.login(self.customer.account_id, "pass123")
        self.assertTrue(result)
        self.assertEqual(self.bank.logged_in_customer, self.customer)

    def test_login_wrong_password(self):
        with self.assertRaises(PermissionError):
            self.bank.login(self.customer.account_id, "wrongpass")

    def test_login_account_not_found(self):
        with self.assertRaises(ValueError):
            self.bank.login("99999", "pass123")

    def test_logout(self):
        self.bank.login(self.customer.account_id, "pass123")
        self.bank.logout()
        self.assertIsNone(self.bank.logged_in_customer)

if __name__ == "__main__":
    unittest.main()
