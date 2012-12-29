from django.conf.urls.defaults import patterns, include, url
from memestat.views import hello

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('', ('^hello/$', hello), ('^$', hello),
    # Examples:
     url(r'^$', 'memestat.views.home', name='hello'),
    # url(r'^memestat/', include('memestat.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
