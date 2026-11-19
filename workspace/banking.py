# banking.py

class InsufficientFundsError(Exception):
    """Raised when attempting to withdraw more than the available balance."""
    pass

class InvalidAmountError(Exception):
    """Raised when deposit or withdraw amount is not positive."""
    pass

class BankAccount:
    def __init__(self, initial_balance: float = 0.0):
        if initial_balance < 0:
            raise InvalidAmountError("Initial balance cannot be negative.")
        self._balance = float(initial_balance)

    def deposit(self, amount: float) -> None:
        """Deposit a positive amount into the account."""
        if amount <= 0:
            raise InvalidAmountError("Deposit amount must be positive.")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        """Withdraw a positive amount from the account if sufficient funds exist."""
        if amount <= 0:
            raise InvalidAmountError("Withdrawal amount must be positive.")
        if amount > self._balance:
            raise InsufficientFundsError("Insufficient balance for withdrawal.")
        self._balance -= amount

    def balance(self) -> float:
        """Return the current account balance."""
        return self._balance

    def __repr__(self) -> str:
        return f"BankAccount(balance={self._balance})"

# Simple demonstration when run directly
if __name__ == "__main__":
    acc = BankAccount(100)
    print(f"Initial balance: {acc.balance()}")
    acc.deposit(50)
    print(f"After deposit of 50: {acc.balance()}")
    try:
        acc.withdraw(200)
    except Exception as e:
        print(f"Withdrawal failed: {e}")
    acc.withdraw(30)
    print(f"After withdrawal of 30: {acc.balance()}")
