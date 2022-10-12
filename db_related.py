import sqlite3

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
        conn, c = self.create_connection()
        c.execute(table)
        c.execute(f"""INSERT INTO accounts(username, password)
            VALUES("admin.admin", "0000") """)
        conn.commit()
        conn.close

    def add_account(self, account):
        conn, c = self.create_connection()
        c.execute(f"""INSERT INTO accounts(
            username, visa_or_mastercard , contactless, card_number,
            date_of_birth, expiry_date, password, money
            )
            VALUES(
            "{account.get('usrname')}", "{account.get('visa_or_mastercard')}", "{account.get('contactless')}",
            "{account.get('card_num')}","{account.get('dob')}", "{account.get('expiry_date')}", "{account.get('passwd')}", 1000
            ) """)
        conn.commit()
        conn.close
    
    def del_account(self, usrname):
        conn, c = self.create_connection()
        c.execute(f"""DELETE FROM accounts
            WHERE username = "{usrname}" """)
        conn.commit()
        conn.close

    def change_money(self, usrname, money_value, added_or_withdrawed):
        conn, c = self.create_connection()
        if added_or_withdrawed == 'add': sign = '+'
        elif added_or_withdrawed == 'withdraw': sign = '-'
        c.execute(f"""UPDATE accounts
            SET money = money{sign}{money_value}
            WHERE username = "{usrname}";""")
        conn.commit()
        conn.close

    def get_money_amount(self, usrname):
        conn, c = self.create_connection()
        c.execute(f"""SELECT money 
            FROM accounts
            WHERE username = "{usrname}" """)
        money = c.fetchone()
        conn.commit()
        conn.close
        return money[0]
    
    def fetch_all_accounts(self):
        conn, c = self.create_connection()
        c.execute(f"""SELECT *
            FROM accounts""")
        accounts= c.fetchall()
        conn.commit()
        conn.close
        return accounts[1:]

    def exec_sql(self, command):
        conn, c = self.create_connection()
        c.execute(command)
        output = c.fetchall()
        conn.commit()
        conn.close
        return output
    
    def usr_exist(self, usrname):
        conn, c = self.create_connection()
        c.execute(f"""SELECT username
            FROM accounts
            WHERE username = "{usrname}" """)
        output = c.fetchall()
        conn.commit()
        conn.close
        if output: return True
        else: return False
    
    def check_passwd(self, usrname, passwd):
        conn, c = self.create_connection()
        c.execute(f"""SELECT password 
            FROM accounts
            WHERE username = "{usrname}" """)
        real_passwd = c.fetchone()[0]
        conn.commit()
        conn.close
        if real_passwd == passwd: 
            print(real_passwd)
            print(passwd)
            return True
        else: return False


db = DebitCard_db('accounts.db')
# db.create_db()
# db.add_account('omar elsayed', '23/8/2012', 'mastercard', 'false', '1234567812345678', '2345')
# db.del_account('ahmed elsayed')
# db.change_money('ahmed elsayed', 700, 'withdraw')
# print(db.fetch_all_accounts())
# print(db.exec_sql("""UPDATE accounts
#             SET money = money+300
#             WHERE username = "omar elsayed";"""))
# print(db.usr_exist('admin'))
# print(db.usr_exist('ahmed'))

            # username, visa_or_mastercard , contactless, card_number,
            # date_of_birth, expiry_date, password, money

account = {
    'usrname': 'ahmed.elsayed',
    'visa_or_mastercard': 'visa',
    'contactless': 'True',
    'card_num': '1234567812345678',
    'dob': '20/11/2005',
    'expiry_date': '30/4/2008',
    'passwd': '1234'
}

# db.add_account(account)

# print(db.check_passwd('ahmed.elsayed', '1234'))