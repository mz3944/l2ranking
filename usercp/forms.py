from django.contrib.auth import forms as auth_forms

from captcha.fields import ReCaptchaField


class RegisterForm(auth_forms.UserCreationForm):
    """
    Extends build-in user creation form.
    """

    captcha = ReCaptchaField()