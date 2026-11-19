import unittest
from banking import BankAccount, InsufficientFundsError, InvalidAmountError

class TestBankAccount(unittest.TestCase):
    def test_normal_transactions(self):
        acc = BankAccount(100)
        acc.deposit(50)
        self.assertAlmostEqual(acc.balance(), 150)
        acc.withdraw(20)
        self.assertAlmostEqual(acc.balance(), 130)

    def test_insufficient_balance(self):
        acc = BankAccount(30)
        with self.assertRaises(InsufficientFundsError):
            acc.withdraw(40)
        # balance should remain unchanged
        self.assertAlmostEqual(acc.balance(), 30)

    def test_invalid_amounts(self):
        acc = BankAccount()
        with self.assertRaises(InvalidAmountError):
            acc.deposit(0)
        with self.assertRaises(InvalidAmountError):
            acc.deposit(-10)
        with self.assertRaises(InvalidAmountError):
            acc.withdraw(0)
        with self.assertRaises(InvalidAmountError):
            acc.withdraw(-5)
        # also test initializing with negative balance
        with self.assertRaises(InvalidAmountError):
            BankAccount(-100)

    # New edge case tests
    def test_withdraw_exact_balance(self):
        acc = BankAccount(75.5)
        acc.withdraw(75.5)
        self.assertAlmostEqual(acc.balance(), 0.0)

    def test_deposit_decimal_amount(self):
        acc = BankAccount()
        acc.deposit(123.45)
        self.assertAlmostEqual(acc.balance(), 123.45)

    def test_multiple_transactions_balance(self):
        acc = BankAccount(200)
        acc.deposit(50.5)
        acc.withdraw(30.25)
        acc.deposit(19.75)
        acc.withdraw(100)
        expected = 200 + 50.5 - 30.25 + 19.75 - 100
        self.assertAlmostEqual(acc.balance(), expected)

if __name__ == '__main__':
    unittest.main()
