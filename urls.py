from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^mgmt/', include(admin.site.urls)),
	(r'^login/', 'res_auth.views.login'),
	(r'^ajax_login/', 'res_auth.views.ajax_login'),
	(r'^logout/', 'res_auth.views.logout'),
	(r'^ajax_logout/', 'res_auth.views.ajax_logout'),
    (r'.*', include('rooms.urls')), # redirect control to rooms app
)
