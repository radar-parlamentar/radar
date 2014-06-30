# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Partido.nome'
        db.alter_column('modelagem_partido', 'nome', self.gf(
            'django.db.models.fields.CharField')(max_length=13))

    def backwards(self, orm):

        # Changing field 'Partido.nome'
        db.alter_column('modelagem_partido', 'nome', self.gf(
            'django.db.models.fields.CharField')(max_length=12))

    models = {
        'modelagem.casalegislativa': {
            'Meta': {'object_name': 'CasaLegislativa'},
            'atualizacao': ('django.db.models.fields.DateField', [],
             {'null': 'True', 'blank': 'True'}),
            'esfera': ('django.db.models.fields.CharField', [],
                       {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [],
                   {'primary_key': 'True'}),
            'local': ('django.db.models.fields.CharField', [],
                      {'max_length': '100'}),
            'nome': ('django.db.models.fields.CharField', [],
                     {'max_length': '100'}),
            'nome_curto': ('django.db.models.fields.CharField', [],
                           {'unique': 'True', 'max_length': '50'})
        },
        'modelagem.indexadores': {
            'Meta': {'object_name': 'Indexadores'},
            'id': ('django.db.models.fields.AutoField', [],
                   {'primary_key': 'True'}),
            'principal': ('django.db.models.fields.BooleanField', [],
                          {'default': 'False'}),
            'termo': ('django.db.models.fields.CharField', [],
                      {'max_length': '120'})
        },
        'modelagem.legislatura': {
            'Meta': {'object_name': 'Legislatura'},
            'casa_legislativa': (
                'django.db.models.fields.related.ForeignKey',
                [], {
                    'to': "orm['modelagem.CasaLegislativa']", 'null': 'True'}),
            'fim': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [],
                   {'primary_key': 'True'}),
            'inicio': ('django.db.models.fields.DateField', [],
                       {'null': 'True'}),
            'localidade': ('django.db.models.fields.CharField', [],
                           {'max_length': '100', 'blank': 'True'}),
            'parlamentar': ('django.db.models.fields.related.ForeignKey', [],
                            {'to': "orm['modelagem.Parlamentar']"}),
            'partido': ('django.db.models.fields.related.ForeignKey', [],
                {'to': "orm['modelagem.Partido']"})
        },
        'modelagem.parlamentar': {
            'Meta': {'object_name': 'Parlamentar'},
            'genero': ('django.db.models.fields.CharField', [],
                       {'max_length': '10', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [],
                   {'primary_key': 'True'}),
            'id_parlamentar': ('django.db.models.fields.CharField', [],
                               {'max_length': '100', 'blank': 'True'}),
            'nome': ('django.db.models.fields.CharField', [],
                     {'max_length': '100'})
        },
        'modelagem.partido': {
            'Meta': {'object_name': 'Partido'},
            'cor': ('django.db.models.fields.CharField', [],
                    {'max_length': '7'}),
            'id': ('django.db.models.fields.AutoField', [],
                   {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [],
                     {'max_length': '13'}),
            'numero': ('django.db.models.fields.IntegerField', [], {})
        },
        'modelagem.proposicao': {
            'Meta': {'object_name': 'Proposicao'},
            'ano': ('django.db.models.fields.CharField', [],
                    {'max_length': '4'}),
            'autor_principal': ('django.db.models.fields.TextField', [],
                                {'blank': 'True'}),
            'autores': ('django.db.models.fields.related.ManyToManyField', [],
                        {'symmetrical': 'False',
                         'related_name': "u'demais_autores'",
                         'null': 'True', 'to': "orm['modelagem.Parlamentar']"}),
            'casa_legislativa': ('django.db.models.fields.related.ForeignKey',
                                 [],
                                 {'to': "orm['modelagem.CasaLegislativa']",
                                  'null': 'True'}),
            'data_apresentacao': ('django.db.models.fields.DateField', [],
                                  {'null': 'True'}),
            'descricao': ('django.db.models.fields.TextField', [],
                          {'blank': 'True'}),
            'ementa': ('django.db.models.fields.TextField', [],
                       {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [],
                   {'primary_key': 'True'}),
            'id_prop': ('django.db.models.fields.CharField', [],
                        {'max_length': '100', 'blank': 'True'}),
            'indexacao': ('django.db.models.fields.TextField', [],
                          {'blank': 'True'}),
            'numero': ('django.db.models.fields.CharField', [],
                       {'max_length': '10'}),
            'sigla': ('django.db.models.fields.CharField', [],
                      {'max_length': '10'}),
            'situacao': ('django.db.models.fields.TextField', [],
                         {'blank': 'True'})
        },
        'modelagem.votacao': {
            'Meta': {'object_name': 'Votacao'},
            'data': ('django.db.models.fields.DateField', [],
                     {'null': 'True', 'blank': 'True'}),
            'descricao': ('django.db.models.fields.TextField', [],
                          {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [],
                   {'primary_key': 'True'}),
            'id_vot': ('django.db.models.fields.CharField', [],
                       {'max_length': '100', 'blank': 'True'}),
            'proposicao': ('django.db.models.fields.related.ForeignKey', [],
                           {'to': "orm['modelagem.Proposicao']",
                            'null': 'True'}),
            'resultado': ('django.db.models.fields.TextField', [],
                          {'blank': 'True'})
        },
        'modelagem.voto': {
            'Meta': {'object_name': 'Voto'},
            'id': ('django.db.models.fields.AutoField', [],
                   {'primary_key': 'True'}),
            'legislatura': ('django.db.models.fields.related.ForeignKey', [],
                            {'to': "orm['modelagem.Legislatura']"}),
            'opcao': ('django.db.models.fields.CharField', [],
                      {'max_length': '10'}),
            'votacao': ('django.db.models.fields.related.ForeignKey', [],
                        {'to': "orm['modelagem.Votacao']"})
        }
    }

    complete_apps = ['modelagem']
