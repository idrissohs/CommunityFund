from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^blank/$', views.blank, name='blank'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^funder/$', views.funder, name='funder'),
    url(r'^initiator/$', views.initiator, name='initiator'),
    url(r'^fundproject/(?P<pk>[0-9]+)/$', views.fund_project, name='fund_project'),
)
