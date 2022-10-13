from datetime import date, datetime, timedelta
from PyInquirer import prompt
from validation import *
from examples import custom_style_2
import cipher
from db_related import *
from random import randint


global db
db = DebitCard_db('accounts.db')

def starting():
    starting_q = [{
        'type': 'list',
        'name': 'action',
        'message': 'Welcome',
        'choices': ["Login", "Sign up"]
        }]

    action = prompt(starting_q, style=custom_style_2).get('action')
    if action == 'Login': 
        login()
    elif action == 'Sign up':
        sign_up()
        print("Now u need to log in")
        login()

def login():
    login_q = [{
        'type': "input",
        "name": "usrname",
        "message": "Username:",
        "validate": UsrnameValidator
        },{
        'type': "input",
        "name": "date_of_birth",
        "message": "Date Of Birth:",
        "validate": DateValidator
        },{
        'type': "password",
        "name": "pin",
        "message": "PIN:",
        "validate": NumValidator
        }]
    
    login_info = prompt(login_q, style=custom_style_2)
    if not db.check_passwd(login_info.get('usrname'), login_info.get('passwd')):
        wrong_login_options()
    else:
        access_program()
    
def wrong_login_options():
    options = [{
        'type': 'list',
        'name': 'ans',
        'message': '\n',
        'choices': ["Try again", "Go back"]
        }]
    if options.get('ans') == 'Try again':
        login
    else:
        starting()

def sign_up():
    signup_q = [{
        'type': "input",
        "name": "forename",
        "message": "Forename:",
        "validate": UsrnameValidator
        }, {
        'type': "input",
        "name": "surname",
        "message": "Surname:",
        "validate": UsrnameValidator
        },{
        'type': "input",
        "name": "date_of_birth",
        "message": "Date Of Birth:",
        "validate": DateValidator
        },{
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

    info = prompt(signup_q, style=custom_style_2)
    info['usrname'] = info.get('forename') + '.' + info.get('surname')
    info['expiry_date'] = get_expiry_date(info.get('date_of_birth'))
    info['passwd'] = cipher.encrypt_msg(info.get('passwd'))
    info['card_num'] = get_card_num()

def get_expiry_date( dob):
    dob = datetime.strptime(dob, '%d/%m/%Y').date()
    days_in_30yr = int(365.25*30)
    expiry_date = dob + timedelta(days=days_in_30yr)
    return expiry_date

def get_card_num():
    return randint(1_000_000_000_000_000,9_999_999_999_999_999)


def can_make_card( expiry_date):
    today = date.today()
    if today > expiry_date:
        return False
    else:
        return True

def access_program():
    pass

def run():
    starting()

#
    