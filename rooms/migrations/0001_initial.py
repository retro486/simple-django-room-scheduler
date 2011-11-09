# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'NPSUser'
        db.create_table('rooms_npsuser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('balance', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=3, decimal_places=2)),
            ('date_last_booking', self.gf('django.db.models.fields.DateField')(default=datetime.date(2000, 1, 1))),
        ))
        db.send_create_signal('rooms', ['NPSUser'])

        # Adding model 'Floor'
        db.create_table('rooms_floor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=25)),
            ('level', self.gf('django.db.models.fields.IntegerField')(unique=True)),
        ))
        db.send_create_signal('rooms', ['Floor'])

        # Adding model 'Feature'
        db.create_table('rooms_feature', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('requires_checkout', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('rooms', ['Feature'])

        # Adding model 'Room'
        db.create_table('rooms_room', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=25)),
            ('floor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rooms.Floor'])),
        ))
        db.send_create_signal('rooms', ['Room'])

        # Adding M2M table for field features on 'Room'
        db.create_table('rooms_room_features', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('room', models.ForeignKey(orm['rooms.room'], null=False)),
            ('feature', models.ForeignKey(orm['rooms.feature'], null=False))
        ))
        db.create_unique('rooms_room_features', ['room_id', 'feature_id'])

        # Adding model 'Reservation'
        db.create_table('rooms_reservation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('datetime_end', self.gf('django.db.models.fields.DateTimeField')()),
            ('requested_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rooms.NPSUser'])),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rooms.Room'])),
            ('type', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('rooms', ['Reservation'])


    def backwards(self, orm):
        
        # Deleting model 'NPSUser'
        db.delete_table('rooms_npsuser')

        # Deleting model 'Floor'
        db.delete_table('rooms_floor')

        # Deleting model 'Feature'
        db.delete_table('rooms_feature')

        # Deleting model 'Room'
        db.delete_table('rooms_room')

        # Removing M2M table for field features on 'Room'
        db.delete_table('rooms_room_features')

        # Deleting model 'Reservation'
        db.delete_table('rooms_reservation')


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
        'rooms.npsuser': {
            'Meta': {'object_name': 'NPSUser'},
            'balance': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '3', 'decimal_places': '2'}),
            'date_last_booking': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2000, 1, 1)'}),
            'email': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'rooms.reservation': {
            'Meta': {'object_name': 'Reservation'},
            'datetime_end': ('django.db.models.fields.DateTimeField', [], {}),
            'datetime_start': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'requested_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rooms.NPSUser']"}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rooms.Room']"}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'rooms.room': {
            'Meta': {'object_name': 'Room'},
            'features': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['rooms.Feature']", 'symmetrical': 'False'}),
            'floor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rooms.Floor']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'})
        }
    }

    complete_apps = ['rooms']
