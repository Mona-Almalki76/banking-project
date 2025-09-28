from classes.bank import Bank

def main():
    bank = Bank()
    bank.load_customers_from_csv()
    
    while True:
        print("=== Welcome to the Bank System ===\n")
        print("1. Add Customer")
        print("2. Login")
        print("3. Logout")
        print("4. Withdraw")
        print("5. Deposit")
        print("6. Transfer")
        print("7. View All Transactions")
        print("8. View Transaction Details")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            frst_name = input("First Name: ")
            last_name = input("Last Name: ")
            password = input("Password: ")
            customer = bank.add_customer(frst_name, last_name, password)
            bank.save_customers_to_csv()
            print(f"Customer added with Account ID: {customer.account_id} (Saved to CSV)")

        elif choice == "2":
            account_id = input("Account ID: ")
            password = input("Password: ")
            try:
                bank.login(account_id, password)
                print(f"Logged in as {bank.logged_in_customer.frst_name}")
            except Exception as e:
                print(f"Login failed: {e}")

        elif choice == "3":
            bank.logout()
            print("Logged out successfully.")

        elif choice == "4":
            if not bank.logged_in_customer:
                print("You must login first.")
                continue
            amount = float(input("Withdraw amount: "))
            account_type = input("Account type (checking/savings): ").lower()
            try:
                transaction = bank.withdraw(amount, account_type)
                print(f"Withdrew {transaction.amount} from {account_type} account. Status: {transaction.status}")
            except Exception as e:
                print(f"Withdrawal failed: {e}")

        elif choice == "5":
            if not bank.logged_in_customer:
                print("You must login first.")
                continue
            amount = float(input("Deposit amount: "))
            account_type = input("Account type (checking/savings): ").lower()
            try:
                transaction = bank.deposit(amount, account_type)
                print(f"Deposited {transaction.amount} to {account_type} account. Status: {transaction.status}")
            except Exception as e:
                print(f"Deposit failed: {e}")

        elif choice == "6":
            if not bank.logged_in_customer:
                print("You must login first.")
                continue
            amount = float(input("Transfer amount: "))
            from_account = input("From account (checking/savings): ").lower()
            to_account = input("To account (checking/savings): ").lower()
            recipient_id = input("Recipient Account ID (leave blank for self): ")
            recipient_id = recipient_id if recipient_id else None
            try:
                transaction = bank.transfer(amount, from_account, to_account, recipient_id)
                print(f"Transferred {transaction.amount}. Status: {transaction.status}")
            except Exception as e:
                print(f"Transfer failed: {e}")

        elif choice == "7":
                if not bank.logged_in_customer:
                    print("Login required.")
                    continue
                transactions = bank.get_customer_transactions()
                if not transactions:
                    print("No transactions found.")
                else:
                    print("\n--- All Transactions ---")
                    for i in range(len(transactions)):
                        t = transactions[i]
                        print(f"{i}: {t['transaction_type']} ${t['amount']} [{t['account_type']}] at {t['timestamp']} Status: {t['status']}")

        elif choice == "8":
                if not bank.logged_in_customer:
                    print("Login required.")
                    continue
                index = int(input("Enter transaction index: "))
                t = bank.show_transaction_details(index)
                print("\n--- Transaction Details ---")
                for key, value in t.items():
                    print(f"{key}: {value}")

        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
