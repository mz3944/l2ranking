from django.conf.urls import patterns, url

from usercp import views as usercp_views

urlpatterns = patterns('',
                       url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
                       url(r'^register/$', usercp_views.Register.as_view(), name='register'),
)