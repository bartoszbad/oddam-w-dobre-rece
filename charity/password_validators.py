import re

from django.core.exceptions import ValidationError


def number_validator(password):
    if not re.findall('\d', password):
        raise ValidationError("Hasło musi zawierać przynajmniej 1 cyfrę, 0-9.")


def uppercase_validator(password):
    if not re.findall('[A-Z]', password):
        raise ValidationError("Hasło musi zawierać przynajmniej 1 dużą literę, A-Z.")


def lowercase_validator(password):
    if not re.findall('[a-z]', password):
        raise ValidationError("Hasło musi zawierać przynajmniej 1 małą literę, a-z.")


def symbol_validator(password):
    if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
        raise ValidationError("Hasło musi zawierać przynajmniej 1 symbol: " + "()[]{}|`~!@#$%^&*_-+=;:',<>./?")


def length_validator(password):
    if len(password) < 8:
        raise ValidationError("Hasło musi zawierać przynajmniej 8 znaków")


def validators(password):
    length_validator(password)
    number_validator(password)
    uppercase_validator(password)
    lowercase_validator(password)
    symbol_validator(password)