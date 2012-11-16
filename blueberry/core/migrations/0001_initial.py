# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Theme'
        db.create_table('core_theme', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('class_path', self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=50)),
            ('pretty_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('priority', self.gf('django.db.models.fields.IntegerField')(unique=True)),
        ))
        db.send_create_signal('core', ['Theme'])

        # Adding model 'ResourceTemplate'
        db.create_table('core_resourcetemplate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('class_path', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('pretty_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('core', ['ResourceTemplate'])

        # Adding model 'Revision'
        db.create_table('core_revision', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('core', ['Revision'])

        # Adding model 'Resource'
        db.create_table('core_resource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('revision', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Revision'])),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.ResourceTemplate'])),
            ('path_suffix', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('core', ['Resource'])

        # Adding model 'ResourceMap'
        db.create_table('core_resourcemap', (
            ('revision', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Revision'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.ResourceMap'], null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=500, primary_key=True)),
            ('resource', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Resource'])),
        ))
        db.send_create_signal('core', ['ResourceMap'])

        # Adding model 'Panel'
        db.create_table('core_panel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('revision', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Revision'])),
            ('class_path', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('resource', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Resource'])),
            ('alias', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('core', ['Panel'])

        # Adding unique constraint on 'Panel', fields ['resource', 'alias']
        db.create_unique('core_panel', ['resource_id', 'alias'])

        # Adding model 'Block'
        db.create_table('core_block', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('revision', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Revision'])),
            ('class_path', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('panel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Panel'])),
            ('alias', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('core', ['Block'])


    def backwards(self, orm):
        # Removing unique constraint on 'Panel', fields ['resource', 'alias']
        db.delete_unique('core_panel', ['resource_id', 'alias'])

        # Deleting model 'Theme'
        db.delete_table('core_theme')

        # Deleting model 'ResourceTemplate'
        db.delete_table('core_resourcetemplate')

        # Deleting model 'Revision'
        db.delete_table('core_revision')

        # Deleting model 'Resource'
        db.delete_table('core_resource')

        # Deleting model 'ResourceMap'
        db.delete_table('core_resourcemap')

        # Deleting model 'Panel'
        db.delete_table('core_panel')

        # Deleting model 'Block'
        db.delete_table('core_block')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.block': {
            'Meta': {'object_name': 'Block'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'class_path': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'panel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Panel']"}),
            'revision': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Revision']"})
        },
        'core.panel': {
            'Meta': {'unique_together': "(('resource', 'alias'),)", 'object_name': 'Panel'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'class_path': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Resource']"}),
            'revision': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Revision']"})
        },
        'core.resource': {
            'Meta': {'object_name': 'Resource'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path_suffix': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'revision': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Revision']"}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ResourceTemplate']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'core.resourcemap': {
            'Meta': {'object_name': 'ResourceMap'},
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ResourceMap']", 'null': 'True', 'blank': 'True'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Resource']"}),
            'revision': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Revision']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '500', 'primary_key': 'True'})
        },
        'core.resourcetemplate': {
            'Meta': {'object_name': 'ResourceTemplate'},
            'class_path': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pretty_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'core.revision': {
            'Meta': {'object_name': 'Revision'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'core.theme': {
            'Meta': {'object_name': 'Theme'},
            'class_path': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pretty_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'unique': 'True'})
        }
    }

    complete_apps = ['core']