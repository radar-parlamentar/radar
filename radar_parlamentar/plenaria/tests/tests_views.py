from django.test import TestCase
from modelagem.models import Proposicao
from plenaria import views


class ViewsTest(TestCase):

    def test_identificador(self):
        proposicao = Proposicao()
        proposicao.sigla = 'PL'
        proposicao.numero = '42'
        proposicao.ano = '1979'
        resultado = views.identificador(proposicao)
        self.assertEqual(resultado, "PL-42-1979")
