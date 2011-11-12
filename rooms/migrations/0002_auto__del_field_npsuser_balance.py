# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'NPSUser.balance'
        db.delete_column('rooms_npsuser', 'balance')


    def backwards(self, orm):
        
        # Adding field 'NPSUser.balance'
        db.add_column('rooms_npsuser', 'balance', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=3, decimal_places=2), keep_default=False)


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
            'type': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
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
