# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Alimento.ganado'
        db.alter_column(u'alimentos_alimento', 'ganado_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['ganados.Ganado']))

    def backwards(self, orm):

        # Changing field 'Alimento.ganado'
        db.alter_column(u'alimentos_alimento', 'ganado_id', self.gf('django.db.models.fields.related.ForeignKey')(default=datetime.datetime(2014, 7, 19, 0, 0), to=orm['ganados.Ganado']))

    models = {
        u'alimentos.alimento': {
            'Meta': {'object_name': 'Alimento'},
            'caduca': ('django.db.models.fields.DateField', [], {}),
            'cantidad': ('django.db.models.fields.IntegerField', [], {}),
            'etapa': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'ganaderia': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'alimentos'", 'to': u"orm['profiles.Ganaderia']"}),
            'ganado': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'alimentos_ganado'", 'null': 'True', 'to': u"orm['ganados.Ganado']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
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
        u'ganados.ganado': {
            'Meta': {'object_name': 'Ganado'},
            'edad_anios': ('django.db.models.fields.IntegerField', [], {}),
            'edad_dias': ('django.db.models.fields.IntegerField', [], {}),
            'edad_meses': ('django.db.models.fields.IntegerField', [], {}),
            'forma_concepcion': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'ganaderia': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profiles.Ganaderia']"}),
            'genero': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identificacion_ecuador': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'identificaciones_ecuador'", 'null': 'True', 'to': u"orm['ganados.Identificacion_Ecuador']"}),
            'identificacion_simple': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'identificaciones_simples'", 'null': 'True', 'to': u"orm['ganados.Identificacion_Simple']"}),
            'imagen': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'nacimiento': ('django.db.models.fields.DateField', [], {}),
            'observaciones': ('django.db.models.fields.TextField', [], {'max_length': '125'}),
            'raza': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'ganados.identificacion_ecuador': {
            'Meta': {'ordering': "['rp']", 'object_name': 'Identificacion_Ecuador'},
            'codigo_barras': ('django.db.models.fields.CharField', [], {'max_length': "'20'"}),
            'codigo_pais': ('django.db.models.fields.CharField', [], {'max_length': "'7'"}),
            'codigo_provincia': ('django.db.models.fields.CharField', [], {'max_length': "'7'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': "'13'"}),
            'numero_serie': ('django.db.models.fields.CharField', [], {'max_length': "'8'"}),
            'rp': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'rp_madre': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'rp_padre': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'siglas_pais': ('django.db.models.fields.CharField', [], {'max_length': "'7'"})
        },
        u'ganados.identificacion_simple': {
            'Meta': {'ordering': "['rp']", 'object_name': 'Identificacion_Simple'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': "'13'"}),
            'rp': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'rp_madre': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'rp_padre': ('django.db.models.fields.PositiveIntegerField', [], {})
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

    complete_apps = ['alimentos']