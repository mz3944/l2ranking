from django import forms
from captcha.fields import ReCaptchaField

from frontend import models as frontend_models

class SearchForm(forms.Form):
    pass

class VoteForm(forms.Form):
    character = forms.CharField(max_length=80)
    captcha = ReCaptchaField()

class ReviewForm(forms.ModelForm):
    class Meta:
        model = frontend_models.Review
        exclude = ('server', 'user',)