from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from servercp import views as servercp_views

urlpatterns = patterns('',
                       url(r'^list/$', login_required(servercp_views.ServerListView.as_view()), name='servers'),
                       url(r'^add/$', login_required(servercp_views.ServerAddView.as_view()), name='server_add'),
                       url(r'^edit/(?P<pk>\d+)/$', login_required(servercp_views.ServerUpdateView.as_view()),
                           name='server_update'),
                       url(r'^delete/(?P<pk>\d+)/$', login_required(servercp_views.ServerDeleteView.as_view()),
                           name='server_delete'),
                       url(r'^statistics/(?P<pk>\d+)/$', login_required(servercp_views.ServerStatisticsView.as_view()),
                           name='server_stats'),
                       )