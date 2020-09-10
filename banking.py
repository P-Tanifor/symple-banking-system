#
import random
import sqlite3


conn = sqlite3.connect("card.s3db")
cur = conn.cursor()
cur.execute("create table if not exists card(id integer , number text, pin text, balance integer default 0)")
conn.commit()

class AccountCreation:

    def __init__(self):
        self.generated_number = None
        self.pin = None

    def generate_number(self):
        new_str = ""
        part_number = random.sample(range(10), 10)
        generated_number = "400000"

        for i in part_number:
            generated_number += str(i)

        for j in range(len(generated_number) - 1):
            new_str += generated_number[j]
        mult_ = ""

        for k in range(len(new_str)):
            over_nine = 0
            if (k + 1) % 2 == 0:
                mult_ += new_str[k]
            else:
                over_nine = (int(new_str[k]) * 2)
                if over_nine > 9:
                    over_nine -= 9
                    mult_ += str(over_nine)
                else:
                    mult_ += str(over_nine)

        sum_ = 0
        for u in mult_:
            sum_ += int(u)

        if sum_ % 10 == 0:
            new_str += str(0)
        else:
            new_str += str(10 - (sum_ % 10))

        self.generated_number = new_str
        return self.generated_number

    def id(self):
        user_id = ""
        id_ = 0
        for i in range(9):
            user_id += self.generated_number[i + 7]
        id_ = int(user_id)
        return id_

    def generate_pin(self):
        new_pin = random.sample(range(10), 4)
        self.pin = ""
        for i in new_pin:
            self.pin += str(i)
        return self.pin

    def add_income(self, income_to_add):
        new_balance = self.get_balance() + income_to_add
        cur.execute(f"update card  set balance = {new_balance} where number = {self.generated_number}")
        conn.commit()
        print("Income was added!")

    def do_transfer(self, beneficiary_account):
            new_str = ""
            for j in range(len(beneficiary_account) - 1):
                new_str += beneficiary_account[j]
            mult_ = ""

            for k in range(len(new_str)):
                over_nine = 0
                if (k + 1) % 2 == 0:
                    mult_ += new_str[k]
                else:
                    over_nine = (int(new_str[k]) * 2)
                    if over_nine > 9:
                        over_nine -= 9
                        mult_ += str(over_nine)
                    else:
                        mult_ += str(over_nine)
            sum_ = 0
            for u in mult_:
                sum_ += int(u)

            if (sum_ + int(beneficiary_account[-1])) % 10 == 0:

                cur.execute(f"select id from card where number = {beneficiary_account}")
                account_id = cur.fetchone()
                if account_id == None:
                    print("Such a card does not exist.")
                else:
                    if beneficiary_account == self.generated_number:
                        print("You can't transfer money to the same account!")
                    else:
                        print("Enter how much money you want to transfer: ")
                        amount_to_transfer = int(input())
                        current_balance = self.get_balance() - amount_to_transfer
                        if current_balance < 0:
                            print("Not enough money!")
                        else:
                            cur.execute(f"update card set balance = {current_balance} where number = {self.generated_number} ")
                            cur.execute(f"select balance from card where number = {beneficiary_account}")
                            tuple_value = cur.fetchone()
                            for j in tuple_value:
                                beneficiary_balance = j
                            cur.execute(
                                f"update card set balance = {beneficiary_balance + amount_to_transfer} where number = {beneficiary_account} ")
                            conn.commit()
                            print("Success!")
            else:
                print("Probably you made a mistake in the card number. Please try again!")

    def log_in(self, number, entered_pin):
        cur.execute(f"select id from card where number = {number}")
        value1 = cur.fetchone()
        cur.execute(f"select id from card where pin = {entered_pin}")
        value2 = cur.fetchone()

        if (number == self.generated_number or value1 is not None) and (entered_pin == self.pin or value2 is not None):
            self.generated_number = number
            self.pin = entered_pin
            print("""
            You have successfully logged in!

            1. Balance
            2. Add income
            3. Do transfer
            4. Close account
            5. Log out
            0. Exit
            """)

        else:
            print("Wrong card number or PIN!")

    def menu(self):
        print("""

            1. Balance
            2. Add income
            3. Do transfer
            4. Close account
            5. Log out
            0. Exit
            """)

    def get_balance(self):
        cur.execute(f"select balance from card where number = {self.generated_number} ")
        tuple_value = cur.fetchone()
        for i in tuple_value:
            account_balance = i
        return account_balance

    def balance(self):
        account_balance = 0
        print(f"""
        Balance: {account_balance}

        1. Balance
        2. Log out
        0. Exit
        """)
        return account_balance

    def log_out(self):
        print("You have successfully logged out!")

    def close_account(self):
        cur.execute(f"delete from card where number = {self.generated_number}")
        conn.commit()
        print("The account has been closed!")

    def exit(self):
        print("Bye!")
        
        
card_number = AccountCreation()

while True:

    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")

    customer_choice = int(input())
    if customer_choice == 1:

        print("Your card has been created")
        print("Your card number:")
        print(f"{card_number.generate_number()}")
        print("Your card PIN:")
        print(f"{card_number.generate_pin()}")
        cur.execute(f"insert into card values({card_number.id()}, {card_number.generated_number},"
                    f" {card_number.pin}, {card_number.balance()})")
        conn.commit()
    elif customer_choice == 2:
        print("Enter your card number")
        entered_number = input()
        print("Enter your PIN")
        entered_pin = input()
        card_number.log_in(entered_number, entered_pin)
        while True:
            user_input = int(input())

            if user_input == 1:
                print(card_number.get_balance())
            elif user_input == 2:
                print("Enter income: ")
                amount = int(input())
                card_number.add_income(amount)
            elif user_input == 3:
                print("Enter beneficiary account: ")
                beneficiary_account = input()
                card_number.do_transfer(beneficiary_account)
            elif user_input == 4:
                card_number.close_account()
            elif user_input == 5:
                card_number.log_out()
                break
            elif user_input == 0:
                card_number.exit()
                break
            card_number.menu()
        break

    elif customer_choice == 0:
        card_number.exit()
        break
