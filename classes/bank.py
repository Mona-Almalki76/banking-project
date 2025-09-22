from classes.customer import Customer
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

