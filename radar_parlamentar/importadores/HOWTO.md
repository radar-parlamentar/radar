HOW TO
===========

Importação dos dados abertos para o banco de dados do Radar Parlamentar
-------------------------------------------------------------------------

1.Câmara Municipal de São Paulo

    $ python manage.py shell
    $ from importadores import cmsp
    $ cmsp.main()

2.Senado

    $ python manage.py shell
    $ from importadores import senado
    $ senado.main()

3.Câmara dos Deputados

*Passo 1* - Gerar lista de IDs que existem:

    $ from importadores import camara
    $ finder = camara.ProposicoesFinder()
    $ finder.find_props_que_existem() # vai gerar dados/cdep/ids_que_existem.txt

*Passo 2* - Verificar dos IDs que existem, quais são os IDs que possuem votações associadas:

    $ props = finder.find_props_com_votacoes() # vai gerar dados/cdep/votadas.txt

*Passo 3* - importar para o banco de dados:

    $ camara.main()


