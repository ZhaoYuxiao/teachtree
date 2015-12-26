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
    (r'^ssf/$', views.search_schoolfellow),
    (r'^se_date/$', views.search_date),
    url(r'^update/$',views.update),
    url(r'^login/$',views.login),
    url(r'^regist/$',views.CreUser),
    url(r'^index/$',views.index),
    url(r'^logout/$',views.logout),
    url(r'^query/p(\d+)/$',views.query),
    url(r'^query2/$',views.query2),
    url(r'^searchperson/$',views.searchperson),
    url(r'^queryothers/p1(\d+)p(\d+)/$',views.queryothers),
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()