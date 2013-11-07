# coding=utf8

# Copyright (C) 2013, Leonardo Leite
#
# This file is part of Radar Parlamentar.
#
# Radar Parlamentar is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Radar Parlamentar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Radar Parlamentar.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals
from models import *
from models import MES
import datetime
from calendar import monthrange

class MandatoLists:

    def get_mandatos_municipais(self, ini_date, end_date):
        """Retorna datas do início de cada mandato no período compreendido entre ini_date e end_date
            Argumentos:
                ini_date, end_date -- tipo date
            Retorno:
                lista do tipo date
            Obs: início de cada mandato é sempre em 1 de janeiro
        """
        ANO_INICIO_DE_ALGUM_MANDATO = 2009
        ANO_DE_REFERENCIA = ANO_INICIO_DE_ALGUM_MANDATO-4*500 # suficientemente no passado 
        defasagem = (abs(ANO_DE_REFERENCIA - ini_date.year)) % 4
        y = ini_date.year - defasagem 
        mandatos = []
        while y <= end_date.year:
            date_ini_mandato = datetime.date(y,1,1) 
            mandatos.append(date_ini_mandato)
            y += 4
        return mandatos
    
    
class PeriodosRetriever:
    """Recupera os períodos com um mínimo de votações de uma casa legislativa entre inicio e fim
        
        Argumentos:        
          casa_legislativa: um objeto CasaLegislativa. Necessário para acrescentar a cada
              objeto PeriodoCasaLegislativa da lista o número de votações que houve no mesmo.
          periodicidade: uma constante em PERIODOS (ex. ANO, SEMESTRE).
          inicio, fim: objetos datetime. Se não especificados, utiliza todo o histórico da casa
          numero_minimo_de_votacoes: periodos com menos votações são excluídos da lista. default é 1.
        Retorna:
            Uma lista de objetos do tipo PeriodoCasaLegislativa.
        Detalhes:
        1) Se a data de início for por exemplo 15/08/1999 e a periodicidade for quadrianual,
            bianual, anual, ou semestral, o primeiro período irá começar em 01/01/1999. Se
            a periodicidade for mensal com a mesma data de início, o primeiro período irá 
            começar em 01/08/1999. Analogamente todos os períodos anuais terminam em 31 de
            dezembro e assim por diante, seguindo o calendário. Nunca será retornado um
            período com datas "quebradas" na lista.
        2) É garantido que cada período esteja inteiramente dentro de um período de mandato.
            Períodos de mandatos do municipal são grupos de 4 anos começando em 2009 + i*4, i \in Z 
            Períodos de mandatos do federal/estadual são grupos de 4 anos começando em 2011 + i*4, i \in Z
            WARNING: Brazil dependent code! 
    """
    
    def __init__(self, casa_legislativa, periodicidade, ini_date=None, end_date=None, numero_minimo_de_votacoes=1):
        self.casa_legislativa = casa_legislativa
        self.periodicidade = periodicidade
        self.ini_date = ini_date
        self.end_date = end_date
        self.numero_minimo_de_votacoes = numero_minimo_de_votacoes
    
    def get_periodos(self):
        if (self.ini_date == None):
            # TODO a query abaixo poderia usar um ORDER BY
            votacao_datas = [votacao.data for votacao in Votacao.objects.filter(proposicao__casa_legislativa=self.casa_legislativa)]
            if votacao_datas:
                return []
            self.ini_date = min(votacao_datas)
            self.end_date = max(votacao_datas)
        data_inicial = self._inicio()
        data_fim = self._fim()
        delta = self._periodo_to_delta()
        periodos_candidatos = []
        dias_que_faltam = 1
        while dias_que_faltam > 0:
            mes = self.ini_date.month
            ano = self.ini_date.year
            mes = mes + delta
            while mes > 12:
                mes = mes - 12
                ano = ano + 1
            data_final = self.end_date.replace(month=mes,year=ano)
            # ir ate ultimo dia do mes:
            dia_final = monthrange(data_final.year,data_final.month)[1]
            data_final = data_final.replace(day=dia_final)
            quantidade_votacoes = self.casa_legislativa.num_votacao(data_inicial,data_final)
            periodo = PeriodoCasaLegislativa(data_inicial, data_final, quantidade_votacoes)
            periodos_candidatos.append(periodo)
            data_inicial = data_final + datetime.timedelta(days=1)
            delta_que_falta = data_fim - data_final
            dias_que_faltam = delta_que_falta.days
        periodos_aceitos = PeriodoCasaLegislativa._filtra_periodos_com_minimo_de_votos(periodos_candidatos, self.numero_minimo_de_votacoes)
        return periodos_aceitos

    def _filtra_periodos_com_minimo_de_votos(self, periodos_candidatos, numero_minimo_de_votacoes):
        return [ p for p in periodos_candidatos if p.quantidade_votacoes >= numero_minimo_de_votacoes ]

    def _periodo_to_delta(self):
        delta_numero = {QUADRIENIO:47,BIENIO:23,ANO:11,MES:0,SEMESTRE:5}
        delta = delta_numero[self.periodicidade]
        return delta
    
    def _inicio(self):
        dia_inicial = 1
        ano_inicial = self.ini_date.year
        if self.periodicidade == MES:
            mes_inicial = self.ini_date.month
        elif self.periodicidade in [SEMESTRE,ANO,BIENIO,QUADRIENIO]:
            mes_inicial = 1
        return datetime.date(ano_inicial,mes_inicial,dia_inicial)

    def _fim(self):
        ano_fim = self.end_date.year
        if self.periodicidade == MES:
            mes_fim = self.end_date.month
        elif self.periodicidade == SEMESTRE:
            if self.end_date.month <= 6:
                mes_fim = 6
            else:
                mes_fim = 12
        else:
            mes_fim = 12
        dia_fim = monthrange(ano_fim,mes_fim)[1]
        return datetime.date(ano_fim,mes_fim,dia_fim)
    
    
    
    
    
    
    