# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Patron.exempt_from_restrictions'
        db.add_column('rooms_patron', 'exempt_from_restrictions', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Patron.exempt_from_restrictions'
        db.delete_column('rooms_patron', 'exempt_from_restrictions')


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
            'exempt_from_restrictions': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
