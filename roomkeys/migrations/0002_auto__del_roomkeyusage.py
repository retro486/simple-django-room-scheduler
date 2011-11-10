# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'RoomKeyUsage'
        db.delete_table('roomkeys_roomkeyusage')


    def backwards(self, orm):
        
        # Adding model 'RoomKeyUsage'
        db.create_table('roomkeys_roomkeyusage', (
            ('datetime_checkin', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('roomkey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['roomkeys.RoomKey'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime_checkout', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('roomkeys', ['RoomKeyUsage'])


    models = {
        'roomkeys.roomkey': {
            'Meta': {'object_name': 'RoomKey'},
            'barcode': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'datetime_last_checkin': ('django.db.models.fields.DateTimeField', [], {}),
            'datetime_last_checkout': ('django.db.models.fields.DateTimeField', [], {}),
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
