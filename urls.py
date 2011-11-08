from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^mgmt/', include(admin.site.urls)),
	(r'^login/', 'res_auth.views.login'),
	(r'^logout/', 'res_auth.views.logout'),
    (r'.*', include('rooms.urls')), # redirect control to rooms app
)
