import hashlib
from pick import pick
import time
import csv
import os
def home(id):
    title = "Birbcoin Terminal!\n--------------------------------\nLogged in\nWhat would you like to do today?"
    options = ["Balance", "Transfer","Exit"]
    option, index =  pick(options,title)
    if option == "Balance":
        balance_screen(id)
    if option == "Transfer":
        transfer_screen(id)
    if option == "Exit":
        exit(0)
def transfer_screen(id):
    print("Birbcoin Terminal!\n--------------------------------\nExchange!")
    input("Press any key to continue...")
    home(id)
def balance_screen(id):
    print("Birbcoin Terminal!\n--------------------------------\nMoney!")
    cols, rows = os.get_terminal_size()
    pad = " "*(int(cols/2)-12)
    print(pad.replace(" ","-")+"BALANCE"+pad.replace(" ","-"))
    bals = []
    existingids = []
    with open("data.csv","r") as f:
        datread = csv.reader(f,delimiter=",")
        
        for row in datread:
            existingids.append(str(row[0]))
            datread = csv.reader(f,delimiter=",")
            if row[1]!="bal":
                bals.append(int(row[1]))
            else:
                bals.append(int(-1))     
    print(pad+str(bals[existingids.index(id)])+" Birbcoins"+pad)
    print(pad+str(int(bals[existingids.index(id)]/6621))+"ℎ Birbcoins"+pad)
    input("Press any key to continue...")
    home(id)
def login_screen():
    print("Birbcoin Terminal!\n--------------------------------\nTime to login!")
    uname = input("> ")
    existingids = []
    phashes = []
    saline = []
    
    id = hashlib.sha256(uname.encode('ASCII')).hexdigest()
    with open("data.csv","r") as f:
        datread = csv.reader(f,delimiter=",")
        for row in datread:
            existingids.append(str(row[0]))
            
            phashes.append(row[2])
            saline.append(row[3])
    while not id in existingids:
        print("Your username is not in the database. How sad.")
        uname = input("> ")
        id = hashlib.sha256(uname.encode('ASCII')).hexdigest()
    nacl = saline[existingids.index(id)]
    print(nacl)
    print("Enter your password:")
    password1 = input("> ")
    password = hashlib.sha3_512(str(password1+nacl).encode('ASCII')).hexdigest()
    for i in range(5):
        if not password in phashes:
            print(f"You have failed {i+1} times to enter your password. Please try again")
            print("Enter your password:")
            password1 = input("> ")
            password = hashlib.sha3_512(str(password1+nacl).encode('ASCII')).hexdigest()
        else:
            break
    if not password in phashes:
        print("You are a failure.")
        time.sleep(1)
        exit(-1)
    print("You have successfully logged in!")
    balance_screen(id)

def register_screen():
    print("Birbcoin Terminal!\n--------------------------------\nLet's create a new account!")
    print("Enter account name: ")
    uname = input("> ")
    password1 = ""
    password2 = ""
    existingids = []
    id = hashlib.sha256(uname.encode('ASCII')).hexdigest()
    with open("data.csv","r") as f:
        datread = csv.reader(f,delimiter=",")
        for row in datread:
            existingids.append(str(row[0]))
    while id in existingids:
        print("That username is already taken!")
        uname = input("> ")
        id = hashlib.sha256(uname.encode('ASCII')).hexdigest()
    while password2!=password1 or len(password1)<16:
        if password2!="":
            print("Confirmation failed!")
        if (len(password1)<16 or len(password2)<16) and password2!="":
            print("Minimum password length is 16 characters! Try again!")
        print("Enter password:")
        password1 = input("> ")
        print("Confirm password:")
        password2 = input("> ")

    nacl =  hashlib.sha256(str(time.time()).encode('ASCII')).hexdigest()
    password = hashlib.sha3_512(str(password1+nacl).encode('ASCII')).hexdigest()
    password1 = ""
    password2 = ""
    with open("data.csv","a") as f:
        f.write(f"\n{id},0,{password},{nacl}")
    print("Your account has been successfully created! Now become hap hap!")
    time.sleep(1.5)
    main()
def main():
    title = "Birbcoin Terminal!\n--------------------------------\nWhat would you like to do today?"
    options = ["Login", "Register","Exit"]
    option, index =  pick(options,title)
    if option == "Login":
        login_screen()
    if option == "Register":
        register_screen()
    if option == "Exit":
        exit(0)
if __name__ == "__main__":
    main()