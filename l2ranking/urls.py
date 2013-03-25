from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.decorators.cache import cache_page

from frontend import views as frontend_views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'l2ranking.views.home', name='home'),
    # url(r'^l2ranking/', include('l2ranking.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', frontend_views.HomeView.as_view(), name='home'),
    url(r'^servers/(?P<page>[0-9]+)?$', frontend_views.ServerListView.as_view(), name='servers'),
    url(r'^server/(?P<pk>\d+)/$', frontend_views.ServerDetailView.as_view(), name='server'),
    url(r'^server/vote/(?P<pk>\d+)/$', frontend_views.ServerVoteView.as_view(), name='vote'),
    url(r'^server/banner/(?P<pk>\d+)/$', 'frontend.views.dynamic_banner', name='dynamic_banner'),
    url(r'^category/(?P<pk>[a-z0-9\-]+)/(?P<page>[0-9]+)?$', frontend_views.CategoryDetailView.as_view(), name='category'),
    url(r'^search/$', frontend_views.SearchView.as_view(), name='search'),

    # News
    url(r'^news/$', frontend_views.NewsListView.as_view(), name='news'),
    url(r'^news/(?P<pk>\d+)/$', frontend_views.NewsDetailView.as_view(), name='news_detail'),

    # Account
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),

    # Media file serve path
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)