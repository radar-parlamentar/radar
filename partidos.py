
def vetor_votacoes(partido, proposicoes):
  vetor = []
  for prop in proposicoes:
    for votacao in prop.votacoes:
      dic = votacao.por_partido()
      voto = dic[partido]
      vi = (voto.sim + 0.5*voto.abstencao) / (voto.sim + voto.nao + voto.abstencao)
      vetor.append(vi)
  return vetor  

def hello():
  print('Hello')

#def semelhanca(partido1, partido2, proposicoes):


