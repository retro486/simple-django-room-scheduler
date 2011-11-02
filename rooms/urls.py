from django.conf.urls.defaults import *
from views import default_view

urlpatterns = patterns('',
    #(r'^/', include('rooms.urls')), # redirect control to rooms app
	(r'^$',default_view),
)
