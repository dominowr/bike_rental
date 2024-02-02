import re
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _


class PasswordValidator:
    error_messages = {
        'password_mismatch': _('The two password fields did not match.'),
        'invalid_password': _('Password must be at least 8 characters long and contain at least one uppercase letter, '
                              'one digit, and one special character.'),
        'email_used': _('This email is already in use.'),
    }

    @staticmethod
    def clean_password(password):
        """
        Validates the provided password based on specific criteria.
        :param password: The password to be validated.

        Raises:
            - ValidationError: If the password does not meet the specified criteria.
        """
        regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'

        if not re.match(regex, password):
            raise ValidationError(
                PasswordValidator.error_messages['invalid_password'],
                code='invalid_password'
            )
        return password

    @staticmethod
    def clean_password2(password1, password2):
        """
        Validates that two provided passwords match.
        :param password1: The first password.
        :param password2: The second password.

        Raises:
            - ValidationError: If the passwords do not match.
        """
        if password1 != password2:
            raise ValidationError(
                PasswordValidator.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
