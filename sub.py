'''class DebitCard():
    def __init__(self):
        pass
    
    def get_name(self):
        alphabet = 'abcdefghijklmnopqrstuvwxyz '
        not_valid = True
        while not_valid:
            name = input('Full Name:\t').lower()
            for letter in name:
                if letter not in alphabet: 
                    print('Only letters are allowed\n')
                    break
            else: not_valid = False
        return name

    def get_dob(self):
        valid = False
        today = date.today().year
        while not valid:
            date_of_birth = input('Date Of Birth(dd/mm/yyyy):\t').split('/')
            try: 
                days, month, year = int(date_of_birth[0]), int(date_of_birth[1]), int(date_of_birth[2])
                valid = (len(date_of_birth) == 3) and (0<days<32) and (0<month<13) and (1900<year<today-2)
                print("Enter Date Of Birth in the given format\n")
            except: print("Enter Date Of Birth in the given format\n")
        age = today-int(date_of_birth[2])
        return [age, f"{days}/{month}/{year}"]

    def get_pin(self):
        nums = '123456789'
        not_valid = True
        while not_valid:
            pin = input('PIN Number:\t')
            for i in pin:
                if i not in nums:
                    print('Only numbers are allowed\n')
                    break
                if len(pin) != 4:
                    print('PIN must be 4 numbers')
                    break
            else: not_valid = False
        return pin
                    
    def run(self):
        # name = self.get_name()
        # print(f'name: {name}')
        # date_of_birth = self.get_dob()
        # print(f'dob: {date_of_birth[1]}')
        pin = self.get_pin()
        print(f'pin: {pin}')

          
    def run(self):
        pass'''

# def __init__(self):
#     self.usrname = ''
#     self.dob = ''
#     self.passwd = b''
#     self.expiry_date = ''
#     self.visa_or_mastercard = ''
#     self.contactless = ''
#     self.card_num = ''

    # self.usrname = self.get_usrname(info.get('forename'), info.get('surname'))
    # self.dob = info.get('date_of_birth')
    # self.passwd = info.get('passwd').encode()
    # self.expiry_date = self.get_expiry_date(info.get('date_of_birth'))
    # self.visa_or_mastercard = info.get('')
    # self.contactless = ''
    # self.card_num = ''


# answers = prompt(questions, style=custom_style_2)
# usrname = answers.get("usrname")
# dob = answers.get("date_of_birth")
# pin = answers.get("pin")


# print(usrname, dob, pin)