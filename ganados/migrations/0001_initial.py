# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Identificacion_Simple'
        db.create_table(u'ganados_identificacion_simple', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rp', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length='13')),
            ('rp_madre', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('rp_padre', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'ganados', ['Identificacion_Simple'])

        # Adding model 'Identificacion_Ecuador'
        db.create_table(u'ganados_identificacion_ecuador', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('siglas_pais', self.gf('django.db.models.fields.CharField')(max_length='7')),
            ('codigo_pais', self.gf('django.db.models.fields.CharField')(max_length='7')),
            ('codigo_provincia', self.gf('django.db.models.fields.CharField')(max_length='7')),
            ('numero_serie', self.gf('django.db.models.fields.CharField')(max_length='8')),
            ('codigo_barras', self.gf('django.db.models.fields.CharField')(max_length='20')),
            ('rp', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length='13')),
            ('rp_madre', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('rp_padre', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'ganados', ['Identificacion_Ecuador'])

        # Adding model 'Ganado'
        db.create_table(u'ganados_ganado', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('imagen', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('ganaderia', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.Ganaderia'])),
            ('nacimiento', self.gf('django.db.models.fields.DateField')()),
            ('genero', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('raza', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('forma_concepcion', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('observaciones', self.gf('django.db.models.fields.TextField')(max_length=125)),
            ('edad_anios', self.gf('django.db.models.fields.IntegerField')()),
            ('edad_meses', self.gf('django.db.models.fields.IntegerField')()),
            ('edad_dias', self.gf('django.db.models.fields.IntegerField')()),
            ('identificacion_simple', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='identificaciones_simples', null=True, to=orm['ganados.Identificacion_Simple'])),
            ('identificacion_ecuador', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='identificaciones_ecuador', null=True, to=orm['ganados.Identificacion_Ecuador'])),
        ))
        db.send_create_signal(u'ganados', ['Ganado'])

        # Adding model 'Verificacion'
        db.create_table(u'ganados_verificacion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('intento', self.gf('django.db.models.fields.IntegerField')()),
            ('fecha_inicio', self.gf('django.db.models.fields.DateField')()),
            ('fecha_fin', self.gf('django.db.models.fields.DateField')()),
            ('estado', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('observaciones', self.gf('django.db.models.fields.TextField')(max_length=150, null=True, blank=True)),
            ('ganado', self.gf('django.db.models.fields.related.ForeignKey')(related_name='verificaciones', null=True, to=orm['ganados.Ganado'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'ganados', ['Verificacion'])

        # Adding model 'Ordenio'
        db.create_table(u'ganados_ordenio', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fecha', self.gf('django.db.models.fields.DateField')()),
            ('numero_ordenio', self.gf('django.db.models.fields.IntegerField')()),
            ('cantidad', self.gf('django.db.models.fields.IntegerField')()),
            ('total', self.gf('django.db.models.fields.IntegerField')()),
            ('observaciones', self.gf('django.db.models.fields.TextField')(max_length=150, null=True, blank=True)),
            ('ganado', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ordenios', null=True, to=orm['ganados.Ganado'])),
        ))
        db.send_create_signal(u'ganados', ['Ordenio'])

        # Adding model 'Celo'
        db.create_table(u'ganados_celo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fecha_inicio', self.gf('django.db.models.fields.DateTimeField')()),
            ('fecha_fin', self.gf('django.db.models.fields.DateTimeField')()),
            ('estado', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('observaciones', self.gf('django.db.models.fields.TextField')(max_length=150, null=True, blank=True)),
            ('ganado', self.gf('django.db.models.fields.related.ForeignKey')(related_name='celos', null=True, to=orm['ganados.Ganado'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'ganados', ['Celo'])

        # Adding model 'Ciclo'
        db.create_table(u'ganados_ciclo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fecha_inicio', self.gf('django.db.models.fields.DateField')()),
            ('nombre', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('fecha_fin', self.gf('django.db.models.fields.DateField')()),
            ('ganado', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ciclos', null=True, to=orm['ganados.Ganado'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'ganados', ['Ciclo'])

        # Adding model 'ProblemaGestacion'
        db.create_table(u'ganados_problemagestacion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fecha_problema', self.gf('django.db.models.fields.DateField')()),
            ('tipo_problema', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('observaciones', self.gf('django.db.models.fields.TextField')(max_length=150)),
        ))
        db.send_create_signal(u'ganados', ['ProblemaGestacion'])

        # Adding model 'Gestacion'
        db.create_table(u'ganados_gestacion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fecha_servicio', self.gf('django.db.models.fields.DateField')()),
            ('fecha_parto', self.gf('django.db.models.fields.DateField')()),
            ('tipo_parto', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('observaciones', self.gf('django.db.models.fields.TextField')(max_length=150)),
            ('problema', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['ganados.ProblemaGestacion'], unique=True)),
            ('ganado', self.gf('django.db.models.fields.related.ForeignKey')(related_name='gestaciones', null=True, to=orm['ganados.Ganado'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'ganados', ['Gestacion'])

        # Adding model 'Etapa'
        db.create_table(u'ganados_etapa', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fecha_inicio', self.gf('django.db.models.fields.DateField')()),
            ('nombre', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('observaciones', self.gf('django.db.models.fields.TextField')(max_length=150)),
            ('ganado', self.gf('django.db.models.fields.related.ForeignKey')(related_name='etapas', null=True, to=orm['ganados.Ganado'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'ganados', ['Etapa'])


    def backwards(self, orm):
        # Deleting model 'Identificacion_Simple'
        db.delete_table(u'ganados_identificacion_simple')

        # Deleting model 'Identificacion_Ecuador'
        db.delete_table(u'ganados_identificacion_ecuador')

        # Deleting model 'Ganado'
        db.delete_table(u'ganados_ganado')

        # Deleting model 'Verificacion'
        db.delete_table(u'ganados_verificacion')

        # Deleting model 'Ordenio'
        db.delete_table(u'ganados_ordenio')

        # Deleting model 'Celo'
        db.delete_table(u'ganados_celo')

        # Deleting model 'Ciclo'
        db.delete_table(u'ganados_ciclo')

        # Deleting model 'ProblemaGestacion'
        db.delete_table(u'ganados_problemagestacion')

        # Deleting model 'Gestacion'
        db.delete_table(u'ganados_gestacion')

        # Deleting model 'Etapa'
        db.delete_table(u'ganados_etapa')


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
        u'ganados.celo': {
            'Meta': {'object_name': 'Celo'},
            'estado': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'fecha_fin': ('django.db.models.fields.DateTimeField', [], {}),
            'fecha_inicio': ('django.db.models.fields.DateTimeField', [], {}),
            'ganado': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'celos'", 'null': 'True', 'to': u"orm['ganados.Ganado']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {}),
            'observaciones': ('django.db.models.fields.TextField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'})
        },
        u'ganados.ciclo': {
            'Meta': {'object_name': 'Ciclo'},
            'fecha_fin': ('django.db.models.fields.DateField', [], {}),
            'fecha_inicio': ('django.db.models.fields.DateField', [], {}),
            'ganado': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ciclos'", 'null': 'True', 'to': u"orm['ganados.Ganado']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {}),
            'nombre': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'ganados.etapa': {
            'Meta': {'object_name': 'Etapa'},
            'fecha_inicio': ('django.db.models.fields.DateField', [], {}),
            'ganado': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'etapas'", 'null': 'True', 'to': u"orm['ganados.Ganado']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {}),
            'nombre': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'observaciones': ('django.db.models.fields.TextField', [], {'max_length': '150'})
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
        u'ganados.gestacion': {
            'Meta': {'object_name': 'Gestacion'},
            'fecha_parto': ('django.db.models.fields.DateField', [], {}),
            'fecha_servicio': ('django.db.models.fields.DateField', [], {}),
            'ganado': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gestaciones'", 'null': 'True', 'to': u"orm['ganados.Ganado']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {}),
            'observaciones': ('django.db.models.fields.TextField', [], {'max_length': '150'}),
            'problema': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['ganados.ProblemaGestacion']", 'unique': 'True'}),
            'tipo_parto': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
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
        u'ganados.ordenio': {
            'Meta': {'object_name': 'Ordenio'},
            'cantidad': ('django.db.models.fields.IntegerField', [], {}),
            'fecha': ('django.db.models.fields.DateField', [], {}),
            'ganado': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ordenios'", 'null': 'True', 'to': u"orm['ganados.Ganado']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numero_ordenio': ('django.db.models.fields.IntegerField', [], {}),
            'observaciones': ('django.db.models.fields.TextField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'total': ('django.db.models.fields.IntegerField', [], {})
        },
        u'ganados.problemagestacion': {
            'Meta': {'object_name': 'ProblemaGestacion'},
            'fecha_problema': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observaciones': ('django.db.models.fields.TextField', [], {'max_length': '150'}),
            'tipo_problema': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'ganados.verificacion': {
            'Meta': {'object_name': 'Verificacion'},
            'estado': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_fin': ('django.db.models.fields.DateField', [], {}),
            'fecha_inicio': ('django.db.models.fields.DateField', [], {}),
            'ganado': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'verificaciones'", 'null': 'True', 'to': u"orm['ganados.Ganado']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intento': ('django.db.models.fields.IntegerField', [], {}),
            'is_active': ('django.db.models.fields.BooleanField', [], {}),
            'observaciones': ('django.db.models.fields.TextField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'})
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

    complete_apps = ['ganados']