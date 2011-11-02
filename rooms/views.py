from django.template import RequestContext
from django.shortcuts import render_to_response
from datetime import datetime,timedelta
from models import Reservation,Room
from django.conf import settings

def default_view(request):
	dt_start = datetime.now()
	fix1 = timedelta(minutes=dt_start.minute % settings.RES_MIN_LENGTH, seconds=dt_start.second,
	  microseconds=dt_start.microsecond) # zero out seconds
	dt_start -= fix1 # round down to nearest increment of 15 minutes

	print dt_start

	res = {}
	res['times'] = []
	res['rooms'] = []

	if settings.RES_SWAP_AXIS:
		# this bit is confusing because of naming; TODO change naming to be less confusing.
		for i in range(0,17):
			t = dt_start + timedelta(minutes=i*settings.RES_MIN_LENGTH)
			res['rooms'].append([])
			res['rooms'][i].append(':'.join(t.time().isoformat().split(':')[0:2]))
		
		for room in Room.objects.all():
			res['times'].append(room.name)
			
			for i in range(0,len(res['rooms'])):
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
					res['rooms'][i].append(0)
				else:
					res['rooms'][i].append(cur.type)

	else:
		for i in range(0,17):
			t = dt_start + timedelta(minutes=i*settings.RES_MIN_LENGTH)
			res['times'].append(':'.join(t.time().isoformat().split(':')[0:2]))

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

			res['rooms'].append(r)

	c = RequestContext(request, {
		'page_title': 'Welcome!',
		'res': res,
		'swap_axis': settings.RES_SWAP_AXIS,
	})

	return render_to_response('rooms_default.html', c)
