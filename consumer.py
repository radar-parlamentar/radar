# Pequeno script que baixa a votação do código florestal
# Fonte: http://rest.elkstein.org/2008/02/using-rest-in-python.html
import urllib2

tipo = 'pl'
num = '1876'
ano = '1999'
url = 'http://www.camara.gov.br/sitcamaraws/Proposicoes.asmx/ObterVotacaoProposicao?tipo='+tipo+'&numero='+num+'&ano='+ano
response = urllib2.urlopen(url).read()

print response

# Para fazer POST
#url = 'http:www;blbalab'
#params = urllib.urlencode({
#  'firstName':'John',
#  'lastName':'Doe'
#})
#response = urllib2.urlopen(url, params).read()
