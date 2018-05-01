import hashlib
class User():
        def __init__(self, ID, name, lastName, group, password, mail):
                self.ID = ID
                self.name = name
                self.lastName = lastName
                self.group = group
                self.password = password
                self.mail = mail
                

        def login(self, mail, password):
                if self.mail == mail and self.password == hashlib.sha224(password).hexdigest():
                        return True
                else:
                        return False
p = User(1, "Laura", "Akhmedova", "10ME5", hashlib.sha224(b"12345").hexdigest(), "la@mail.ru")
login = input("Login ")
password = input("password ").encode("utf-8")
if p.login(login, password):
        print("You logged in")
else:
        print("Access Denied")
