from classes.customer import Customer
import csv
import os
class Bank:
    def __init__(self):
        self.customers = {}

    # generate account id automatically
    def auto_id_generated(self):
        if self.customers:
            max_id = 0
            for account_id in self.customers.keys():
                account_num = int(account_id)
                if account_num > max_id:
                    max_id = account_num
            return str(max_id + 1)
        return "10001" # no customer yet

    # Add New Customer
    def add_customer(self, frst_name, last_name, password, given_id=None, create_checking=True, create_savings=True):
        # cashiers can type in an id or this can be automatically generated
        if given_id:
            account_id = given_id
        else:
            account_id = self.auto_id_generated()

        # customer can have a checking account
        # customer can have a savings account
        # customer can have both a checking and a savings account
        if create_checking:
            balance_checking = 0.0
        else:
            balance_checking = None

        if create_savings:
            balance_savings = 0.0
        else:
            balance_savings = None

        customer = Customer(account_id, frst_name, last_name, password, balance_checking, balance_savings)
        self.customers[account_id] = customer
        return customer
    
    # login
    def login(self, account_id, password):
        customer = self.customers.get(account_id)
        if not customer:
            raise ValueError("Account not found")
        if customer.password != password:
            raise PermissionError("Invalid password")
        self.logged_in_customer = customer
        return True

    # logout
    def logout(self):
        self.logged_in_customer = None

    # save customers to csv file
    def save_customers_to_csv(self, filename="bank.csv"):
        fieldnames = ["account_id", "frst_name", "last_name",
                    "password", "balance_checking", "balance_savings"]
        
        write_header = not os.path.exists(filename)

        with open(filename, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            if write_header:
                writer.writeheader()

            for customer in self.customers.values():
                writer.writerow({
                    "account_id": customer.account_id,
                    "frst_name": customer.frst_name,
                    "last_name": customer.last_name,
                    "password": customer.password,
                    "balance_checking": customer.balance_checking,
                    "balance_savings": customer.balance_savings
                })
