from django.contrib.auth.forms import SetPasswordForm
from .utils import PasswordValidator


class CustomPasswordResetForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['new_password1'].label = 'New Password:'
        self.fields['new_password2'].label = 'Password confirmation:'

    def clean_password(self):
        password = self.cleaned_data.get('new_password1')
        return PasswordValidator.clean_password(password)

    def clean_password2(self):
        password1 = self.cleaned_data('new_password1')
        password2 = self.cleaned_data('new_password2')
        return PasswordValidator.clean_password2(password1, password2)
