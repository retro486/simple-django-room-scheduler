from rooms.models import NPSUser
from sip2talk import auth_card
from django.http import HttpResponseRedirect,HttpResponse
import sys
from django.template import RequestContext
from django.core.context_processors import csrf
from forms import LoginForm
from django.shortcuts import render_to_response
import urllib2
from django.conf import settings
import json

'''
Ideally this would use SIP2, but our internal SIP2 server is heavily locked down and
to gain access would require much paperwork, so for now we confirm the validity of
a user's barcode (and obtain their email address) via a slightly modified VuFind
driver.pl script running on the Sirsi server as http://biblio/vufind/

Returns a dictionary with keys:
  * auth: True if user was validated, False if they were not.
  * message: will contain the email of the user if auth is True, otherwise it will contain the raw
			return value from the auth server.
  * error: if auth is False, this will contain an explanation.
'''
def bare_login(barcode):
	ret = {
		'auth': True,
		'message': '',
		'error': '',
	}
	message = ''
	
	try:
		response = urllib2.urlopen(settings.RES_BARCODE_URL + barcode)
		message = response.read()
		if len(message) == 0:
			ret['auth'] = False
			ret['error'] = 'Invalid barcode or email not in system. Please see the circulation desk for assistance.'
			
	except Exception as ex:
		# authentication failure
		ret['auth'] = False
		ret['error'] = 'Please report the following message to the circulation desk: ' + str(ex)
	
	if ret['auth']:
		ret['message'] = message.split('|')[0] # extract the email
	else:
		ret['message'] = message # just forward whatever you got, likely nothing if an exception hit
	
	return ret
		
# POST method of login with form
def login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		
		if form.is_valid():
			result = bare_login(form.cleaned_data['barcode'])
			
			if result['auth']:
				request.session['email'] = result['message']
				return HttpResponseRedirect('/')
				
			else:
				# invalid barcode was provided
				ret = RequestContext(request, {
					'auth': result['error'],
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
	
# the following are ajax versions of the above functions. they do not return forwarding requests,
# only json responses.

def ajax_login(request):
	# ensure this wasn't a post attempt
	if request.method == 'GET':
		result = bare_login(request.GET.get('barcode', '0'))
		
		# TODO need to implement anti-css?
		return HttpResponse(json.dumps(result))
		
	else:
		return HttpResponse(json.dumps(False))
		
def ajax_logout(request):
	# ensure this wasn't a POST attempt
	if request.method == 'GET':
		request.session['email'] = False
		return HttpResponse(json.dumps(True))
		
	else:
		return HttpResponse(json.dumps(False))