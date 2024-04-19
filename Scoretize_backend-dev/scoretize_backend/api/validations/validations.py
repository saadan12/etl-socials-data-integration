
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

regex_email = r'^([A-Za-z0-9]+[.-_])*[A-Za-z0-9]' + \
              r'+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
regex_password = r'^(?=.*[A-Z])(?=.*[!@#$&*+_-])(?=.*[0-9])(?=.*[a-z]).{8,}$'
regex_name = r'^[A-Za-z][A-Za-z0-9_ -]{1,20}$'
regex_phone = r'^(\+\d{1,3})?,?\s?\d{8,13}'


class Validations:
    # Validation for email
    def email(email):
        if not (re.search(regex_email, email)):
            raise ValidationError(
                _('Email format is not correct.'),
                params={'email': email},
            )

# Validation for password
    def password(password):
        if not (re.search(regex_password, password)):
            raise ValidationError(
                _('Password must have at least one uppercase, '
                  'one lowercase, one numerical digit and '
                  'a character like !@#$&*+_- with a '
                  'minimum length of 8 chars.'),
                params={'password': password},
            )

# Validation for name
    def name(name):
        if not (re.search(regex_name, name)):
            raise ValidationError(
                _('Must have more than 2 chars and less than 20. \
                    Only letters and numbers are permitted'),
                params={'name': name},
            )

# Validation for phone
    def phone(phone):
        if not (re.search(regex_phone, phone)):
            raise ValidationError(
                _('This phone cannot exist'),
                params={'phone': phone},
            )
