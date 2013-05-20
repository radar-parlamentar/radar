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
