from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^mgmt/', include(admin.site.urls)),
	
	(r'^ajax_login/', 'res_auth.views.ajax_login'),
	(r'^ajax_login/', 'res_auth.views.ajax_login'),
	#(r'^ajax_logout/', 'res_auth.views.ajax_logout'),
	
	# the below lines are used primarily for kiosk-style linear functionality
	(r'^ajax_roomkey/', 'roomkeys.views.ajax_get_room'),
	(r'^ajax_roomkey_checkin/', 'rooms.views.ajax_return_key'),
	(r'^ajax_reserve/', 'rooms.views.ajax_reserve'),
	
	# the default calendar view
    (r'^$', 'rooms.views.default_view'),
)
