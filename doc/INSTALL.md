Passo a Passo da instalação
============================

1. Clonando o repositório
------------------------------

A primeira coisa que deve ser feita é o clone do projeto no *Github*. Para isso basta fazer:

        $ git clone https://github.com/radar-parlamentar/radar.git

2. Configuração do ambiente
---------------------------

O Radar Parlamentar funciona, tanto em produção quanto em desenvolvimento,
utilizando containers docker.
Para tanto, você precisa ter instalado em seu sistema operacional tanto o
*Docker* quanto o *docker-compose*.
Nossa instalação foi testada utilizando:

    * Docker 18.02.0-ce (Community Edition) build __fc4de44__
    * docker-compose 1.17.1

3. Rodar o projeto
------------------

Para rodar o projeto, agora precisamos de mais dois containers. O container
(**django**) que tem o projeto do radar em si e o servidor de aplicação (**uwsgi**) e o
container que possui o webserver (**nginx**).

Primeiro iniciaremos o servidor de aplicação.

    docker-compose up django

Pronto, o projeto já deve estar acessível via "http://localhost". =)

Caso queira que o console não fique preso o docker, utilize a flag `-d`.

Para limpar tudo, rode o comando:

    docker-compose down -v; -docker-compose rm -fsv; docker volume prune -f

Para interagir diretamente com o shell do django em execução:

    docker-compose exec django python manage.py shell

Para ver o log do Django:

     docker-compose exec django tail -f /var/log/radar/radar.log

3.1. Rodar o Projeto em Produção
--------------------------------
Para rodar o radar em produção você precisa definir duas variáveis de ambiente:

    - `RADAR_IS_PRODUCTION`: Define que o projeto está sendo executado em
        ambiente de produção. Isso habilita o Cache do Django e coloca o DEBUG
        como 'FALSE'
    - `RADAR_DB_PASSWORD`: Define a senha do banco de dados do radar em 
        produção

    RADAR_IS_PRODUCTION=True RADAR_DB_PASSWORD=senha docker-compose up -d django

4. Importação dos Dados
-----------------------

Primeiro crie um usuário administrativo do django:

     docker-compose exec django python manage.py createsuperuser

## CONTINUAR A REFATORAR DAQUI:
Depois inicie o Celery na pasta onde fica o manage.py:

    $./start_celery.sh

O Celery é um gerenciador de execução de tarefas assíncronas.

Para importar os dados basta acessar a URL: `http://127.0.0.1:8000/importar/<nome-curto-da-casa-legislativa>/`

Possíveis valores para `<nome-curto-da-casa-legislativa>`:

* Convenção Francesa: "conv"
* Camara Municipal de São Paulo: "cmsp"
* Senado: "sen"
* Câmara dos Deputados: "cdep"

Exemplo: para importar dados da Câmara Municipal de São Paulo basta acessar:

http://127.0.0.1:8000/importar/cmsp

Recomendamos inicialmente que você realize a importação dos dados Convenção Nacional Francesa (uma casa legislativa fictícia).

Obs: todas as importações são relativamente rápidas, exceto a da Câmara dos Deputados, que pode levar horas.

- Criando novos importadores:

http://radarparlamentar.polignu.org/importadores/

6. Executando os testes
---------------------------------
Rode o comando:

    docker-compose -f docker-compose-test.yml up

7. Instalação do Elasticsearch
-------------------

O Elasticsearch é um sistema de busca full-text em tempo real distribuido, escalável, altamente disponível e open-source.

Para instalar, primeiro é necessário baixar e descompactar o Elasticsearch disponível em: http://www.elastic.co/

    $ wget http://download.elastic.co/elasticsearch/elasticsearch/elasticsearch-1.5.1.zip
    $ unzip elasticsearch-1.5.1.zip

Também é necessário instalar o JDK7 do Java

Se o objetivo é iniciar o Elasticsearch apenas em um determinado endereço, é necessário editar o arquivo de configuração. No exemplo abaixo o Elasticsearch é iniciado apenas no endereço local 127.0.0.1.

    $ vim config/elasticsearch.yml
    descomentar e editar a linha network.bind_host: 127.0.0.1

Para iniciar o Elasticsearch:

    $ ./bin/elasticsearch -d

checar o endereço http://127.0.0.1:9200 se retorna um json.

Vamos ainda instalar o stem por dicionario em português, para aumentar a qualidade das buscas no elastic search (busca por ambientalista retornará ambiental).

    $wget https://addons.cdn.mozilla.net/user-media/addons/_attachments/6081/verificador_ortografico_para_portugues_do_brasil-2.5-3.2.12-fx+an+sm+fn+tb.xpi?filehash=sha256%3A4a0e3d4523185a8240bda56164ebb21d8787a563e0832907b27ea7ce39e36ff0

    descompactar e copiar arquivos .aff, .dic
    para pasta /elasticsearch-1.x.x/config/hunspell/pt_BR/
    onde /elasticsearch-1.x.x é o diretório do Elasticsearch

    renomear o arquivo .aff para pt_BR.aff
    renomear o arquivo .dic para pt_BR.dic
    e criar arquivo settings.yml com:
    ---
    ignore_case:          true
    strict_affix_parsing: true

Agora é preciso executar a importação dos dados no elastic search, o que deve ser feito após a importação dos dados das casas legislativas.

    $ python manage.py shell
    >>> from importadores import importador_elasticsearch as iel
    >>> iel.main()

Por fim, para testar:

    $ curl -XGET 'http://localhost:9200/radar_parlamentar/radar/_search?q=texto'
onde text é o texto que será analisado.
