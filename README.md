# Debit Card CLI


A Debit Card CLI is a simple abstraction of what an interactive debit card CLI would look like without caring much about server-side or handling requests. The program is written in the Python library and SQLite3.

## Features
![Image](https://github.com/AhmedBlackEye/DebitCard/blob/main/Debitcard.jpg?raw=true)
- Accounts are saved in a local DB to remember users
- Instant and interactive validations
- Card Number checker based on Luhn algorithm
- Admin account where accounts can be managed(_Default PIN is 0000_)
- Password Encryption
## Tech

Debit Card CLI uses a number of open source python libraries to work properly:

- PyInquirer
- Termcolor
- Pyfiglet
- etc..

## Installation

Debit Card CLI requires Python v3+ to run.

```sh
git clone https://github.com/AhmedBlackEye/DebitCard
cd DebitCard
python main.py
```

## Developers
- [Ahmed Elsayed](https://github.com/AhmedBlackEye)

# License

### **MIT**


 
