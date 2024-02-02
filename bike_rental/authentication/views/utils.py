from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import reverse


def send_activation_mail(user):
    """
    Sends an activation email to a newly registered user.
    :param user: The user object for whom the activation email is being sent.
    """
    token = default_token_generator.make_token(user)
    uidb64 = urlsafe_base64_encode(force_str(user.pk).encode())

    activation_url = reverse(
        'authentication:activate-account', kwargs={'uidb64': uidb64, 'token': token}
    )

    activation_url = f'{settings.BASE_URL}{activation_url}'

    send_mail(
        subject='Account Activation Code',
        message=f'''
        Hello {user.first_name},
        
        Welcome to DnD motorcycles family!
        Here is your activation link: {activation_url}
        
        Best Regards
        DnD Motorcycles Team
        ''',
        from_email=settings.EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
