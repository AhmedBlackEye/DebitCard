from PyInquirer import prompt
from examples import custom_style_2
from prompt_toolkit.validation import Validator, ValidationError

class TheValidator(Validator):
    
    def validate_usrname(self, document):
        alphabet = 'abcdefghijklmnopqrstuvwxyz '
        name = input('Full Name:\t').lower()
        for letter in name:
            if letter not in alphabet: 
                raise ValidationError(message="Only letters are allowed", cursor_position=len(document.text))

options = [
    {
        'type': 'list',
        'name': 'command',
        'message': 'Welcome to Debit Card CLI',
        'choices': ["Access debit card account","Create debit card account","Delete debit card account"]
    },
    {
        'type': "input",
        "name": "a",
        "message": "Name",
        "validate": TheValidator,
    },]

x  = prompt(options, style=custom_style_2)
y = options.get('a')
print(y)
print(x.get('command'))