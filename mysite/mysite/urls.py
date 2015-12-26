#-*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from teachertree import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', views.login),
    (r'^searchteacher/$', views.searchteacher),
    (r'^searchstudent/$', views.searchstudent),
    (r'^buildteacher/p1(\d+)/$', views.buildteacher),
    (r'^buildstudent/p1(\d+)/$', views.buildstudent),
    (r'^searchre/$', views.se_re),
    (r'^search_relation/p1(\d+)/$', views.search_relation),
    (r'^delete/$', views.deletedetail),
    (r'^deletestudent/p1(\d+)/$', views.deletestudent),
    (r'^deleteteacher/p1(\d+)/$', views.deleteteacher),
    url(r'^update/$',views.update),
    url(r'^login/$',views.login),
    url(r'^regist/$',views.CreUser),
    url(r'^index/$',views.index),
    url(r'^logout/$',views.logout),
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
