from django.contrib.auth import get_user_model
from django.views.generic import CreateView
from django.shortcuts import redirect
from authentication.forms import SignUpForm
from authentication.views.utils import send_activation_mail


User = get_user_model()


class SignUpView(CreateView):
    http_method_names = ['post', 'get']
    template_name = 'sign_up/sign_up.html'
    form_class = SignUpForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        send_activation_mail(user)

        return redirect('authentication:sign-up-info')
