from django.conf.urls import patterns, url, include

from usercp import views as usercp_views
from usercp.api import UserResource


urlpatterns = patterns('',
<<<<<<< HEAD
                       url(r'^login/$', 'django.contrib.auth.views.login',
                           name='login'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout',
                           name='logout'),
                       url(r'^register/$', usercp_views.Register.as_view(),
                           name='register'),
                       url(r'^account/$', usercp_views.AccountUpdate.as_view(),
                           name='account'),

                       # Password reset
                       url(r'^password/reset/$',
                           'django.contrib.auth.views.password_reset',
                           {'post_reset_redirect': 'done/'},
                           name='password_reset'),
                       (r'^password/reset/done/$',
                        'django.contrib.auth.views.password_reset_done'),
                       # This should redirect to /usercp/password/done
                       url(r'^password/reset/'
                           r'(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
                           'django.contrib.auth.views.password_reset_confirm',
                           {'post_reset_redirect': '/password/done/'},
                           name='password_confirm'),
                       (r'^password/done/$',
                        'django.contrib.auth.views.password_reset_complete'),)

                       # RESTful authentication
                       # url(r'^api/', include(UserResource().urls)),
                       # url(r'^$', usercp_views.index, name='index'),)
=======
                       url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
                       url(r'^register/$', usercp_views.Register.as_view(), name='register'),
                       url(r'^account/$', usercp_views.AccountUpdate.as_view(), name='account'),

                       # Password reset
                       url(r'^password/reset/$', 'django.contrib.auth.views.password_reset',
                           {'post_reset_redirect': 'done/'}, name='password_reset'),
                       (r'^password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
                       # This should redirect to /usercp/password/done
                       url(r'^password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
                           'django.contrib.auth.views.password_reset_confirm', {'post_reset_redirect': 'done/'},
                           name='password_confirm'),
                       (r'^password/done/$', 'django.contrib.auth.views.password_reset_complete'),
                       )
>>>>>>> origRep/master
