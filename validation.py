from prompt_toolkit.validation import Validator, ValidationError

def raise_err(msg, position):
    raise ValidationError(
        message=msg, 
        cursor_position=position
    )

class NumValidator(Validator):        
    def validate(self, document):
        if not document.text.isdigit():
            raise_err("Only numbers are allowed", len(document.text))
        elif not 0<len(document.text)<5:
            raise_err("PIN must contain 4 numbers", len(document.text))


class UsrnameValidator(Validator):
    def validate(self, document):
        alphabet = 'abcdefghijklmnopqrstuvwxyz '
        for letter in document.text:
            if letter not in alphabet: 
                raise_err("Only lowercase letters are allowed", len(document.text))

        
class DateValidator(Validator):
    def validate(self, document):
        from datetime import date
        current_yr = date.today().year
        try:
            days, month, year = document.text.split('-')
            days, month, year = int(days), int(month), int(year)
        except: 
            raise_err("Enter Date in dd/mm/yyyy format", len(document.text))
        if not (1900<year<current_yr-2 and 0<days<32 and 0<month<13):
            raise_err(f"Year must be between 1900 and {current_yr-2} with realistic values", len(document.text))