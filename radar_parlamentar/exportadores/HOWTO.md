HOW TO
===========

Exportação dos dados existentes no banco de dados local para arquivos XML
-------------------------------------------------------------------------

1.Exportar todos os registros existentes

    $ python manage.py shell
    $ from exportadores import exportar
    $ exportar.main()

2.Exportar apenas os objetos desejados

*Exemplo 1* - Exportar os registros de Partidos:

    $ python manage.py shell
    $ from exportadores import exportar
    $ exportar.serialize_partido()

O mesmo pode ser feito para os seguintes tipos de objetos da models.py:
	# exportar.serialize_partido()
	# exportar.serialize_casa_legislativa()
	# exportar.serialize_parlamentar()
	# exportar.serialize_legislatura()
	# exportar.serialize_proposicao()
	# exportar.serialize_votacao()
	# exportar.serialize_voto()

Exportação dos dados existentes no banco de dados local para CSV
-------------------------------------------------------------------------

    data_ini = parse_datetime('2010-06-01 0:0:0')
    data_fim = parse_datetime('2010-06-30 0:0:0')
    exportador = ExportadorCSV('sen', data_ini, data_fim)
    exportador.exportar_csv()

Arquivo é gerado em exportadores/dados/votes.csv

Obs: os dados exportados nessa opção visam objetivamente exportar os dados que precisamos para as nossas análises em R.



