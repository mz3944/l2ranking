from django import forms
from captcha.fields import ReCaptchaField

class SearchForm(forms.Form):
    pass

class VoteForm(forms.Form):
    character = forms.CharField(max_length=80)
    captcha = ReCaptchaField()