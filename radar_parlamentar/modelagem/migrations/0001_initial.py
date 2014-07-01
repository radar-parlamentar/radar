# -*- coding: utf-8 -*-

from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Indexadores'
        db.create_table('modelagem_indexadores', (
            ('id', self.gf('django.db.models.fields.AutoField')(
                primary_key=True)),
            ('termo', self.gf('django.db.models.fields.CharField')(
                max_length=120)),
            ('principal', self.gf('django.db.models.fields.BooleanField')(
                default=False)),
        ))
        db.send_create_signal('modelagem', ['Indexadores'])

        # Adding model 'Partido'
        db.create_table('modelagem_partido', (
            ('id', self.gf('django.db.models.fields.AutoField')(
                primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(
                max_length=12)),
            ('numero', self.gf('django.db.models.fields.IntegerField')()),
            ('cor', self.gf('django.db.models.fields.CharField')(
                max_length=7)),
        ))
        db.send_create_signal('modelagem', ['Partido'])

        # Adding model 'CasaLegislativa'
        db.create_table('modelagem_casalegislativa', (
            ('id', self.gf('django.db.models.fields.AutoField')(
                primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(
                max_length=100)),
            ('nome_curto', self.gf('django.db.models.fields.CharField')
             (unique=True, max_length=50)),
            ('esfera', self.gf('django.db.models.fields.CharField')
                (max_length=10)),
            ('local', self.gf('django.db.models.fields.CharField')
                (max_length=100)),
            ('atualizacao', self.gf('django.db.models.fields.DateField')
             (null=True, blank=True)),
        ))
        db.send_create_signal('modelagem', ['CasaLegislativa'])

        # Adding model 'Parlamentar'
        db.create_table('modelagem_parlamentar', (
            ('id', self.gf('django.db.models.fields.AutoField')
                (primary_key=True)),
            ('id_parlamentar', self.gf('django.db.models.fields.CharField')
             (max_length=100, blank=True)),
            ('nome', self.gf('django.db.models.fields.CharField')
                (max_length=100)),
            ('genero', self.gf('django.db.models.fields.CharField')
             (max_length=10, blank=True)),
        ))
        db.send_create_signal('modelagem', ['Parlamentar'])

        # Adding model 'Legislatura'
        db.create_table('modelagem_legislatura', (
            ('id', self.gf('django.db.models.fields.AutoField')
                (primary_key=True)),
            ('parlamentar', self.gf(
                'django.db.models.fields.related.ForeignKey')
             (to=orm['modelagem.Parlamentar'])),
            ('casa_legislativa', self.gf(
                'django.db.models.fields.related.ForeignKey')
             (to=orm['modelagem.CasaLegislativa'], null=True)),
            ('inicio', self.gf('django.db.models.fields.DateField')
                (null=True)),
            ('fim', self.gf('django.db.models.fields.DateField')(null=True)),
            ('partido', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['modelagem.Partido'])),
            ('localidade', self.gf('django.db.models.fields.CharField')
             (max_length=100, blank=True)),
        ))
        db.send_create_signal('modelagem', ['Legislatura'])

        # Adding model 'Proposicao'
        db.create_table('modelagem_proposicao', (
            ('id', self.gf('django.db.models.fields.AutoField')
                (primary_key=True)),
            ('id_prop', self.gf('django.db.models.fields.CharField')
             (max_length=100, blank=True)),
            ('sigla', self.gf('django.db.models.fields.CharField')
                (max_length=10)),
            ('numero', self.gf('django.db.models.fields.CharField')
                (max_length=10)),
            ('ano', self.gf('django.db.models.fields.CharField')
                (max_length=4)),
            ('ementa', self.gf('django.db.models.fields.TextField')
                (blank=True)),
            ('descricao', self.gf('django.db.models.fields.TextField')
                (blank=True)),
            ('indexacao', self.gf('django.db.models.fields.TextField')
                (blank=True)),
            ('data_apresentacao', self.gf(
                'django.db.models.fields.DateField')(null=True)),
            ('situacao', self.gf('django.db.models.fields.TextField')
                (blank=True)),
            ('casa_legislativa', self.gf(
                'django.db.models.fields.related.ForeignKey')
             (to=orm['modelagem.CasaLegislativa'], null=True)),
            ('autor_principal', self.gf(
                'django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('modelagem', ['Proposicao'])

        # Adding M2M table for field autores on 'Proposicao'
        m2m_table_name = db.shorten_name('modelagem_proposicao_autores')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True,
                                    auto_created=True)),
            ('proposicao', models.ForeignKey(
                orm['modelagem.proposicao'], null=False)),
            ('parlamentar', models.ForeignKey(
                orm['modelagem.parlamentar'], null=False))
        ))
        db.create_unique(m2m_table_name, ['proposicao_id', 'parlamentar_id'])

        # Adding model 'Votacao'
        db.create_table('modelagem_votacao', (
            ('id', self.gf('django.db.models.fields.AutoField')
                (primary_key=True)),
            ('id_vot', self.gf('django.db.models.fields.CharField')
             (max_length=100, blank=True)),
            ('descricao', self.gf('django.db.models.fields.TextField')
                (blank=True)),
            ('data', self.gf('django.db.models.fields.DateField')
             (null=True, blank=True)),
            ('resultado', self.gf('django.db.models.fields.TextField')
                (blank=True)),
            ('proposicao', self.gf(
                'django.db.models.fields.related.ForeignKey')
             (to=orm['modelagem.Proposicao'], null=True)),
        ))
        db.send_create_signal('modelagem', ['Votacao'])

        # Adding model 'Voto'
        db.create_table('modelagem_voto', (
            ('id', self.gf('django.db.models.fields.AutoField')
                (primary_key=True)),
            ('votacao', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['modelagem.Votacao'])),
            ('legislatura', self.gf(
                'django.db.models.fields.related.ForeignKey')
             (to=orm['modelagem.Legislatura'])),
            ('opcao', self.gf('django.db.models.fields.CharField')
                (max_length=10)),
        ))
        db.send_create_signal('modelagem', ['Voto'])

    def backwards(self, orm):
        # Deleting model 'Indexadores'
        db.delete_table('modelagem_indexadores')

        # Deleting model 'Partido'
        db.delete_table('modelagem_partido')

        # Deleting model 'CasaLegislativa'
        db.delete_table('modelagem_casalegislativa')

        # Deleting model 'Parlamentar'
        db.delete_table('modelagem_parlamentar')

        # Deleting model 'Legislatura'
        db.delete_table('modelagem_legislatura')

        # Deleting model 'Proposicao'
        db.delete_table('modelagem_proposicao')

        # Removing M2M table for field autores on 'Proposicao'
        db.delete_table(db.shorten_name('modelagem_proposicao_autores'))

        # Deleting model 'Votacao'
        db.delete_table('modelagem_votacao')

        # Deleting model 'Voto'
        db.delete_table('modelagem_voto')

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
            'casa_legislativa': ('django.db.models.fields.related.ForeignKey',
                                 [],
                                 {'to': "orm['modelagem.CasaLegislativa']",
                                  'null': 'True'}),
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
            'legislatura': ('django.db.models.fields.related.ForeignKey', [],
                            {'to': "orm['modelagem.Legislatura']"}),
            'opcao': ('django.db.models.fields.CharField', [],
                      {'max_length': '10'}),
            'votacao': ('django.db.models.fields.related.ForeignKey', [],
                        {'to': "orm['modelagem.Votacao']"})
        }
    }

    complete_apps = ['modelagem']
