import json


class Admin:
    def __init__(self):
        self.name = ""
        self.password = "1234"
        self.balance = "0"
        self.role = ""
        self.file = "users.json"

    def create(self, names):
        self.name = input("Enter name : ")
        self.role = input("Enter role(user or admin) : ")
        if self.role == "admin" or self.role == "user":
            if self.name in names:
                print("Account already exists!")
            else:
                file = open(self.file, 'a')
                data = {"Name": self.name, "Password": self.password, "Balance": self.balance, "role": self.role}
                data = json.dumps(data)
                data = data + "\n"
                if file.write(data):
                    print("user created.")
        else:
            print("Role must be admin or user")

    @staticmethod
    def view(names, balances, roles):
        if len(names) != 0:
            print("Name", "     ", "Balance", "     ", "Roles")
            for i in range(len(names)):
                print(names[i], '     ', balances[i], "       ", roles[i])
        else:
            print("There is no user currently enrolled.")

    @staticmethod
    def set_limit(transfer, deposit, withdraw):
        file = open("limit.json", 'w')
        data = {"transfer": transfer, "deposit": deposit, "withdraw": withdraw}
        data = json.dumps(data)
        if file.write(data):
            print("Limit set successfully!")
        else:
            print("Error occur during saving file.")

    @staticmethod
    def search(name, names):
        if name in names:
            return True
        else:
            return False
