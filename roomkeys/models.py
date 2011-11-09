from django.db import models
from rooms.models import Room

class RoomKey(models.Model):
	barcode = models.CharField(max_length=100,unique=True)
	room = models.ForeignKey(Room)
	datetime_last_checkout = models.DateTimeField()
	datetime_last_checkin = models.DateTimeField()
	
	def __str__(self):
		return self.room.name

class RoomKeyUsage(models.Model):
	roomkey = models.ForeignKey(RoomKey)
	datetime_checkout = models.DateTimeField()
	datetime_checkin = models.DateTimeField(blank=True,null=True) # aids in the detection of incomplete sessions
	