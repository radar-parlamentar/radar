
from __future__ import unicode_literals
from django.test import TestCase
from modelagem.models import Parlamentar, Proposicao, Votacao, \
        PeriodoCasaLegislativa, Voto
from modelagem import utils
from modelagem.models import ANO, BIENIO, QUADRIENIO
from analises.analise import AnalisadorPeriodo
from datetime import datetime
from operator import itemgetter

class OrdenacaoTest(TestCase):

    def test_ordem_dos_parlamentares(self):
        pass
