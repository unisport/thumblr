# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'ImageFile', fields ['size']
        db.delete_unique(u'thumblr_imagefile', ['size_id'])

        # Adding M2M table for field content_types on 'ImageSize'
        m2m_table_name = db.shorten_name(u'thumblr_imagesize_content_types')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('imagesize', models.ForeignKey(orm[u'thumblr.imagesize'], null=False)),
            ('contenttype', models.ForeignKey(orm[u'contenttypes.contenttype'], null=False))
        ))
        db.create_unique(m2m_table_name, ['imagesize_id', 'contenttype_id'])


        # Changing field 'ImageFile.size'
        db.alter_column(u'thumblr_imagefile', 'size_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['thumblr.ImageSize']))

    def backwards(self, orm):
        # Removing M2M table for field content_types on 'ImageSize'
        db.delete_table(db.shorten_name(u'thumblr_imagesize_content_types'))


        # Changing field 'ImageFile.size'
        db.alter_column(u'thumblr_imagefile', 'size_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['thumblr.ImageSize'], unique=True))
        # Adding unique constraint on 'ImageFile', fields ['size']
        db.create_unique(u'thumblr_imagefile', ['size_id'])


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
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'original_file_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']", 'null': 'True'})
        },
        u'thumblr.imagefile': {
            'Meta': {'object_name': 'ImageFile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['thumblr.Image']"}),
            'image_hash': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'image_hash_in_storage': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'image_in_storage': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'meta_data': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['thumblr.ImageSize']"})
        },
        u'thumblr.imagesize': {
            'Meta': {'object_name': 'ImageSize'},
            'content_types': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'image_sizes'", 'symmetrical': 'False', 'to': u"orm['contenttypes.ContentType']"}),
            'height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'primary_key': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['thumblr']