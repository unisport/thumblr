# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Image'
        db.create_table(u'thumblr_image', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['sites.Site'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('original_file_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'thumblr', ['Image'])

        # Adding model 'ImageSize'
        db.create_table(u'thumblr_imagesize', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30, primary_key=True)),
            ('max_width', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('max_height', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal(u'thumblr', ['ImageSize'])

        # Adding model 'ImageFile'
        db.create_table(u'thumblr_imagefile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['thumblr.Image'])),
            ('image_in_storage', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('image_hash', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('size', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['thumblr.ImageSize'])),
            ('meta_data', self.gf('jsonfield.fields.JSONField')(null=True)),
            ('old', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'thumblr', ['ImageFile'])


    def backwards(self, orm):
        # Deleting model 'Image'
        db.delete_table(u'thumblr_image')

        # Deleting model 'ImageSize'
        db.delete_table(u'thumblr_imagesize')

        # Deleting model 'ImageFile'
        db.delete_table(u'thumblr_imagefile')


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
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'original_file_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['sites.Site']"})
        },
        u'thumblr.imagefile': {
            'Meta': {'object_name': 'ImageFile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['thumblr.Image']"}),
            'image_hash': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'image_in_storage': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'meta_data': ('jsonfield.fields.JSONField', [], {'null': 'True'}),
            'old': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['thumblr.ImageSize']"})
        },
        u'thumblr.imagesize': {
            'Meta': {'object_name': 'ImageSize'},
            'max_height': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'max_width': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'primary_key': 'True'})
        }
    }

    complete_apps = ['thumblr']