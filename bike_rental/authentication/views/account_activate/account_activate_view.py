from django.views.generic import View
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

User = get_user_model()


class ActivateAccountView(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        token = request.GET.get('token')
        user = get_object_or_404(User, verify_token=token, is_active=False)

        user.is_active = True
        user.verify_token = None
        user.save()

        messages.success(request, 'Your account has been successfully activated.')

        return redirect('authentication:sign-in')
