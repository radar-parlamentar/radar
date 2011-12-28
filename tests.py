#!/usr/bin/python3.2
# -*- coding: utf-8 -*-

from model import Deputado
from model import Votacao
from model import Proposicao
import model
import partidos
import unittest

class CamaraWS_Test(unittest.TestCase):

  def test_vetor_votacoes(self): 
    '''testa a geração de um vetor de votações'''

    # votações testadas (s,n,a):
    #(9,0,0) 
    #(0,8,1) 
    #(7,1,1) 
    #(3,3,3) 

    partido = 'arena'
    votacoes = []

    depSim = Deputado()
    depSim.partido = partido
    depSim.voto = model.SIM 
    depNao = Deputado()
    depNao.partido = partido
    depNao.voto = model.NAO
    depAbs = Deputado()
    depAbs.partido = partido
    depAbs.voto = model.ABSTENCAO 

    # 1a votação
    vot = Votacao()
    for i in range(0,9):
      vot.deputados.append(depSim)
    votacoes.append(vot)

    # 2a votação
    vot = Votacao()
    for i in range(0,8):
      vot.deputados.append(depNao)
    vot.deputados.append(depAbs)
    votacoes.append(vot)

    # 3a votação
    vot = Votacao()
    for i in range(0,7):
      vot.deputados.append(depSim)
    vot.deputados.append(depNao)
    vot.deputados.append(depAbs)
    votacoes.append(vot)

    # 4a votação
    vot = Votacao()
    for i in range(0,3):
      vot.deputados.append(depSim)
    for i in range(0,3):
      vot.deputados.append(depNao)
    for i in range(0,3):
      vot.deputados.append(depAbs)
    votacoes.append(vot)

    proposicao = Proposicao()
    proposicao.votacoes = votacoes
    proposicoes = [proposicao]
  
    # invocando a função testada
    vetor = partidos.vetor_votacoes(partido, proposicoes)

    # testando se tá certo
    expected = [1, 0.055555556, 0.833333333, 0.5]
    self.assertEqual(len(expected), len(vetor))
    for e, v in zip(expected, vetor):
      self.assertAlmostEqual(e, v, 5)


if __name__ == '__main__':
  unittest.main()

