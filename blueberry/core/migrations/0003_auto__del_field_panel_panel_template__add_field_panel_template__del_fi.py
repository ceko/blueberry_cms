# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Panel.panel_template'
        db.delete_column('core_panel', 'panel_template_id')

        # Adding field 'Panel.template'
        db.add_column('core_panel', 'template',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['core.PanelTemplate']),
                      keep_default=False)

        # Deleting field 'Block.block_template'
        db.delete_column('core_block', 'block_template_id')

        # Adding field 'Block.template'
        db.add_column('core_block', 'template',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['core.BlockTemplate']),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Panel.panel_template'
        raise RuntimeError("Cannot reverse this migration. 'Panel.panel_template' and its values cannot be restored.")
        # Deleting field 'Panel.template'
        db.delete_column('core_panel', 'template_id')


        # User chose to not deal with backwards NULL issues for 'Block.block_template'
        raise RuntimeError("Cannot reverse this migration. 'Block.block_template' and its values cannot be restored.")
        # Deleting field 'Block.template'
        db.delete_column('core_block', 'template_id')


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'panel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Panel']"}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.BlockTemplate']"})
        },
        'core.blocktemplate': {
            'Meta': {'object_name': 'BlockTemplate'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'class_path': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'core.panel': {
            'Meta': {'unique_together': "(('resource', 'alias'),)", 'object_name': 'Panel'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Resource']"}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.PanelTemplate']"})
        },
        'core.paneltemplate': {
            'Meta': {'object_name': 'PanelTemplate'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'class_path': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'revision_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.RevisionGroup']"})
        },
        'core.revisiongroup': {
            'Meta': {'object_name': 'RevisionGroup'},
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