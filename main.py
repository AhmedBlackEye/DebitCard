from datetime import date, datetime, timedelta
from PyInquirer import prompt
from validation import *
from examples import custom_style_2
from cipher import *
from db_related import *


questions = [
    {
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


def usr_interface():
    info = prompt(questions, style=custom_style_2)
    info['usrname'] = info.get('forename') + '.' + info.get('surname')
    info['expiry_date'] = get_expiry_date(info.get('date_of_birth'))
    info['passwd'] = cipher.encrypt_msg(info.get('passwd'))
    info['card_num'] = get_card_num()


def get_expiry_date(dob):
    dob = datetime.strptime(dob, '%d-%m-%Y').date()
    days_in_30yr = int(365.25*30)
    expiry_date = dob + timedelta(days=days_in_30yr)
    return expiry_date

def get_card_num():
    pass


def can_make_card(expiry_date):
    today = date.today()
    if today > expiry_date:
        print(1)
    else:
        print(0)

def login(usrname, passwd):
    encr_passwd = cipher().encrypt_msg(passwd)
    db = DebitCard_db('accounts.db')
    if db.check_passwd(usrname, encr_passwd):
        print('0')
    else: print(1)

login('ahmed.elsayed', '134')