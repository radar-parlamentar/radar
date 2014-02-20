Importação dos dados abertos para o banco de dados do Radar Parlamentar
===========

0. Convenção Nacional Francesa
-----------------------------------

    $ python manage.py shell
    $ from importadores import convencao
    $ convencao.main()

1.Câmara Municipal de São Paulo
-----------------------------------

    $ python manage.py shell
    $ from importadores import cmsp
    $ cmsp.main()

2.Senado
-----------------------------------

    $ python manage.py shell
    $ from importadores import senado
    $ senado.main()

3.Câmara dos Deputados
-----------------------------------

    $python manage.py shell
    $from importadores import camara
    $ camara.main()

4.Criando novos importadores:
-----------------------------------

http://radarparlamentar.polignu.org/importadores/



