from django.conf.urls import patterns, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
from teachertree.views import person,addteacher,addstudent,search,deletestudent,deleteteacher

urlpatterns = patterns('',
    url(r'^$',person),
    url(r'^addteacher/p1(\d+)/$',addteacher),
    url(r'^addstudent/p1(\d+)/$',addstudent),
    url(r'^search/$',search),
    url(r'^deletestudent/p1=(\d+)p2=(\w+)/$',deletestudent),
    url(r'^deleteteacher/p1=(\d+)p2=(\w+)/$',deleteteacher),
)