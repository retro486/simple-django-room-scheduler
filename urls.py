from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^mgmt/', include(admin.site.urls)),
	(r'^ajax_login/', 'res_auth.views.ajax_login'),
	(r'^ajax_logout/', 'res_auth.views.ajax_logout'),
	(r'^ajax_roomkey/', 'roomkeys.views.ajax_get_room'),
	(r'^ajax_roomkey_checkin/', 'roomkeys.views.ajax_checkin'),
	(r'^ajax_reserve/', 'rooms.views.ajax_reserve'),
    (r'.*', include('rooms.urls')), # redirect control to rooms app
)
