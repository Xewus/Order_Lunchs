from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordChangeView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path

from .views import SignUp

app_name = 'employees'

urlpatterns = (
    path(
        'signup/', SignUp.as_view(), name='signup'
        ),
    path(
        'logout/',
        LogoutView.as_view(template_name='employees/logout.html'),
        name='logout'
    ),
    path(
        'login/',
        LoginView.as_view(template_name='employees/login.html'),
        name='login'
    ),
    path(
        'password_change/',
        PasswordChangeView.as_view(template_name='employees/password_change.html'),
        name='password_change'
    ),
    path(
        'password_change/done/',
        PasswordChangeDoneView.as_view(template_name='employees/password_change_done.html'),
        name='password_change_done'
    ),
    path(
        'password_reset/',
        PasswordResetView.as_view(template_name='employees/password_reset.html'),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        PasswordResetDoneView.as_view(template_name='employees/password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(template_name='employees/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        PasswordResetCompleteView.as_view(template_name='employees/password_reset_complete.html'),
        name='password_reset_complete'
    ),



)
