import random
from datetime import datetime

accounts = {}

def generate_account_number():
    while True:
        acc_no = random.randint(100000, 999999)
        if acc_no not in accounts:
            return acc_no


def get_timestamp():
   
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


def add_history(acc_no, entry):
    
    accounts[acc_no]["history"].append(f"[{get_timestamp()}] {entry}")


def line():
    print("-" * 45)


def create_account():
    line()
    print("CREATE A NEW ACCOUNT")
    line()
    name = input("Enter your name: ").strip().title()   # string operation
    phone = input("Enter your phone number: ").strip()

    while not phone.isdigit() or len(phone) != 10:
        print("Invalid phone number. Please enter a 10-digit number.")
        phone = input("Enter your phone number: ").strip()

    while True:
        pin = input("Create a 4-digit PIN: ").strip()
        confirm_pin = input("Confirm PIN: ").strip()
        if pin != confirm_pin:
            print("PINs do not match. Try again.\n")
        elif not pin.isdigit() or len(pin) != 4:
            print("PIN must be exactly 4 digits.\n")
        else:
            break

    acc_no = generate_account_number()
    accounts[acc_no] = {
        "name": name,
        "phone": phone,
        "pin": pin,
        "balance": 0.0,
        "history": []
    }
    add_history(acc_no, "Account created")

    line()
    print("Account created successfully!")
    print(f"Your Account Number is: {acc_no}")
    print("Please note this down. You will need it to log in.")
    line()


def login():
    line()
    print("LOGIN")
    line()
    try:
        acc_no = int(input("Enter Account Number: ").strip())
    except ValueError:
        print("Invalid account number format.")
        return None

    pin = input("Enter PIN: ").strip()

    if acc_no in accounts and accounts[acc_no]["pin"] == pin:
        print(f"\nWelcome, {accounts[acc_no]['name']}!")
        return acc_no
    else:
        print("Invalid Account Number or PIN.")
        return None


def check_balance(acc_no):
    line()
    print(f"Account Holder : {accounts[acc_no]['name']}")
    print(f"Current Balance: Rs. {accounts[acc_no]['balance']:.2f}")
    line()


def deposit(acc_no):
    line()
    try:
        amount = float(input("Enter amount to deposit: Rs. "))
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
    except ValueError:
        print("Invalid amount entered.")
        return

    accounts[acc_no]["balance"] += amount
    add_history(acc_no, f"Deposited Rs. {amount:.2f}")
    print(f"Rs. {amount:.2f} deposited successfully.")
    print(f"New Balance: Rs. {accounts[acc_no]['balance']:.2f}")


def withdraw(acc_no):
    line()
    try:
        amount = float(input("Enter amount to withdraw: Rs. "))
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
    except ValueError:
        print("Invalid amount entered.")
        return

    if amount > accounts[acc_no]["balance"]:
        print("Insufficient balance!")
        return

    accounts[acc_no]["balance"] -= amount
    add_history(acc_no, f"Withdrew Rs. {amount:.2f}")
    print(f"Rs. {amount:.2f} withdrawn successfully.")
    print(f"New Balance: Rs. {accounts[acc_no]['balance']:.2f}")


def transfer(acc_no):
    line()
    try:
        receiver_no = int(input("Enter receiver's account number: ").strip())
    except ValueError:
        print("Invalid account number format.")
        return

    if receiver_no not in accounts:
        print("Receiver account does not exist.")
        return
    if receiver_no == acc_no:
        print("You cannot transfer money to your own account.")
        return

    try:
        amount = float(input("Enter amount to transfer: Rs. "))
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
    except ValueError:
        print("Invalid amount entered.")
        return

    if amount > accounts[acc_no]["balance"]:
        print("Insufficient balance!")
        return

    accounts[acc_no]["balance"] -= amount
    accounts[receiver_no]["balance"] += amount

    add_history(acc_no, f"Transferred Rs. {amount:.2f} to Account {receiver_no}")
    add_history(receiver_no, f"Received Rs. {amount:.2f} from Account {acc_no}")

    print(f"Rs. {amount:.2f} transferred to Account {receiver_no} successfully.")
    print(f"New Balance: Rs. {accounts[acc_no]['balance']:.2f}")


def view_history(acc_no):
    line()
    print(f"TRANSACTION HISTORY - Account {acc_no}")
    line()
    history = accounts[acc_no]["history"]
    if not history:
        print("No transactions yet.")
    else:
        for i, entry in enumerate(history, start=1):
            print(f"{i}. {entry}")
    line()


def change_pin(acc_no):
    line()
    old_pin = input("Enter old PIN: ").strip()
    if old_pin != accounts[acc_no]["pin"]:
        print("Incorrect old PIN.")
        return

    new_pin = input("Enter new PIN: ").strip()
    confirm_pin = input("Confirm new PIN: ").strip()

    if new_pin != confirm_pin:
        print("New PINs do not match.")
        return
    if not new_pin.isdigit() or len(new_pin) != 4:
        print("PIN must be exactly 4 digits.")
        return

    accounts[acc_no]["pin"] = new_pin
    add_history(acc_no, "PIN changed")
    print("PIN changed successfully.")



def account_menu(acc_no):
    while True:
        line()
        print("ACCOUNT MENU")
        line()
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Transaction History")
        print("6. Change PIN")
        print("7. Logout")
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            check_balance(acc_no)
        elif choice == "2":
            deposit(acc_no)
        elif choice == "3":
            withdraw(acc_no)
        elif choice == "4":
            transfer(acc_no)
        elif choice == "5":
            view_history(acc_no)
        elif choice == "6":
            change_pin(acc_no)
        elif choice == "7":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please select between 1 and 7.")


def main_menu():
    while True:
        line()
        print("BANKING SYSTEM - MAIN MENU")
        line()
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            create_account()
        elif choice == "2":
            acc_no = login()
            if acc_no is not None:
                account_menu(acc_no)
        elif choice == "3":
            print("Thank you for using the Banking System. Goodbye!")
            break
        else:
            print("Invalid choice. Please select between 1 and 3.")


if __name__ == "__main__":
    main_menu()