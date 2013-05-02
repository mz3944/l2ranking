from django.contrib.auth.models import User

from tastypie.resources import ModelResource, ALL
from tastypie import fields

from frontend import models as frontend_models


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['username', 'id']
        filtering = {
            'username': ALL
        }


class CategoryResource(ModelResource):
    class Meta:
        queryset = frontend_models.Category.objects.all()
        resource_name = 'category'


class ServerResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = frontend_models.Server.objects.all()
        resource_name = 'server'
        fields = ['name', 'id', 'description', 'banner', 'rating', 'last_rank', 'create_date', 'vote_count']
        ordering = ['create_date', 'vote_count']
        filtering = {
            'name': ALL,
            'id': ALL,
        }


class NewsResource(ModelResource):
    class Meta:
        queryset = frontend_models.News.objects.all()
        resource_name = 'news'
        ordering = ['create_date']


class ReviewResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    name = fields.CharField(attribute='server')

    class Meta:
        queryset = frontend_models.Review.objects.all()
        resource_name = 'review'
        ordering = ['create_date']
        filtering = {
            'id': ALL,
            'name': ALL
        }
