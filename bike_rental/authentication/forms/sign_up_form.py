from django.forms import ModelForm, CharField, ValidationError, PasswordInput
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .utils import PasswordValidator

User = get_user_model()


class SignUpForm(ModelForm):

    error_messages = {
        'email_used': _('This email is already in use.'),
    }

    password2 = CharField(label='Password confirmation',
                          widget=PasswordInput,
                          )

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'phone_no', 'email', 'password',
        ]
        widgets = {
            'password': PasswordInput
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return PasswordValidator.clean_password(password)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        return PasswordValidator.clean_password2(password1, password2)

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise ValidationError(
                self.error_messages['email_used'],
                code='email_used',
            )
        return email
