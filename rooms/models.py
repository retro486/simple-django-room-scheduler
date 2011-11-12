from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime,timedelta,date
from django.conf import settings
from django.db.models.signals import pre_delete

class NPSUser(models.Model):
	email = models.CharField(max_length=255, unique=True)
	# just some random date in the far past:
	date_last_booking = models.DateField(default=date(2000,1,1)) 

	def __str__(self):
		return self.email

class Floor(models.Model):
	name = models.CharField(max_length=25, unique=True)
	level = models.IntegerField(unique=True)

	def __str__(self):
		return self.name

class Feature(models.Model):
	name = models.CharField(max_length=100, unique=True)
	requires_checkout = models.BooleanField()

	def __str__(self):
		return self.name

class Room(models.Model):
	name = models.CharField(max_length=25, unique=True)
	floor = models.ForeignKey(Floor)
	features = models.ManyToManyField(Feature)

	def __str__(self):
		return self.name

class Reservation(models.Model):
	datetime_start = models.DateTimeField()
	datetime_end = models.DateTimeField()
	requested_user = models.ForeignKey(NPSUser)
	room = models.ForeignKey(Room)
	type = models.PositiveIntegerField(choices=settings.RES_TYPE_CHOICES, default=1)

	def __str__(self):
		return self.room.name + ': ' + self.datetime_start.ctime() + ' to ' + self.datetime_end.ctime()
		 
	'''
	Validates a reservation in that it ensures no conflicts.
	'''
	def clean(self):
		conflict = False
		is_admin = self.requested_user.email in settings.RES_ADMINS
		hours = float((self.datetime_end - self.datetime_start).seconds) / (60.00*60.00)

		if settings.RES_ENFORCE_OAAT:
			try:
				res = Reservation.objects.get(requested_user=self.requested_user,
					datetime_start__lte=datetime.now(),
					datetime_end__gte=datetime.now())
				# if no exception at this point, user already has a reservation right now
				raise ValidationError(u'You already have a reservation in progress. Please return the key for the current reservation before requesting another one.')
			
			except ValidationError as v:
				raise v
			except Exception as ex:
				pass
				 # nothing wrong
		
		# make sure user didn't "accidentally" swap start/end datetimes
		if self.datetime_start >= self.datetime_end:
			raise ValidationError(u'The selected start and end dates/times do not make sense.')

		if settings.RES_ENFORCE_MIN_LENGTH:
			if (self.datetime_end - self.datetime_start).seconds / 60 < settings.RES_MIN_LENGTH:
				raise ValidationError(u'The selected start and end dates/times do not meet the minimum length requirement of %i minutes.' % settings.RES_MIN_LENGTH)

		if settings.RES_ENFORCE_MAX_NUM and not is_admin and len(Reservation.objects.filter(
		  requested_user=self.requested_user,
		  datetime_start__year=self.datetime_start.year,
		  datetime_start__month=self.datetime_start.month,
		  datetime_start__day=self.datetime_start.day)) > settings.RES_MAX_NUM:
			raise ValidationError(u'You have met your daily quota of %i reservations today. Please share with another student or return tomorrow. Quotas are reset every day.' % settings.RES_MAX_NUM)

		res = Reservation.objects.filter(room=self.room,datetime_start__gte=self.datetime_start,
			datetime_start__lte=self.datetime_end).exclude(pk=self.pk)
		if len(res) > 0:
			conflict = True

		res = Reservation.objects.filter(room=self.room,datetime_end__gte=self.datetime_start,
			datetime_end__lte=self.datetime_end).exclude(pk=self.pk)
		if len(res) > 0:
			conflict = True

		res = Reservation.objects.filter(room=self.room,datetime_start__gte=self.datetime_start,
			datetime_end__lte=self.datetime_end).exclude(pk=self.pk)
		if len(res) > 0:
			conflict = True

		res = Reservation.objects.filter(room=self.room,datetime_start__lte=self.datetime_start,
			datetime_end__gte=self.datetime_end).exclude(pk=self.pk)
		if len(res) > 0:
			conflict = True

		if conflict:
			raise ValidationError(u'There exists a reservation which conflicts with your requested dates and/or times.')

		return # model passes validation
