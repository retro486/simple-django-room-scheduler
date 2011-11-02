from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime,timedelta,date
from django.conf import settings
from django.db.models.signals import pre_delete

class NPSUser(models.Model):
	email = models.CharField(max_length=255, unique=True)
	balance = models.DecimalField(default=0.0,
		max_digits=len(str(settings.RES_DAILY_QUOTA)),
		decimal_places=2, # doesn't need to be super-accurate and really should be in 
						# increments of settings.RES_INTERVAL
	)
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
	type = models.PositiveIntegerField(choices=settings.RES_TYPE_CHOICES)

	def __str__(self):
		return self.room.name + ': ' + self.datetime_start.ctime() + ' to ' + self.datetime_end.ctime()
		 
	'''
	Validates a reservation in that it ensures no conflicts.
	'''
	def clean(self):
		conflict = False
		is_admin = self.requested_user.email in settings.RES_ADMINS
		hours = float((self.datetime_end - self.datetime_start).seconds) / (60.00*60.00)

		# make sure user didn't "accidentally" swap start/end datetimes
		if self.datetime_start >= self.datetime_end:
			raise ValidationError(u'The selected start and end dates/times do not make sense.')

		if settings.RES_ENFORCE_MIN_LENGTH:
			if (self.datetime_end - self.datetime_start).seconds / 60 < settings.RES_MIN_LENGTH:
				raise ValidationError(u'The selected start and end dates/times do not meet the minimum length requirement of %i minutes.' % settings.RES_MIN_LENGTH)

		if settings.RES_ENFORCE_DAILY_QUOTA and not is_admin:
			balance = float(self.requested_user.balance)
			
			# reset the user's quota if they haven't booked any rooms today
			if self.requested_user.date_last_booking < datetime.now().date():
				self.requested_user.date_last_booking = datetime.now().date()
				self.requested_user.balance = 0.00
				balance = 0.00
			
			elif balance > settings.RES_DAILY_QUOTA: 
				raise ValidationError(u'You have met your daily reservation quota. Please share with another student or return tomorrow. Quotas are reset every day.')
		
			# check if the selected time slot would go over user's quota
			elif balance + hours > settings.RES_DAILY_QUOTA:
				raise ValidationError(u'The selected reservation length would put you over your daily alloted limit of %.2f hours. Please reduce your reservation time by %.2f hours and try again.' % (settings.RES_DAILY_QUOTA,(hours + balance - settings.RES_DAILY_QUOTA)))
	
		# if this is a modification or reschedule, refund the user the full value of the old schedule later
		refund = 0.00
		try:
			r = Reservation.objects.get(pk=self.pk)
			refund = float((r.datetime_end - r.datetime_start).minutes / (60.00*60.00))
		except:
			pass # this is NOT a modification or reschedule

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

		if settings.RES_ENFORCE_DAILY_QUOTA and not is_admin:
			value = balance + hours
			if settings.RES_ALLOW_REFUNDS:
				value -= refund
	
			self.requested_user.balance = str(value) # has to do with how Decimal hates float :'(
			self.requested_user.save() # update the user object

		return # model passes validation
	
'''
Refunds a user their hours if a scheduled meeting is cancelled, but only if it was cancelled at most
10 minutes after it started. Using pre_delete signal to ensure this gets caught on bulk deletes.
'''
def refund_before_delete(sender, **kwargs):
	dt = timedelta(minutes=-(settings.RES_REFUND_THRESHOLD))
	instance = kwargs['instance']
	if datetime.now() < instance.datetime_start - dt:
		refund = (instance.datetime_end - instance.datetime_start).seconds / (60.00*60.00)
		balance = float(instance.requested_user.balance)
		instance.requested_user.balance = str(balance - refund)
		instance.requested_user.save()

# hook into signals for special processing
if settings.RES_ALLOW_REFUNDS:
	pre_delete.connect(refund_before_delete, Reservation)
