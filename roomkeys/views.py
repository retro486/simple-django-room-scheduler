from django.http import HttpResponse
from models import RoomKey, RoomKeyUsage
from datetime import datetime
import json

def get_room(barcode):
	ret = {
		'room': False,
		'error': '',
	}
		
	try:
		result = RoomKey.objects.get(barcode=barcode)
		ret['room'] = result.room.name
		_ = checkin(ret['room'].barcode) # check in the room, throwing out the result
		
	except Exception as ex:
		ret['error'] = 'Invalid room key barcode or that room key isn\'t in the system. Please contact the circulation desk.'
		
	return ret

def checkin(barcode):
	ret = {
		'error': '',
	}
	
	try:
		roomkey = RoomKey.objects.get(barcode=barcode)
		roomusage = RoomKeyUsage.objects.filter(datetime_checkin=None,roomkey=roomkey)
		
		if len(roomusage) > 1:
			raise Exception('Detected corrupt usage data for this key.')
		elif len(roomusage) == 1:
			roomusage[0].datetime_checkin = datetime.now()
			roomusage[0].save()
		else:
			ret['error'] = 'The given room key is not currently checked out.'
		
	except Exception as ex:
		ret['error'] = str(ex) + ' Please notify the circulation desk.'
	
	return ret

# ajax request to translate a room key barcode into a room
def ajax_get_room(request):
	ret = {
		'room': False,
		'error': '',
	}
	
	if request.method == 'GET':
		ret = get_room(request.GET.get('barcode', '0'))
	
	return HttpResponse(json.dumps(ret))
	
def ajax_checkin(request):
	ret = {
		'error': '',
	}
	
	if request.method == 'GET':
		ret = checkin(request.GET.get('barcode', '0'))
		
	return HttpResponse(json.dumps(ret))
