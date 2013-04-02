from django.db import models
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

from l2ranking import settings


class BannerField(models.ImageField):
    """
    Banner image field with size validation
    """

    description = "Banner image field with size validation"

    def clean(self, *args, **kwargs):
        data = super(BannerField, self).clean(*args, **kwargs)
        banner = data.file
        if banner:
            width, heigth = get_image_dimensions(banner)
            if banner._size > settings.BANNER_SIZE * 1024:
                raise ValidationError(
                    "Banner file too large ( > " + str(settings.BANNER_SIZE) + " kb )")
            if width > settings.BANNER_WIDTH:
                raise ValidationError("Banner too wide ( > " + str(settings.BANNER_WIDTH) + " px )")
            if heigth > settings.BANNER_HEIGHT:
                raise ValidationError(
                    "Banner too high (no pun, lol) ( > " + str(settings.BANNER_HEIGHT) + " px )")
        else:
            raise ValidationError("Couldn't read the uploaded banner")
        return data