from django.template import RequestContext
from django.core.context_processors import csrf
from res_auth.forms import LoginForm
from django.shortcuts import render_to_response
from datetime import datetime,timedelta
from models import Reservation,Room,NPSUser
from roomkeys.models import RoomKey
from django.conf import settings
from django.http import HttpResponseRedirect,HttpResponse
import json

def default_view(request):
	dt_start = datetime.now()
	fix1 = timedelta(minutes=dt_start.minute % settings.RES_MIN_LENGTH, seconds=dt_start.second,
	  microseconds=dt_start.microsecond) # zero out seconds
	dt_start -= fix1 # round down to nearest increment of 15 minutes

	email = request.session.get('email', False)
	
	times = []
	rooms = []

	if settings.RES_SWAP_AXIS:
		# this bit is confusing because of naming; TODO change naming to be less confusing.
		for i in range(0,17):
			t = dt_start + timedelta(minutes=i*settings.RES_MIN_LENGTH)
			times.append(':'.join(t.time().isoformat().split(':')[0:2]))
		
		for room in Room.objects.all():
			rooms.append([])
			rooms[-1].append(room.name)
			
			for i in range(0,len(times)):
				dts = dt_start + timedelta(minutes=(settings.RES_MIN_LENGTH*i)) 
				try:
					cur = Reservation.objects.get(
						room=room,
						datetime_start__lte=dts,
						datetime_end__gte=dts,
					)
				except:
					cur = None

				if cur is None:
					rooms[-1].append((0,True,room.pk))
				else:
					if email and cur.requested_user.email == email:
						editable = True
					else:
						editable = False
					rooms[-1].append((cur.type,editable,room.pk))

	else:
		for i in range(0,17):
			t = dt_start + timedelta(minutes=i*settings.RES_MIN_LENGTH)
			times.append(':'.join(t.time().isoformat().split(':')[0:2]))

		for room in Room.objects.all():
			r = []
			r.append(room.name)

			for i in range(0,17):
				try:
					cur = Reservation.objects.get(
					  room=room,
					  datetime_start__lte=(dt_start + timedelta(minutes=(settings.RES_MIN_LENGTH*i))),
					  datetime_end__gte=(dt_start + timedelta(minutes=(settings.RES_MIN_LENGTH*i))),
					  )
				except:
					cur = None

				if not cur is None:
					r.append(cur.type)
				else:
					r.append(0)

			rooms.append(r)

	c = RequestContext(request, {
		'page_title': 'Welcome!',
		'times': times,
		'rooms': rooms,
		'login_form': LoginForm(),
		'swap_axis': settings.RES_SWAP_AXIS,
		'email' : request.session.get('email',False),
	})
	c.update(csrf(request))

	return render_to_response(settings.RES_DEFAULT_TEMPLATE, c)

def reserve(email,roombc,datetime_start,datetime_end):
	ret = {
		'success': False,
		'error': '',
	}
	
	try:
		user = NPSUser.objects.get(email=email)
	except:
		user = NPSUser()
		user.email = email
		user.date_last_booking = datetime.now()
		
	try:
		roombc = RoomKey.objects.get(barcode=roombc)
		room = roombc.room
	except:
		ret['error'] = 'That room doesn\'t appear to exist. Please select another room.'
		return ret
		
	res = Reservation()
	res.requested_user = user
	res.room = room
	res.datetime_start = datetime_start
	res.datetime_end = datetime_end
	
	try:
		user.save()
		res.save()
	except Exception as ex:
		ret['error'] = str(ex)
		return ret
		
	ret['success'] = True
	return ret
	
def ajax_reserve(request):
	ret = {
		'success': False,
		'error': '',
	}
	
	if request.method == 'GET':
		email = request.GET.get('email', '0')
		roombc = request.GET.get('barcode','0')
		minutes = int(request.GET.get('minutes','0'))
		
		start = datetime.now()
		datetime_start = start - timedelta(minutes=(start.minute % settings.RES_MIN_LENGTH),
			seconds=start.second,
			microseconds=start.microsecond)
		datetime_end = start + timedelta(minutes=minutes)
		
		ret = reserve(email, roombc, datetime_start, datetime_end)
		
	return HttpResponse(json.dumps(ret))