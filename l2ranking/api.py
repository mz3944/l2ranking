#l2ranking/l2ranking/api.py
from tastypie.resources import ModelResource
from frontend.models import Category
from frontend.models import News
from frontend.models import Review
from frontend.models import Server
from frontend.models import Vote

class CategoryResource(ModelResource):
    class Meta:
        queryset = Category.objects.all()
        resource_name = 'category'

class NewsResource(ModelResource):
    class Meta:
        queryset = News.objects.all()
        resource_name = 'news'

class ReviewResource(ModelResource):
    class Meta:
        queryset = Review.objects.all()
        resource_name = 'review'

class ServerResource(ModelResource):
    class Meta:
        queryset = Server.objects.all()
        resource_name = 'server'

class VoteResource(ModelResource):
    class Meta:
        queryset=Vote.objects.all()
        resource_name = 'vote'
