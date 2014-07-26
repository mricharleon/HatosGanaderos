# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Configuracion'
        db.create_table(u'profiles_configuracion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tipo_identificacion', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('celo_frecuencia', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('celo_frecuencia_error', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('celo_duracion', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('celo_duracion_error', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('celo_despues_parto', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('celo_despues_parto_error', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('intentos_verificacion_celo', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
            ('etapa_ternera', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('etapa_vacona', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('etapa_vientre', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('periodo_gestacion', self.gf('django.db.models.fields.IntegerField')(max_length=3)),
            ('periodo_seco', self.gf('django.db.models.fields.IntegerField')(max_length=3)),
            ('periodo_lactancia', self.gf('django.db.models.fields.IntegerField')(max_length=3)),
            ('periodo_vacio', self.gf('django.db.models.fields.IntegerField')(max_length=3)),
            ('numero_ordenios', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
        ))
        db.send_create_signal(u'profiles', ['Configuracion'])

        # Adding model 'Profile'
        db.create_table(u'profiles_profile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mugshot', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('privacy', self.gf('django.db.models.fields.CharField')(default='registered', max_length=15)),
            ('language', self.gf('django.db.models.fields.CharField')(default='es', max_length=5)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True, to=orm['auth.User'])),
            ('gender', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('direccion', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('telefono', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
        ))
        db.send_create_signal(u'profiles', ['Profile'])

        # Adding model 'Ganaderia'
        db.create_table(u'profiles_ganaderia', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombreEntidad', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('direccion', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('perfil', self.gf('django.db.models.fields.related.OneToOneField')(related_name='ganaderia', unique=True, to=orm['profiles.Profile'])),
            ('configuracion', self.gf('django.db.models.fields.related.OneToOneField')(related_name='ganaderia', unique=True, to=orm['profiles.Configuracion'])),
        ))
        db.send_create_signal(u'profiles', ['Ganaderia'])


    def backwards(self, orm):
        # Deleting model 'Configuracion'
        db.delete_table(u'profiles_configuracion')

        # Deleting model 'Profile'
        db.delete_table(u'profiles_profile')

        # Deleting model 'Ganaderia'
        db.delete_table(u'profiles_ganaderia')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'profiles.configuracion': {
            'Meta': {'object_name': 'Configuracion'},
            'celo_despues_parto': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'celo_despues_parto_error': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'celo_duracion': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'celo_duracion_error': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'celo_frecuencia': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'celo_frecuencia_error': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'etapa_ternera': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'etapa_vacona': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'etapa_vientre': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intentos_verificacion_celo': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            'numero_ordenios': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            'periodo_gestacion': ('django.db.models.fields.IntegerField', [], {'max_length': '3'}),
            'periodo_lactancia': ('django.db.models.fields.IntegerField', [], {'max_length': '3'}),
            'periodo_seco': ('django.db.models.fields.IntegerField', [], {'max_length': '3'}),
            'periodo_vacio': ('django.db.models.fields.IntegerField', [], {'max_length': '3'}),
            'tipo_identificacion': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        u'profiles.ganaderia': {
            'Meta': {'object_name': 'Ganaderia'},
            'configuracion': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'ganaderia'", 'unique': 'True', 'to': u"orm['profiles.Configuracion']"}),
            'direccion': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombreEntidad': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'perfil': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'ganaderia'", 'unique': 'True', 'to': u"orm['profiles.Profile']"})
        },
        u'profiles.profile': {
            'Meta': {'object_name': 'Profile'},
            'direccion': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'gender': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'es'", 'max_length': '5'}),
            'mugshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'privacy': ('django.db.models.fields.CharField', [], {'default': "'registered'", 'max_length': '15'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['profiles']