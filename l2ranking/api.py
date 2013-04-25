#l2ranking/l2ranking/api.py
from django.contrib.auth.models import User
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from frontend.models import Category, News, Review, Server

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name ='user'
        excludes = ['password','email','is_staff','is_supervisor']
        filtering = {
            'username': ALL
        }

class CategoryResource(ModelResource):
    class Meta:
        queryset = Category.objects.all()
        resource_name = 'category'

class NewsResource(ModelResource):
    class Meta:
        queryset = News.objects.all()
        resource_name = 'news'

class ReviewResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    class Meta:
        queryset = Review.objects.all()
        resource_name = 'review'
        filtering = {
            'id': ALL,
        }

class ServerResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    class Meta:
        queryset = Server.objects.all()
        resource_name = 'server'
        fields = ['name','id','description','banner','rating','last_rank']
        filtering = {
            'name': ALL,
            'id': ALL
        }

class TopFiveResource(ModelResource):
    class Meta:
        queryset = Server.objects.all().order_by('-vote_count')[:5]
        resource_name = 'top_five'
        fields = ['name']


class LatestFiveResource(ModelResource):
    class Meta:
        queryset = Server.objects.all().order_by('-create_date')[:5]
        resource_name = 'latest_five'
        fields = ['name']