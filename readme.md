# Banking System Project

## Overview  
This project is a **terminal-based banking system** that allows users to manage checking and savings accounts.  

### Features
- **Account Management**: Create new customers with optional checking and savings accounts.  
- **Deposits and Withdrawals**: Deposit or withdraw money with proper validation.  
- **Overdraft Protection**: Accounts can temporarily overdraft up to **$100** with a **$35 fee**. Accounts are deactivated after **2 overdrafts** and can be reactivated when balances are restored.  
- **Money Transfers**: Transfer funds between a customer’s own accounts or to other customers’ accounts.  
- **Transaction History**: View all transactions or details of a single transaction, including date, type, amount, account type, and status.  
- **Data Persistence**: Customer and transaction data are stored in **CSV files** to retain information between sessions.  

---
## Code Highlight  
One feature I’m most proud of is the **overdraft and account deactivation logic** in `Customer`:  
```python
def withdraw_checking(self, amount):
    if not self.is_active:
        raise ValueError("Account is deactivated due to overdrafts")
    
    if self.balance_checking is None:
        raise ValueError("No checking account")
    
    if amount > self.balance_checking:
        overdraft_fee = 35
        new_balance = self.balance_checking - amount - overdraft_fee

        if new_balance < -100:
            raise ValueError("Overdraft limit exceeded (-100 USD max)")

        self.balance_checking = new_balance
        self.overdraft_count += 1

        if self.overdraft_count >= 2:
            self.is_active = False

        return self.balance_checking

    self.balance_checking -= amount
    return self.balance_checking 
```
I’m proud of this part because it combines validation, business rules, and customer protection in one function.
---
## What I Learned  
- **Object-Oriented Programming in Python**: classes, methods, and attributes.  
- **Transaction handling** with error checking and overdraft rules.  
- Using **CSV files** for data persistence across sessions.  
- Implementing **user authentication** and login/logout functionality.  
- **Terminal-based UI design** and handling user input efficiently.  
- Writing **unit tests** for bank operations to ensure robustness.  
