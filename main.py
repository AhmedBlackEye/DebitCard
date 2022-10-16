from datetime import date, datetime, timedelta
from PyInquirer import prompt
from validation import *
from examples import custom_style_2
from cipher import *
from db_related import *
from random import randint
import colorama
from termcolor import cprint, colored
from pyfiglet import figlet_format
import os


class usr_interface:

    def __init__(self):
        self.db = DebitCard_db('accounts.db')
        self.usrname = ''

    def starting(self):
        starting_q = [{
            'type':
            'list',
            'name':
            'action',
            'message':
            '',
            'choices': ["Login", "Sign up", "Verify card number", 'Exit']
        }]

        self.clear()
        self.big_text('Debit Card CLI', 'cyan')
        action = prompt(starting_q, style=custom_style_2).get('action')
        if action == 'Login':
            self.login()
        elif action == 'Sign up':
            self.sign_up()
        elif action == 'Verify card number':
            self.verify_num_program()
        elif action == 'Exit':
            os._exit(1)

    def login(self):
        login_q = [{
            'type': "input",
            "name": "usrname",
            "message": "Username:",
            "validate": UsrnameValidator
        }, {
            'type': "password",
            "name": "pin",
            "message": "PIN:",
            "validate": NumValidator
        }]

        self.clear()
        self.big_text('Login', 'magenta')
        login_info = prompt(login_q, style=custom_style_2)

        if login_info.get('usrname') == 'admin' and self.db.check_passwd(
                'admin', login_info.get('pin')):
            self.usrname = 'admin'
            self.admin_program()
        elif self.db.usr_exist(login_info.get('usrname')):
            if self.db.check_passwd(login_info.get('usrname'),
                                    login_info.get('pin')):
                self.usrname = login_info.get('usrname')
                self.program()
            else:
                self.wrong_login_options()
        else:
            self.wrong_login_options()

    def wrong_login_options(self):
        choices = [{
            'type': 'list',
            'name': 'ans',
            'message': 'Your username or password was wrong',
            'choices': ["Try again", "Go back"]
        }]

        options = prompt(choices, style=custom_style_2)
        if options.get('ans') == 'Try again':
            self.login()
        else:
            self.starting()

    def sign_up(self):
        signup_q = [{
            'type': "input",
            "name": "usrname",
            "message": "Username:",
            "validate": UsrnameValidator
        }, {
            'type': "input",
            "name": "date_of_birth",
            "message": "Date Of Birth:",
            "validate": DateValidator
        }, {
            'type': "password",
            "name": "pin",
            "message": "PIN:",
            "validate": NumValidator
        }, {
            'type': 'list',
            'name': 'card_type',
            'message': 'Visa or Mastercard?',
            'choices': ["Visa", "Mastercard"]
        }, {
            'type': 'list',
            'name': 'contactless',
            'message': 'Contactless?',
            'choices': ["Yes", "No"]
        }]

        self.clear()
        self.big_text('Sign up', 'magenta')
        info = prompt(signup_q, style=custom_style_2)
        info['expiry_date'] = self.get_expiry_date(info.get('date_of_birth'))
        info['passwd'] = encrypt_(info.get('pin')).decode()
        info['card_num'] = self.get_card_num()

        if self.db.usr_exist(info.get('usrname')):
            options = [{
                'type': 'list',
                'name': 'action',
                'message': "if that\'s you then login",
                'choices': ["Login", "Sign up"]
            }]

            cprint('\n[-]User already exists', 'red')
            ans = prompt(options, style=custom_style_2)
            if ans.get('action') == 'Sign up':
                self.sign_up()
            else:
                self.login()
        elif not self.can_make_card(info['expiry_date']):
            cprint('\n[-]User must be younger than 30 to make a card', 'red')
            self.wait()
            self.starting()
        else:
            self.db.add_account(info)
            cprint(
                'Your account has successfully registered, Your informations:',
                'green')

            output = f"{'Username':18} {'Card Number':18} {'Expiry Date':12} {'Money'}\n" + '-' * 56 + f"\n{info['usrname']:18} {info['card_num']:18} {str(info['expiry_date']):12} 1000"
            cprint(output, 'yellow')
            self.wait()
            self.login()

    def get_expiry_date(self, dob):
        dob = datetime.strptime(dob, '%d/%m/%Y').date()
        days_in_30yr = int(365.25 * 30)
        expiry_date = dob + timedelta(days=days_in_30yr)
        return expiry_date

    def get_card_num(self):
        num = str(randint(1_000_000_000_000_000, 9_999_999_999_999_999))
        if not self.verify_card_number(num):
            return self.get_card_num()

        else:
            return num

    def verify_card_number(self, nums):
        total = 0
        for index, num in enumerate(nums):
            if index % 2 == 1:
                total += sum(int(i) for i in str(int(num) * 2))
            else:
                total += int(num)

        if total % 10 == 0:
            return True
        else:
            return False

    def can_make_card(self, expiry_date):
        today = date.today()
        if today > expiry_date:
            return False
        else:
            return True

    def program(self):
        program_q = [{
            'type':
            'list',
            'name':
            'action',
            'message':
            '\n' * 75,
            'choices': [
                "Show money in your account", "Add money", "Withdraw money",
                "Log out", "Delete account", "Exit"
            ]
        }]

        self.clear()
        self.big_text(f'Welcome {self.usrname}', 'yellow')
        action = prompt(program_q, style=custom_style_2)

        if action.get('action') == "Show money in your account":
            self.show_money()

        elif action.get('action') == "Add money":
            money_tobe_added = self.input_money_amount('add')
            self.db.change_money(self.usrname, money_tobe_added, "add")
            self.show_money()

        elif action.get('action') == "Withdraw money":
            self.withdraw_money()

        elif action.get('action') == "Log out":
            return self.starting()

        elif action.get('action') == "Delete account":
            self.delete_account()
            return self.starting()

        elif action.get('action') == "Exit":
            os._exit(1)

        self.program()

    def input_money_amount(self, add_or_withdraw):
        q = [{
            'type': "input",
            "name": "money",
            "message": f"How much money do you want to {add_or_withdraw}?",
            "validate": PostiveIntChecker,
            "filter": lambda val: int(val)
        }]

        ans = prompt(q, style=custom_style_2)
        return ans.get('money')

    def show_money(self):
        money = self.db.get_money_amount(self.usrname)
        cprint(f"Your account now has {money}£", 'green')
        self.wait()

    def delete_account(self):
        is_sure = [{
            'type':
            'list',
            'name':
            'ans',
            'message':
            "Are you sure of delelting your account(Y/n)? (Note:this action can't be reversed)",
            'choices':
            ["Yes, I'm sure of deleting my account", "No, I want to go back"]
        }]

        ans = prompt(is_sure, style=custom_style_2)
        if ans.get('ans') == "Yes, I'm sure of deleting my account":
            self.db.del_account(self.usrname)
            cprint("Account has been successfully deleted", 'green')
            self.wait()
        else:
            self.program()

    def withdraw_money(self):
        money_tobe_withdrawed = self.input_money_amount('withdraw')
        money_in_account = int(self.db.get_money_amount(self.usrname))
        if money_tobe_withdrawed > money_in_account:
            cprint(
                f"you can't withdraw such amount since you only have {money_in_account}\n",
                'red')
            self.wait()
        else:
            self.db.change_money(self.usrname, money_tobe_withdrawed,
                                 "withdraw")
            self.show_money()

    def verify_num_program(self):
        card_num_q = [{
            'type': 'input',
            'name': 'card_num',
            'message': 'Enter the card number:',
            "validate": CardNumValidator
        }]

        self.clear()
        self.big_text("Card Number Verifier", 'magenta')
        card_num = prompt(card_num_q, style=custom_style_2).get('card_num')
        if self.verify_card_number(card_num):
            cprint('This card number is Valid', 'green')
        else:
            cprint('This card number is invalid', 'red')
        options = [{
            'type': 'list',
            'name': 'ans',
            'message': '',
            'choices': ["Test another number", "Go back"]
        }]

        ans = prompt(options, style=custom_style_2).get('ans')
        if ans == "Test another number":
            self.verify_num_program()
        else:
            self.starting()

    def admin_program(self):
        program_q = [{
            'type':
            'list',
            'name':
            'action',
            'message':
            '\n' * 75,
            'choices': [
                "View all accounts", "Delete an account",
                "Execute SQL command", "Log out", "Exit"
            ]
        }]

        self.clear()
        self.big_text('Welcome ADMIN', 'yellow')
        action = prompt(program_q, style=custom_style_2)
        if action.get('action') == "View all accounts":
            table = self.db.fetch_all_accounts()
            print(table)
            self.wait()
        elif action.get('action') == "Delete an account":
            usrname = input("Enter the account's username:\n\t")
            if self.db.usr_exist(usrname):
                self.db.del_account(usrname)
                cprint('The account has been successfully deleted', 'green')
            else:
                cprint("User doesn't exist", 'red')
            self.wait()

        elif action.get('action') == "Execute SQL command":
            self.sql_terminal()

        elif action.get('action') == "Log out":
            return self.starting()

        elif action.get('action') == "Exit":
            os._exit(1)

        self.admin_program()

    def sql_terminal(self):
        self.clear()
        self.big_text('> SQLite 3', 'yellow')
        cprint('>> To exit type: exit or exit()', 'yellow')
        while True:
            command = input('\n>>> ')
            if command in ['exit', 'exit()']:
                break
            elif command == 'schema':
                output = self.db.exec_sql("select sql from sqlite_master where type = 'table' and name = 'accounts';")
                cprint(output, 'green')
                continue
            try:
                output = self.db.exec_sql(command)
                cprint(output, 'green')
            except sqlite3.OperationalError:
                cprint("Invalid SQL command", 'red')
            self.wait()

    def big_text(self, text, colour):
        cprint(figlet_format(text), colour)

    def clear(self):
        if os.name == "nt":
            os.system('cls')
        else:
            os.system('clear')

    def wait(self):
        if os.name == "nt":
            from msvcrt import getch
            getch()
        else:
            input()


if __name__ == '__main__':
    try:
        colorama.init()
        usr_interface().starting()
    except:
        print('Something went wrong, please contact the developer.')
