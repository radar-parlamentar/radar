
def vetor_votacao(partido, proposicoes):
  vetor = []
  for votacao in prop.votacoes:
    dic = votacao.por_partido()
    voto = dic[partido]
    vi = (voto.sim + 0,5*voto.abstencao) / (voto.sim + voto.nao + voto.abstencao)
    vetor.append(vi)
  return vetor  

#def semelhanca(partido1, partido2, proposicoes):


