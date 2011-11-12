# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'RoomKey.datetime_last_checkout'
        db.delete_column('roomkeys_roomkey', 'datetime_last_checkout')

        # Deleting field 'RoomKey.datetime_last_checkin'
        db.delete_column('roomkeys_roomkey', 'datetime_last_checkin')


    def backwards(self, orm):
        
        # Adding field 'RoomKey.datetime_last_checkout'
        db.add_column('roomkeys_roomkey', 'datetime_last_checkout', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 11, 12, 11, 57, 30, 419525)), keep_default=False)

        # Adding field 'RoomKey.datetime_last_checkin'
        db.add_column('roomkeys_roomkey', 'datetime_last_checkin', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 11, 12, 11, 57, 36, 795505)), keep_default=False)


    models = {
        'roomkeys.roomkey': {
            'Meta': {'object_name': 'RoomKey'},
            'barcode': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rooms.Room']"})
        },
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
        'rooms.room': {
            'Meta': {'object_name': 'Room'},
            'features': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['rooms.Feature']", 'symmetrical': 'False'}),
            'floor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rooms.Floor']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'})
        }
    }

    complete_apps = ['roomkeys']
