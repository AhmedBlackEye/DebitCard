import sqlite3
from cipher import *


class Database:

    def __init__(self, name):
        self.db_name = name

    def create_connection(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
        except sqlite3.Error as e:
            print(e)
        return conn, c


class DebitCard_db(Database):

    def create_db(self):
        table = """CREATE TABLE accounts (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        visa_or_mastercard TEXT,
        contactless TEXT,
        card_number TEXT,
        date_of_birth TEXT,
        expiry_date TEXT,
        password TEXT,
        money INTERGER
        );"""

        encr_pin = encrypt_('0000').decode()
        exec = f"""INSERT INTO accounts(username, password)
            VALUES('admin', '{encr_pin}') """
        conn, c = self.create_connection()
        c.execute(table)
        c.execute(exec)
        conn.commit()
        conn.close()

    def add_account(self, account):
        conn, c = self.create_connection()
        exec = f"""INSERT INTO accounts(
            username, visa_or_mastercard , contactless, card_number,
            date_of_birth, expiry_date, password, money)
            VALUES(
            "{account.get('usrname')}", "{account.get('card_type')}", "{account.get('contactless')}",
            "{account.get('card_num')}","{account.get('date_of_birth')}", "{account.get('expiry_date')}", "{account.get('passwd')}\", 1000) """
        c.execute(exec)
        conn.commit()
        conn.close

    def del_account(self, usrname):
        conn, c = self.create_connection()
        exec = f"""DELETE FROM accounts
            WHERE username = "{usrname}\" """
        c.execute(exec)
        conn.commit()
        conn.close

    def change_money(self, usrname, money_value, added_or_withdrawed):
        conn, c = self.create_connection()
        if added_or_withdrawed == 'add': sign = '+'
        elif added_or_withdrawed == 'withdraw': sign = '-'
        exec = f'''UPDATE accounts
            SET money = money{sign}{money_value}
            WHERE username = "{usrname}"; '''
        c.execute(exec)
        conn.commit()
        conn.close

    def get_money_amount(self, usrname):
        conn, c = self.create_connection()
        exec = f'''SELECT money 
            FROM accounts
            WHERE username = "{usrname}" '''
        c.execute(exec)
        money = c.fetchone()
        conn.commit()
        conn.close
        return money[0]

    def fetch_all_accounts(self):
        conn, c = self.create_connection()
        exec = f"""SELECT * FROM accounts"""
        c.execute(exec)
        accounts = c.fetchall()
        conn.commit()
        conn.close()
        columns = f"{'ID':8} {'Username':18} {'Card Number':18} {'Expiry Date':12} {'Money'}\n"
        output =  columns + '-'*len(columns) + '\n'
        for account in accounts[1:]:
            output += f"{str(account[0]):8} {account[1]:18} {account[4]:18} {account[6]:12} {account[8]}\n"

        return output

    def exec_sql(self, exec):
        conn, c = self.create_connection()
        c.execute(exec)
        output = c.fetchall()
        conn.commit()
        conn.close()
        return output

    def usr_exist(self, usrname):
        conn, c = self.create_connection()
        exec = f'''SELECT username
            FROM accounts
            WHERE username = "{usrname}" '''
        c.execute(exec)
        output = c.fetchall()
        conn.commit()
        conn.close
        if output: return True
        else: return False

    def check_passwd(self, usrname, given_passwd):
        conn, c = self.create_connection()
        exec = f'''SELECT password 
            FROM accounts
            WHERE username = "{usrname}"'''
        c.execute(exec)
        db_passwd = c.fetchone()[0]
        conn.commit()
        conn.close()
        db_passwd = decrypt_(db_passwd)
        return db_passwd == given_passwd


if __name__ == '__main__':
    db = DebitCard_db('accounts.db')
    db.create_db()