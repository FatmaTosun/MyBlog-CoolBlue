from django.conf.urls import patterns, include, url
from BlogApplication.views import index
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', index, name='home'),

    # url(r'^BlogApplication/', include('BlogApplication.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^account/', include('account.urls')),
    url(r'^post/', include('post.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
