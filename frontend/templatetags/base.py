from django.template import Library

from frontend import models as frontend_models

register = Library()

@register.inclusion_tag('frontend/categories.html')
def categories():

    categories = frontend_models.Category.objects.all()

    return {
        'category_list': categories,
    }