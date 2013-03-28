from django import forms

from frontend import models as frontend_models


class ServerCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = frontend_models.Server
        exclude = ('vote_count', 'in_stat', 'out_stat', 'rating', 'user')