# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GenericContentBlock'
        db.create_table('seed_genericcontentblock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('block', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.BlockTemplate'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('seed', ['GenericContentBlock'])


    def backwards(self, orm):
        # Deleting model 'GenericContentBlock'
        db.delete_table('seed_genericcontentblock')


    models = {
        'core.blocktemplate': {
            'Meta': {'object_name': 'BlockTemplate'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'class_path': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'seed.genericcontentblock': {
            'Meta': {'object_name': 'GenericContentBlock'},
            'block': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.BlockTemplate']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['seed']