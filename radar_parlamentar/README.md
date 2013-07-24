Projeto Django
====================

Para interagir com os objetos do django, vá na pasta do projeto (essa mesma, onde está este README) e execute:

    $ python manage.py shell 

Isso abre um interpretador python onde você tem acesso a suas coisas do Django, incluindo as classes do models

Pra usar as classes da app modelagem, basta um:

    from modelagem.models import *

Para levantar o servidor do Django:

    $ python manage.py runserver

Executando os testes automatizados:

    $ python manage.py test <nome_do_modulo>

Procure sempre criar mais testes automzatizados. Quando fizer mudanças, execute os testes novamente.

Esteja ciente de que algumas alterações (mudanças em algoritmos, por ex) podem alterar os valores gerados e quebrarem os testes. Nestes casos, altere os testes para utilziarem os novos valores gerados. Mas faça isso apenas quando você realmente esperar que sua alteração vá alterar esses valores (exemplo: quando consertei um bug que fez com que considerassemos algumas votações a mais, as posições dos partidos no gráfico foram *ligeiramente* alteradas, conforme era de se esperar).


Alteração nos models
-----------------------

Caso o model seja alterado, o procedimento mais simples seria apagar o banco e executar o comando:

    $ python manage.py syncdb

No entanto, é muito custoso ter que executar todas as importações novamentes!

Então recomenda-se que toda alteração no model deve gerar dois artefatos:

* o schema do banco de dados na versão v+1 (v era a versão atual); e
* um script SQL que aplica as alterações no banco sob o esquema v para que ele fique com a estrutura v+1;
nesse script é bem vindo o uso de valores default para novas colunas que venham a surgir.


