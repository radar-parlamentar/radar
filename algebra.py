import math

def norma(vetor):
  sum = 0
  for v_i in vetor:
    sum += v_i*v_i
  return math.sqrt(sum)

def normaliza(vetor):
  normalizado = []
  n = norma(vetor)
  for v_i in vetor:
    normalizado.append(v_i / n)
  return normalizado

def prod_escalar(vetor1, vetor2):
  sum = 0
  for v1, v2 in zip(vetor1, vetor2):
    sum += v1*v2
  return sum
