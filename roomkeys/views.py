from django.http import HttpResponse
from models import RoomKey
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
		
	except Exception as ex:
		ret['error'] = 'Invalid room key barcode or that room key isn\'t in the system. Please contact the circulation desk.'
		
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