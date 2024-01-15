from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm
from .views import SignUpView, SignUpInfoView, ActivateAccountView

app_name = 'authentication'
urlpatterns = [
    path('sign-in/', auth_views.LoginView.as_view(template_name='sign_in/sign_in.html'), name='sign-in'),
    path('sign-out/', auth_views.LogoutView.as_view(), name='sign-out'),
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('sign-up/activate-account/<str:uidb64>/<str:token>/', ActivateAccountView.as_view(), name='activate-account'),
    path('sign-up/info/', SignUpInfoView.as_view(), name='sign-up-info'),
    path(
        'password-reset/', auth_views.PasswordResetView.as_view(
            template_name='password_reset/reset.html', email_template_name='password_reset/reset_email.html',
            success_url=reverse_lazy('authentication:password-reset-done')

        ),
        name='password-reset'
    ),
    path(
        'password-reset/done/', auth_views.PasswordResetDoneView.as_view(
            template_name='password_reset/done.html'
        ),
        name='password-reset-done'
    ),
    path(
        'password-reset-confirm/<str:uidb64>/<str:token>/', auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset/confirm.html',
            success_url=reverse_lazy('authentication:password-reset-complete'),
            form_class=CustomPasswordResetForm
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done', auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset/complete.html'
        ),
        name='password-reset-complete'
    ),
]
