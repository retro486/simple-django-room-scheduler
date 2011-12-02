from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^mgmt/', include(admin.site.urls)),
    
    (r'^ajax_login/', 'rooms.views.ajax_login'),
    (r'^ajax_roomkey/', 'rooms.views.ajax_get_room'),
    (r'^ajax_roomkey_checkin/', 'rooms.views.ajax_return_key'),
    (r'^ajax_reserve/', 'rooms.views.ajax_reserve'),
    
    # the default calendar view
    (r'^$', 'rooms.views.default_view'),
)
