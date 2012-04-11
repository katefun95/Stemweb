from django.conf.urls.defaults import patterns, include, url
import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^', include('home.urls')),
	(r'^files/', include('files.urls')),
	(r'^algorithms/', include('algorithms.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}, name='stemweb_media_root_url'),
    
    # These are the registration apps own urls. Check documentation for the usage.
    # https://bitbucket.org/ubernostrum/django-registration/src/tip/docs/quickstart.rst
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
