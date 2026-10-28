class BankAccount:
    account_list = []
    def __init__(self,name):
        self.name = name
        self.balance = 0
        BankAccount.account_list.append(self)

    def deposit(self, amount):
        if amount <= 0:
            print("Amount equal or less than zero inputted. Invalid value.")
        else:
            self.balance = self.balance + amount
    
    def withdraw(self, amount):
        if amount <= 0 or amount > self.balance:
            print("Amount equal or less than zero, or value greater than balance inputted. Invalid value.")
        else:
            self.balance = self.balance - amount
    
    def display_balance(self):
        requested_name = input("What is the name of the owner of the account?")
        for account in BankAccount.account_list:
            if account.name == requested_name:
                print("The owner's balance is: £", account.balance)
            else:
                print("Nobody with that name.")

    def create_owner(self):
        new_name = input("What is the name of the owner?")
        money = float(input("What is the starting balance of the owner?"))
        BankAccount(new_name, money)


charlie = BankAccount("charlie")
