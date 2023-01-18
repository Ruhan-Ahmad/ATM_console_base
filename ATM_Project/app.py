"""
This is the atm console base application which consists of two roles admin and users. Admin allowed to create, update,
delete, view users and specific user transactions and also able ot change password and roles for the users.
User can see their transaction which consist of 7 days, 30 days and 90 days. They are also able to
transfer, withdraw and deposit into their account based upon limits set by the admin. they can also change their
passwords.
"""
__auther__ = "Ruhan_Ahmad"

import getpass  # use for the purpose of hiding the password on entering on terminal
import json  # use for the purpose of parsing the data
import os  # use to check .json file if they are available or not
import time as t  # use for storing the time of transaction
from datetime import datetime  # use to calculate the difference b/w time
from admin import Admin  # Admin.py file from which Admin is the class


class Main:
    def __init__(self):
        self.choice = ""  # this will control main menu navigation
        self.option = ""  # all other navigation within main menu will handle by this
        self.name = ""  # hold name of the user
        self.password = ""  # hold password of the user
        self.deposit = ""  # hold deposit limit read from file
        self.withdraw = ""  # hold withdraw limit
        self.transfer = ""  # hold transfer limit
        self.user_file = "users.json"
        self.transfer_file = "transaction.json"
        self.limit_file = "limit.json"

        self.create_files()

    def main_screen(self):
        print("***************WELCOME TO ATM APPLICATION********************")
        while True:
            print("Enter login for Login into ATM\nEnter exit for existing the ATM")
            self.choice = input("Enter your choice : ").lower()
            while True:
                if self.choice == "login":
                    self.name = input("Enter Name : ").lower()
                    if self.name == "exit":
                        break
                    self.password = getpass.getpass(prompt="Enter Password (default = 1234) : ")
                    auth = self.authenticate(self.name, self.password)
                    if auth == "admin":
                        admin = Admin()
                        while True:
                            self.admin_menu()
                            self.option = input("Enter your choice : ").lower()
                            if self.option == "create" or self.option == "1":
                                prev_names, passwords, balances, roles = self.get_all_users()
                                admin.create(prev_names)
                            elif self.option == "set" or self.option == "2":
                                while True:
                                    if (len(self.transfer) == 0 and len(
                                            self.withdraw) == 0 and len(self.deposit) == 0) or self.transfer == "0" or\
                                            self.withdraw == "0" or self.deposit == "0":
                                        print("Admin please set the limit")
                                    else:
                                        print("Withdraw limit : ", self.withdraw, "       ", "Transfer limit : ",
                                              self.transfer, "      ", "Deposit limit : ", self.deposit)
                                    transfer = self.transfer
                                    withdraw = self.withdraw
                                    deposit = self.deposit
                                    print("Enter 'exit' for exiting to previous menu")
                                    self.transfer = input("Enter Transfer limit : ")
                                    if self.transfer == "exit":
                                        break
                                    self.deposit = input("Enter Deposit Limit : ")
                                    self.withdraw = input("Enter Withdraw limit : ")
                                    if self.withdraw.isnumeric() and self.transfer.isnumeric() \
                                            and self.deposit.isnumeric():
                                        admin.set_limit(self.transfer, self.withdraw, self.deposit)
                                    else:
                                        self.deposit = deposit
                                        self.withdraw = withdraw
                                        self.transfer = transfer
                                        print("Limit must be in integer")
                            elif self.option == "update" or self.option == "3":
                                while True:
                                    print("Enter 'exit' to exit the system")
                                    self.name = input("Enter Account Holder Name for to Update Credentials : ")
                                    if self.name == "exit":
                                        break
                                    names, passwords, balances, roles = self.get_all_users()
                                    is_user = admin.search(self.name, names)
                                    if is_user:
                                        while True:
                                            index = self.get_account_index(self.name, names)

                                            print(names[index], "       ", passwords[index], "        ",
                                                  balances[index], "      ", roles[index])
                                            print("What Credentials Do You Want to Update")
                                            print("Enter '1 or password' to update account password")
                                            print("Enter '2 or balance' to update account balance")
                                            print("Enter '3 or role' to change role of user")
                                            print("Enter 'exit' to exit to prev menu")
                                            self.option = input("Enter your choice : ")
                                            if self.option == "exit":
                                                break
                                            elif self.option == "password" or self.option == "1":
                                                while True:
                                                    print("Enter 'exit' to exit to previous menu")
                                                    password = input("Enter Updated Password : ")
                                                    if password == "exit":
                                                        break
                                                    passwords[index] = password
                                                    # print(names, passwords, balances, roles)
                                                    self.update(names, passwords, balances, roles)
                                                    print("Password of user updated!")
                                                    break
                                            elif self.option == "balance" or self.option == "2":
                                                while True:
                                                    print("Enter 'exit' to exit to previous menu")
                                                    balance = input("Enter Updated Balance : ")
                                                    if balance == "exit":
                                                        break
                                                    balances[index] = balance
                                                    self.update(names, passwords, balances, roles)
                                                    print("Balance of user updated!")
                                                    break
                                            elif self.option == "role" or self.option == "3":
                                                while True:
                                                    print("Enter 'exit' to exit to previous menu")
                                                    role = input("Enter Updated Role : ")
                                                    if role == "exit":
                                                        break
                                                    roles[index] = role
                                                    self.update(names, passwords, balances, roles)
                                                    print("Role of user updated!")
                                                    break
                                    else:
                                        print("No user found in the ATM with this name")
                            elif self.option == "view" or self.option == "5":
                                names, password, balances, roles = self.get_all_users()
                                admin.view(names, balances, roles)
                            elif self.option == "search" or self.option == "6":
                                while True:
                                    names, passwords, balances, roles = self.get_all_users()
                                    name_to_be_search = input("Enter Name for Search the User : ")
                                    if name_to_be_search == "exit":
                                        break
                                    result = admin.search(name_to_be_search, names)
                                    if result:
                                        index_search = names.index(name_to_be_search)
                                        print("Name         ", "Balance         ", "Role")
                                        print(names[index_search], "         ", balances[index_search],
                                              "               ", roles[index_search])
                                    else:
                                        print("No Account Holder with this Name Exist!")
                            elif self.option == "delete" or self.option == "4":
                                while True:
                                    names, passwords, balances, roles = self.get_all_users()
                                    name_to_be_delete = input("Enter Name for Delete the User : ")
                                    if name_to_be_delete == "exit":
                                        break
                                    result_delete = admin.search(name_to_be_delete, names)
                                    if result_delete:
                                        index_delete = names.index(name_to_be_delete)
                                        names.pop(index_delete)
                                        passwords.pop(index_delete)
                                        balances.pop(index_delete)
                                        roles.pop(index_delete)
                                        self.update(names, passwords, balances, roles)
                                        print("Account deleted!")
                                        break
                                    else:
                                        print("No Account Holder with this Name Exist!")
                            elif self.option == "transaction" or self.option == "7":
                                name = self.name
                                while True:
                                    self.name = input("Enter Name to see their transaction : ")
                                    if self.name == "exit":
                                        break
                                    names, types, amounts, transfers, times = self.get_all_transaction()
                                    # print(names, types, amounts, times)
                                    admin = Admin()
                                    is_user = admin.search(self.name, names)
                                    if is_user:
                                        indexs = self.get_transaction_index(self.name, names)
                                        if len(indexs) != 0:
                                            # print(indexs)
                                            print("Name          ", "Type        ", "Amount       ",
                                                  "Transfer To        ", "Time       ")
                                            for index in indexs:
                                                print(names[index], "      ", types[index],
                                                      "        ", amounts[index], "       ", transfers[index],
                                                      "        ", times[index])
                                                self.name = name
                                        else:
                                            print("No Transaction occur by this user")
                                            self.name = name
                                    else:
                                        print(f"{self.name} is not the user of ATM")
                                        self.name = name
                            elif self.option == "exit":
                                break

                    elif auth == "user":
                        while True:
                            print("Account holder : ", self.name)
                            names, passwords, balances, roles = self.get_all_users()
                            index = self.get_account_index(self.name, names)
                            print("Your Balance : ", balances[index])
                            self.user_menu()
                            self.option = input("Enter your choice : ").lower()
                            if self.option == "view" or self.option == "1":
                                while True:
                                    names, types, amounts, transfers, times = self.get_all_transaction()
                                    indexs = self.get_transaction_index(self.name, names)
                                    print("Enter '1' to view last 7 days transactions")
                                    print("Enter 2 to view last 30 days transactions")
                                    print("Enter 3 to view last 90 days transactions")
                                    print("Enter 'exit' to exit to prev menu")
                                    self.option = input("Enter your option : ")
                                    if self.option == "exit":
                                        break
                                    if self.option == "1":
                                        duration = 7
                                        self.print_transactions(duration, indexs, names, types, amounts, transfers,
                                                                times)
                                    elif self.option == "2":
                                        duration = 30
                                        self.print_transactions(duration, indexs, names, types, amounts, transfers,
                                                                times)
                                    elif self.option == "3":
                                        duration = 90
                                        self.print_transactions(duration, indexs, names, types, amounts, transfers,
                                                                times)
                                    else:
                                        print("Please Enter a valid response")
                            elif self.option == "transfer" or self.option == "2":
                                while True:
                                    admin = Admin()
                                    names, passwords, balances, roles = self.get_all_users()
                                    index = self.get_account_index(self.name, names)
                                    print("Enter 'exit' to exit to previous menu")
                                    account_name = input("Enter Account to which you want to transfer : ")
                                    if account_name == "exit":
                                        break
                                    check = admin.search(account_name, names)
                                    if check:
                                        while True:
                                            sender_index = self.get_account_index(account_name, names)
                                            print("Transfer limit is : ", self.transfer)
                                            print("Account Balance is : ", balances[index])
                                            print("Enter 'exit' to exit the system")
                                            amount = input("Enter amount to be transferred : ")
                                            if amount == "exit":
                                                break
                                            if int(amount) <= int(balances[index]):
                                                if int(amount) <= int(self.transfer):
                                                    self.withdraw_amount(balances, index, amount)
                                                    self.deposite_amount(balances, sender_index, amount)
                                                    type_of_transaction = "transfer"
                                                    self.write_transaction(type_of_transaction, amount, names,
                                                                           passwords, balances, roles, account_name)
                                                    print("Amount Transferred successfully!")
                                                    break
                                                else:
                                                    print("Amount should be less than transfer limit")
                                            else:
                                                print("Your don't have enough money for to transfer")
                                    else:
                                        print("No account with these name exist into atm")

                            elif self.option == "edit" or self.option == "5":
                                while True:
                                    names, passwords, balances, roles = self.get_all_users()
                                    index = self.get_account_index(self.name, names)
                                    print("Enter 'exit' to go to previous menu")
                                    password = input("Enter Password : ")
                                    if password == "exit":
                                        break
                                    confirm_password = input("Re-Enter your password : ")
                                    if password == confirm_password:
                                        if len(password) >= 4 and len(confirm_password) >= 4:
                                            passwords[index] = password
                                            self.password = password
                                            self.update(names, passwords, balances, roles)
                                            print("Password updated successfully!")
                                            break
                                        else:
                                            print("Password length should be at least 4 digits")
                                    else:
                                        print("Password and confirm password should match!")

                            elif self.option == "deposit" or self.option == "4":  # for deposit the amount
                                while True:
                                    names, passwords, balances, roles = self.get_all_users()
                                    print("Deposit limit : ", self.deposit)
                                    deposit = input("Enter the amount you want to deposit : ")
                                    if deposit == "exit":
                                        break
                                    if deposit.isnumeric():
                                        if int(deposit) >= int(self.deposit):
                                            self.deposite_amount(balances, index, deposit)
                                            type_of_transaction = "deposit"
                                            transfer_to = "self"
                                            self.write_transaction(type_of_transaction, deposit, names, passwords,
                                                                   balances, roles, transfer_to)
                                            # print(data)
                                            print("Amount is deposited")
                                            break
                                        else:
                                            print("Deposit amount should be at-least : ", self.deposit)
                                    else:
                                        print("Deposit amount should be integer")
                            elif self.option == "withdraw" or self.option == "3":  # for withdraw amount
                                # from the user account
                                while True:
                                    names, passwords, balances, roles = self.get_all_users()
                                    print("Withdraw limit : ", self.withdraw)
                                    withdraw = input("Enter the amount you want to withdraw : ")
                                    if withdraw == "exit":
                                        break
                                    if withdraw.isnumeric():
                                        if int(withdraw) <= int(self.withdraw):
                                            if int(withdraw) <= int(balances[index]):
                                                self.withdraw_amount(balances, index, withdraw)
                                                type_of_transaction = "withdraw"
                                                transfer_to = "self"
                                                self.write_transaction(type_of_transaction, withdraw, names, passwords,
                                                                       balances,
                                                                       roles, transfer_to)
                                                print("Amount is withdraw")
                                                break
                                            else:
                                                print("Not enough money in your account, your account balance is : ",
                                                      balances[index])
                                        else:
                                            print("Withdraw amount should be maximum : ", self.withdraw)
                                    else:
                                        print("withdraw amount should be integer")
                            elif self.option == "exit":
                                break
                    else:
                        print(auth)
                        continue

                elif self.choice == "exit":
                    exit(0)
                else:
                    print("Please Enter a valid response!")
                    break

    @staticmethod
    def deposite_amount(balances, index, amount):
        balances[index] = int(balances[index]) + int(amount)
        balances[index] = str(balances[index])

    @staticmethod
    def withdraw_amount(balances, index, amount):
        balances[index] = int(balances[index]) - int(amount)
        balances[index] = str(balances[index])

    def update(self, names, passwords, balances, roles):
        entry = []
        for i in range(len(names)):
            data = {"Name": names[i], "Password": passwords[i],
                    "Balance": balances[i], "role": roles[i]}
            data = json.dumps(data)
            data = data + "\n"
            entry.append(data)
            # print(data)
        file = open(self.user_file, "r+")
        file.truncate(0)
        for data in entry:
            fil = open(self.user_file, 'a')
            fil.write(data)
            fil.close()

    def write_transaction(self, type_of_transaction, amount, names, passwords, balances, roles, transfer_to):
        self.update(names, passwords, balances, roles)
        data = {"Name": self.name, "Type": type_of_transaction, "Amount": amount,
                "Transfer_to": transfer_to, "Time": t.strftime("%x")}
        data = json.dumps(data)
        data = data + "\n"
        file = open(self.transfer_file, "a")
        file.write(data)
        file.close()

    @staticmethod
    def print_transactions(duration, indexs, names, types, amounts, transfers, times):
        if len(indexs) != 0:
            print("Name              ", "Type           ", "Amount        ",
                  "Transfer To        ", "Time")
            for index in indexs:
                curr_date = t.strftime("%x")
                trans_data = times[index]
                d1 = datetime.strptime(curr_date, "%m/%d/%y")
                d2 = datetime.strptime(trans_data, "%m/%d/%y")
                time = d1 - d2
                if int(time.days) <= duration:
                    # print(time.days)
                    print(names[index], "          ", types[index], "          ",
                          amounts[index], "         ", transfers[index], "        ",
                          times[index])
        else:
            print(f"No Transaction in last {duration} days")

    @staticmethod
    def user_menu():
        print("Enter '1 or view' to see all your transactions")  # done
        print("Enter '2 or transfer' to transfer money to someone")  # done
        print("Enter '3 or withdraw' to withdraw money from your account")  # done
        print("Enter '4 or deposit' to deposit money into your account")  # done
        print("Enter '5 or edit' to edit your password")  # done
        print("Enter 'exit' to exit to previous menu")  # done

    @staticmethod
    def admin_menu():
        print("***************WELCOME ADMIN****************")
        print("Enter '1 or create' for creating new user account")  # done
        print("Enter '2 or set' to set the withdraw and transfer limit")  # done
        print("Enter '3 or update' for update user credentials")  # done
        print("Enter '4 or delete' for deleting the user")  # done
        print("Enter '5 or view' for view all the user of ATM")  # done
        print("Enter '6 or search' to search a specific user")  # done
        print("Enter '7 or transaction' to view all the transaction")  # done
        print("Enter 'exit' to exit the system")  # done

    def get_all_users(self):
        names = []
        password = []
        balances = []
        roles = []
        with open(self.user_file) as users:
            for user in users:
                usr = json.loads(user)
                names.append(usr["Name"])
                password.append(usr["Password"])
                balances.append(usr["Balance"])
                roles.append(usr["role"])
        users.close()
        return names, password, balances, roles

    def get_all_transaction(self):  # this is the static method that will return all the transactions in json format
        names = []
        types = []
        amounts = []
        transfer_to = []
        times = []
        with open(self.transfer_file) as transactions:
            for transaction in transactions:
                trans = json.loads(transaction)
                names.append(trans["Name"])
                types.append(trans["Type"])
                amounts.append(trans["Amount"])
                transfer_to.append(trans["Transfer_to"])
                times.append(trans["Time"])
        transactions.close()
        return names, types, amounts, transfer_to, times

    def authenticate(self, name, password):  # this will authenticate the user if available in users.json
        names, passwords, balances, roles = self.get_all_users()
        index = self.get_account_index(name, names)
        if name in names:
            if password == passwords[index]:
                index_for_role = names.index(name)
                role = roles[index_for_role]
                return role
            else:
                return "Wrong Password! Try Again"
        else:
            return "This user is not valid!"

    @staticmethod
    def get_account_index(name, names):  # this will return the index of user
        if name in names:
            index = names.index(name)
            return index
        else:
            return 0

    @staticmethod
    def get_transaction_index(name, names):  # this will return all the indexes of the transaction occur by users
        indexs = []
        for idx, value in enumerate(names):
            if value == name:
                indexs.append(idx)
        return indexs

    def create_files(self):
        if os.path.exists(self.user_file):  # check if file is available in the path
            names, passwords, balances, roles = self.get_all_users()
            if len(names) == 0:
                data = {"Name": "admin", "Password": "admin", "Balance": "0", "role": "admin"}
                data = json.dumps(data)
                data = data + "\n"
                file = open(self.user_file, 'a')
                file.write(data)
            else:
                pass
        else:
            if open(self.user_file, 'x'):
                data = {"Name": "admin", "Password": "admin", "Balance": "0", "role": "admin"}
                data = json.dumps(data)
                data = data + "\n"
                file = open(self.user_file, 'a')
                file.write(data)
                print("file created")

        if os.path.exists(self.limit_file):
            with open(self.limit_file) as limit:
                for lim in limit:
                    li = json.loads(lim)
                    self.transfer = li["transfer"]
                    self.deposit = li["deposit"]
                    self.withdraw = li["withdraw"]
            limit.close()

        else:
            if open(self.limit_file, 'x'):
                data = {"transfer": "0", "deposit": "0", "withdraw": "0"}
                data = json.dumps(data)
                file = open(self.limit_file, 'w')
                file.write(data)
                print("limit file created")

        if os.path.exists(self.transfer_file):
            pass
        else:
            open(self.transfer_file, "x")
            print("file created.")


if __name__ == "__main__":
    m = Main()
    m.main_screen()
