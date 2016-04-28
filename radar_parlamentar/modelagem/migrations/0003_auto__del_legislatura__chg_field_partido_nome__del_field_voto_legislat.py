# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Legislatura'
        db.delete_table('modelagem_legislatura')

        # Changing field 'Partido.nome'
        db.alter_column(
            'modelagem_partido', 'nome', self.gf(
                'django.db.models.fields.CharField')(max_length=12))
        # Deleting field 'Voto.legislatura'
        db.delete_column('modelagem_voto', 'legislatura_id')

        # Adding field 'Voto.parlamentar'
        db.add_column('modelagem_voto', 'parlamentar',
                      self.gf('django.db.models.fields.related.ForeignKey')(
                          default=1,
                          to=orm['modelagem.Parlamentar']),
                      keep_default=False)

        # Adding field 'Parlamentar.casa_legislativa'
        db.add_column('modelagem_parlamentar', 'casa_legislativa',
                      self.gf('django.db.models.fields.related.ForeignKey')(
                          to=orm['modelagem.CasaLegislativa'],
                          null=True),
                      keep_default=False)

        # Adding field 'Parlamentar.partido'
        db.add_column('modelagem_parlamentar', 'partido',
                      self.gf('django.db.models.fields.related.ForeignKey')(
                          default=1,
                          to=orm['modelagem.Partido']),
                      keep_default=False)

        # Adding field 'Parlamentar.localidade'
        db.add_column('modelagem_parlamentar', 'localidade',
                      self.gf('django.db.models.fields.CharField')(
                          default='',
                          max_length=100,
                          blank=True),
                      keep_default=False)

    def backwards(self, orm):
        # Adding model 'Legislatura'
        db.create_table('modelagem_legislatura', (
            ('parlamentar', self.gf('django.db.models.fields.related. \
                ForeignKey')(to=orm['modelagem.Parlamentar'])),
            ('casa_legislativa', self.gf('django.db.models.fields.related. \
                ForeignKey')(to=orm['modelagem.CasaLegislativa'], null=True)),
            ('inicio', self.gf('django.db.models.fields.DateField')(
                null=True)),
            ('partido', self.gf('django.db.models.fields.related.ForeignKey')(
                to=orm['modelagem.Partido'])),
            ('localidade', self.gf('django.db.models.fields.CharField')(
                max_length=100, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(
                primary_key=True)),
            ('fim', self.gf('django.db.models.fields.DateField')(null=True)),
        ))
        db.send_create_signal('modelagem', ['Legislatura'])

        # Changing field 'Partido.nome'
        db.alter_column('modelagem_partido', 'nome', self.gf(
            'django.db.models.\fields.CharField')(max_length=13))
        # Adding field 'Voto.legislatura'
        db.add_column('modelagem_voto', 'legislatura',
                      self.gf('django.db.models.fields.related.ForeignKey')(
                          default=1,
                          to=orm['modelagem.Legislatura']),
                      keep_default=False)

        # Deleting field 'Voto.parlamentar'
        db.delete_column('modelagem_voto', 'parlamentar_id')

        # Deleting field 'Parlamentar.casa_legislativa'
        db.delete_column('modelagem_parlamentar', 'casa_legislativa_id')

        # Deleting field 'Parlamentar.partido'
        db.delete_column('modelagem_parlamentar', 'partido_id')

        # Deleting field 'Parlamentar.localidade'
        db.delete_column('modelagem_parlamentar', 'localidade')

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
        'modelagem.parlamentar': {
            'Meta': {'object_name': 'Parlamentar'},
            'casa_legislativa': ('django.db.models.fields.related.ForeignKey',
                                 [], {'to': "orm['modelagem.CasaLegislativa']",
                                      'null': 'True'}),
            'genero': ('django.db.models.fields.CharField', [],
                       {'max_length': '10', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [],
                   {'primary_key': 'True'}),
            'id_parlamentar': ('django.db.models.fields.CharField', [],
                               {'max_length': '100', 'blank': 'True'}),
            'localidade': ('django.db.models.fields.CharField', [],
                           {'max_length': '100', 'blank': 'True'}),
            'nome': ('django.db.models.fields.CharField', [],
                     {'max_length': '100'}),
            'partido': ('django.db.models.fields.related.ForeignKey', [],
                        {'to': "orm['modelagem.Partido']"})
        },
        'modelagem.partido': {
            'Meta': {'object_name': 'Partido'},
            'cor': ('django.db.models.fields.CharField', [],
                    {'max_length': '7'}),
            'id': ('django.db.models.fields.AutoField', [],
                   {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [],
                     {'max_length': '12'}),
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
                         'null': 'True',
                         'to': "orm['modelagem.Parlamentar']"}),
            'casa_legislativa': ('django.db.models.fields.related.ForeignKey',
                                 [], {'to': "orm['modelagem.CasaLegislativa']",
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
            'opcao': ('django.db.models.fields.CharField', [],
                      {'max_length': '10'}),
            'parlamentar': ('django.db.models.fields.related.ForeignKey', [],
                            {'to': "orm['modelagem.Parlamentar']"}),
            'votacao': ('django.db.models.fields.related.ForeignKey', [],
                        {'to': "orm['modelagem.Votacao']"})
        }
    }

    complete_apps = ['modelagem']