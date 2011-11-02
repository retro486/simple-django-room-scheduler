from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^mgmt/', include(admin.site.urls)),
    (r'.*', include('rooms.urls')), # redirect control to rooms app
)
