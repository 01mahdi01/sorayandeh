from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

import re


def number_validator(password):
    regex = re.compile('[0-9]')
    if regex.search(password) == None:
        raise ValidationError(
                _("password must include number"),
                code="password_must_include_number"
                )

def letter_validator(password):
    regex = re.compile('[a-zA-Z]')
    if regex.search(password) == None:
        raise ValidationError(
                _("password must include letter"),
                code="password_must_include_letter"
                )

def special_char_validator(password):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if regex.search(password) == None:
        raise ValidationError(
                _("password must include special char"),
                code="password_must_include_special_char"
                )



def validate_phone_number(value):
    pattern = r'^09\d{9}$'  # Matches numbers starting with '09' followed by 9 digits
    if not re.match(pattern, value):
        raise ValidationError("Enter a valid phone number.")