# Debit Card CLI


Debit Card CLI is simple abstraction of what an interactive Debit Card CLI would look like without caring too much about server side requests. The program Written in python and SQL lite library.

## Features
![Image](https://github.com/AhmedBlackEye/DebitCard/blob/main/Debitcard.jpg?raw=true)
- Accounts are saved in a local DB to remember users
- Instant and interactive validations
- Card Number checker based on Luhn algorithm
- Admin account where accounts can be managed(_Default PIN is 0000_)
- Password Encryption
## Tech

Debit Card CLI uses a number of open source python libraries to work properly:

- cryptography
- sqlite3
- validation
- PyInquirer
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
