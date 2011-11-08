from rooms.models import NPSUser
from sip2talk import auth_card
from django.http import HttpResponseRedirect
import sys
from django.template import RequestContext
from django.core.context_processors import csrf
from forms import LoginForm
from django.shortcuts import render_to_response
import urllib2
from django.conf import settings

'''
Ideally this would use SIP2, but our internal SIP2 server is heavily locked down and
to gain access would require much paperwork, so for now we confirm the validity of
a user's barcode (and obtain their email address) via a slightly modified VuFind
driver.pl script running on the Sirsi server as http://biblio/vufind/
'''
def login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		auth = True
		if form.is_valid():
			try:
				response = urllib2.urlopen(settings.RES_BARCODE_URL+form.cleaned_data['barcode'])
				message = response.read()
				if len(message) == 0:
					raise Exception('Invalid barcode.')
					
			except Exception as ex:
				# authentication failure
				auth = False
				message = 'Error: ' + str(ex)
			
			if auth:
				# tack on the email to the current session and foward to the calendar form
				request.session['email'] = message.split('|')[0]
				return HttpResponseRedirect('/')
				
			else:
				# invalid barcode was provided
				ret = RequestContext(request, {
					'auth': message,
					'form': form,
				})
				
				return render_to_response(settings.RES_LOGIN_TEMPLATE, ret)
		
		else:
			c = RequestContext(request,{
				'form': form,
			})
			c.update(csrf(request))
			
			return render_to_response(settings.RES_LOGIN_TEMPLATE, c)
			
	else:
		# don't allow access to this view directly
		return HttpResponseRedirect('/')
		
def logout(request):
	request.session['email'] = False
	return HttpResponseRedirect('/')