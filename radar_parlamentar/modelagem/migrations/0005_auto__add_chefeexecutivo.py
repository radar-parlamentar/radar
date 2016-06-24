# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ChefeExecutivo'
        db.create_table('modelagem_chefeexecutivo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('genero', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('partido', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['modelagem.Partido'])),
            ('mandato_ano_inicio', self.gf('django.db.models.fields.IntegerField')()),
            ('mandato_ano_fim', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('modelagem', ['ChefeExecutivo'])

        # Adding M2M table for field casas_legislativas on 'ChefeExecutivo'
        m2m_table_name = db.shorten_name('modelagem_chefeexecutivo_casas_legislativas')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('chefeexecutivo', models.ForeignKey(orm['modelagem.chefeexecutivo'], null=False)),
            ('casalegislativa', models.ForeignKey(orm['modelagem.casalegislativa'], null=False))
        ))
        db.create_unique(m2m_table_name, ['chefeexecutivo_id', 'casalegislativa_id'])


    def backwards(self, orm):
        # Deleting model 'ChefeExecutivo'
        db.delete_table('modelagem_chefeexecutivo')

        # Removing M2M table for field casas_legislativas on 'ChefeExecutivo'
        db.delete_table(db.shorten_name('modelagem_chefeexecutivo_casas_legislativas'))


    models = {
        'modelagem.casalegislativa': {
            'Meta': {'object_name': 'CasaLegislativa'},
            'esfera': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'nome_curto': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'modelagem.chefeexecutivo': {
            'Meta': {'object_name': 'ChefeExecutivo'},
            'casas_legislativas': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['modelagem.CasaLegislativa']", 'symmetrical': 'False'}),
            'genero': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mandato_ano_fim': ('django.db.models.fields.IntegerField', [], {}),
            'mandato_ano_inicio': ('django.db.models.fields.IntegerField', [], {}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'partido': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['modelagem.Partido']"})
        },
        'modelagem.indexadores': {
            'Meta': {'object_name': 'Indexadores'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'principal': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'termo': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        'modelagem.parlamentar': {
            'Meta': {'object_name': 'Parlamentar'},
            'casa_legislativa': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['modelagem.CasaLegislativa']", 'null': 'True'}),
            'genero': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_parlamentar': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'localidade': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'partido': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['modelagem.Partido']"})
        },
        'modelagem.partido': {
            'Meta': {'object_name': 'Partido'},
            'cor': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'numero': ('django.db.models.fields.IntegerField', [], {})
        },
        'modelagem.proposicao': {
            'Meta': {'object_name': 'Proposicao'},
            'ano': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'autor_principal': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'autores': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'demais_autores'", 'null': 'True', 'to': "orm['modelagem.Parlamentar']"}),
            'casa_legislativa': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['modelagem.CasaLegislativa']", 'null': 'True'}),
            'data_apresentacao': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'descricao': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'ementa': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_prop': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'indexacao': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'numero': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'sigla': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'situacao': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'modelagem.votacao': {
            'Meta': {'object_name': 'Votacao'},
            'data': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'descricao': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_vot': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'proposicao': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['modelagem.Proposicao']", 'null': 'True'}),
            'resultado': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'modelagem.voto': {
            'Meta': {'object_name': 'Voto'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opcao': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'parlamentar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['modelagem.Parlamentar']"}),
            'votacao': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['modelagem.Votacao']"})
        }
    }

    complete_apps = ['modelagem']