from django.db import models
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

from l2ranking import settings as l2ranking_settings


class BannerField(models.ImageField):
    """
    Banner image field with size validation
    """

    description = "Banner image field with size validation"
    __metaclass__ = models.SubfieldBase

    def clean(self, *args, **kwargs):
        banner = super(BannerField, self).clean(*args, **kwargs)
        if banner:
            width, heigth = get_image_dimensions(banner)
            if banner._size > l2ranking_settings.BANNER_SIZE * 1024:
                raise ValidationError(
                    "Banner file too large ( > " + str(l2ranking_settings.BANNER_SIZE) + " kb )")
            if width > l2ranking_settings.BANNER_WIDTH:
                raise ValidationError("Banner too wide ( > " + str(l2ranking_settings.BANNER_WIDTH) + " px )")
            if heigth > l2ranking_settings.BANNER_HEIGHT:
                raise ValidationError(
                    "Banner too high (no pun, lol) ( > " + str(l2ranking_settings.BANNER_HEIGHT) + " px )")
            return banner
        else:
            raise ValidationError("Couldn't read the uploaded banner")