Projeto Django
====================

Para interagir com os objetos do django, vá na pasta do projeto (essa mesma, onde está este README) e execute:

    $ python manage.py shell 

Isso abre um *ipython* onde você tem acesso a suas coisas do Django, incluindo as classes do models

Pra usar as classes da app modelagem, basta um:

    from modelagem.models import *

**Atenção:** edite o atributo **DATABASES[DEFAULT][NAME]** no arquivo *radar_parlamentar/settings.py* para apontar para uma localização adequada em seu computador. Esta localização será onde o banco de dados do Django será criado.

Atualmente se você usar o banco de dados e o *settings.py* que vem do repositório, você não precisa fazer nada.

Caso o model seja alterado, o procedimento mais simples seria apagar o banco e executar o comando:

    $ python manage.py syncdb

No entanto, é muito custoso ter que executar todas as importações novamentes!

Então a partir de agora toda alteração no model deve gerar dois artefatos:

* o schema do banco de dados na versão v+1 (v era a versão atual); e
* um script SQL que aplica as alterações no banco sob o esquema v para que ele fique com a estrutura v+1;
nesse script é bem vindo o uso de valores default para novas colunas que venham a surgir.

Para levantar o servidor do Django:

    $ python manage.py runserver

Executando os testes automatizados:

    $ python manage.py test <nome_do_modulo>

Procure sempre criar mais testes automzatizados. Quando fizer mudanças, execute os testes novamente.

Esteja ciente de que algumas alterações (mudanças em algoritmos, por ex)podem alterar os valores gerados e quebrarem os testes. Nestes casos, altere os testes para utilziarem os novos valores gerados. Mas faça isso apenas quando você realmente esperar que sua alteração vá alterar esses valores (exemplo: quando consertei um bug que fez com que considerassemos algumas votações a mais, as posições dos partidos no gráfico foram *ligeiramente* alteradas, conforme esperado)

O banco de dados (.db) está no *.gitignore*, portanto para fazer o commit de alguma alteração do banco:

    $ git add -f radar_parlamentar.db

Quando se for criar uma nova importação, é preciso tomar o cuidado para criar um processo de importação incremental. Isso quer dizer que se rodamos o script com uma fonte de dados na versão v, e depois rodamos o mesmo script de importação com uma fonte de dados atualizada na versão v+1, as seguintes propriedades são desejáveis:

* os dados importados não devem ser replicados;
* os novos dados devem ser importados;
* a importação não deve travar.


