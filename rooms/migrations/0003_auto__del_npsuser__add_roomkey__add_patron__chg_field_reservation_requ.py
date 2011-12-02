# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'NPSUser'
        db.delete_table('rooms_npsuser')

        # Adding model 'RoomKey'
        db.create_table('rooms_roomkey', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('barcode', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rooms.Room'])),
        ))
        db.send_create_signal('rooms', ['RoomKey'])

        # Adding model 'Patron'
        db.create_table('rooms_patron', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('date_last_booking', self.gf('django.db.models.fields.DateField')(default=datetime.date(2000, 1, 1))),
        ))
        db.send_create_signal('rooms', ['Patron'])

        # Changing field 'Reservation.requested_user'
        db.alter_column('rooms_reservation', 'requested_user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rooms.Patron']))


    def backwards(self, orm):
        
        # Adding model 'NPSUser'
        db.create_table('rooms_npsuser', (
            ('email', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True)),
            ('date_last_booking', self.gf('django.db.models.fields.DateField')(default=datetime.date(2000, 1, 1))),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('rooms', ['NPSUser'])

        # Deleting model 'RoomKey'
        db.delete_table('rooms_roomkey')

        # Deleting model 'Patron'
        db.delete_table('rooms_patron')

        # Changing field 'Reservation.requested_user'
        db.alter_column('rooms_reservation', 'requested_user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rooms.NPSUser']))


    models = {
        'rooms.feature': {
            'Meta': {'object_name': 'Feature'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'requires_checkout': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'rooms.floor': {
            'Meta': {'object_name': 'Floor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'})
        },
        'rooms.patron': {
            'Meta': {'object_name': 'Patron'},
            'date_last_booking': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2000, 1, 1)'}),
            'email': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'rooms.reservation': {
            'Meta': {'object_name': 'Reservation'},
            'datetime_end': ('django.db.models.fields.DateTimeField', [], {}),
            'datetime_start': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'requested_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rooms.Patron']"}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rooms.Room']"}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        'rooms.room': {
            'Meta': {'object_name': 'Room'},
            'features': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['rooms.Feature']", 'symmetrical': 'False'}),
            'floor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rooms.Floor']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'})
        },
        'rooms.roomkey': {
            'Meta': {'object_name': 'RoomKey'},
            'barcode': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rooms.Room']"})
        }
    }

    complete_apps = ['rooms']
