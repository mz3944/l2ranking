from django import forms
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

from frontend import models as frontend_models
from l2ranking import settings as l2ranking_settings


class ServerForm(forms.ModelForm):
    """
    Form used for user to add or update server.
    """

    class Meta:
        model = frontend_models.Server
        exclude = ('vote_count', 'in_stat', 'out_stat', 'rating', 'user', 'last_rank')

    def clean_banner(self):
        banner = self.cleaned_data.get('banner', False)
        if banner:
            width, heigth = get_image_dimensions(banner)
            if banner._size > l2ranking_settings.BANNER_SIZE * 1024:
                raise ValidationError(
                    "Banner file too large ( > " + str(l2ranking_settings.BANNER_SIZE) + " kb )")
            if width > l2ranking_settings.BANNER_WIDTH:
                raise ValidationError("Banner too wide ( > " + str(l2ranking_settings.BANNER_WIDTH) + " px )")
            if heigth > l2ranking_settings.BANNER_HEIGHT:
                raise ValidationError(
                    "Banner too high (no pun, lol p: ) ( > " + str(l2ranking_settings.BANNER_HEIGHT) + " px )")
            return banner
        else:
            raise ValidationError("Couldn't read the uploaded banner")