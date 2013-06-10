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
    $ finder.find_props_que_existem_brute_force(IDS_FILE, ID_MIN, ID_MAX) # vai gerar IDS_FILE

onde temos utilizado *ID_MIN=1 e ID_MAX=600000*

*Passo 2* - Verificar dos IDs que existem, quais são os IDs que possuem votações associadas:

    $ props = finder.parse_ids_que_existem(IDS_FILE, VOTADAS_FILE) # vai gerar VOTADAS_FILE

*Passo 3* - importar para o banco de dados:

    $ camara.main()


