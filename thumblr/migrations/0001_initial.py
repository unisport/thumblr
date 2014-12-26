# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ImageSize'
        db.create_table(u'thumblr_imagesize', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30, primary_key=True)),
            ('width', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('height', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='image_sizes', to=orm['contenttypes.ContentType'])),
        ))
        db.send_create_signal(u'thumblr', ['ImageSize'])

        # Adding model 'Image'
        db.create_table(u'thumblr_image', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'], null=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('original_file_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('image_in_storage', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('image_hash_in_storage', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('image_hash', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('size', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['thumblr.ImageSize'])),
            ('meta_data', self.gf('jsonfield.fields.JSONField')(null=True, blank=True)),
            ('is_main', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'thumblr', ['Image'])


    def backwards(self, orm):
        # Deleting model 'ImageSize'
        db.delete_table(u'thumblr_imagesize')

        # Deleting model 'Image'
        db.delete_table(u'thumblr_image')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'thumblr.image': {
            'Meta': {'object_name': 'Image'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_hash': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'image_hash_in_storage': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'image_in_storage': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'is_main': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'meta_data': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'original_file_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']", 'null': 'True'}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['thumblr.ImageSize']"})
        },
        u'thumblr.imagesize': {
            'Meta': {'object_name': 'ImageSize'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'image_sizes'", 'to': u"orm['contenttypes.ContentType']"}),
            'height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'primary_key': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['thumblr']