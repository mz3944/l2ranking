from django import forms
from captcha.fields import ReCaptchaField

from frontend import models as frontend_models


class SearchForm(forms.Form):
    pass


class VoteForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = frontend_models.Vote
        exclude = ('server', 'ip_address',)


class ReviewForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = frontend_models.Review
        exclude = ('server', 'user',)