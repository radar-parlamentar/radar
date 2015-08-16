Passo a Passo da instalação
============================

1. Clonando o repositório
------------------------------
    
A primeira coisa que deve ser feita é o clone do projeto no *Github*. Para isso basta fazer:

        $ git clone https://github.com/radar-parlamentar/radar.git

2. Configuração do ambiente
------------------------------

Instale os pacotes (apt-get):

    * libpq-dev
    * postgresql
    * postgresql-contrib
    * sqlite3
    * python-dev
    * curl
    * python-pip
    * python-virtualenv
    * rabbitmq-server

Crie a pasta /tmp/django_cache

* **Configuração utilizando o virtualenv**

Para quem não conheçe, o [virtualenv](http://www.virtualenv.org "Virtual Env") cria um *conteiner* com todo um ambiente Python "limpo" para você instalar os pacotes separadamente do seu Sistema Operacional.

Depois de clonar o projeto, vamos criar agora o nosso "Virtual Enviroment":

    $ virtualenv path/para/a/pasta/do/projeto/clonado
    $ cd path/para/a/pasta/do/projeto/clonado
    $ source bin/activate

Agora, dentro da nossa pasta do projeto teremos disponíveis todas variáveis de ambiente em um conteiner vazio para trabalharmos a vontade sem interferir no nosso Sistema Operacional

Para instalar todas as dependencias Python necessárias para o nosso projeto rodar, basta executar:

    $ pip install -r radar_parlamentar/requirements.txt

Este comando vai buscar todas as dependências definidas no arquivo *requirements.txt* e as intalará em nosso *conteiner* do *virtualenv*

Caso queira sair do *virtualenv* basta digitar:

    $ deactivate

ATENÇÃO: toda vez que você for trabalhar no radar é preciso ativar o virtual env! (source bin/activate)

Observações
-------------

* Se por algum motivo a versão do *Django* instalada for a 1.5, possivelmente um erro ocorrerá devido a depreciação de uma lib utilizada no projeto. Este erro pode ser visto ao executar o programa.

* Caso ao tentar executar o *manage.py* um erro parecido com o abaixo ocorra:

    * **UnicodeDecodeError**: *'ascii' codec can't decode byte 0xc3 in position 47: ordinal not in range(128)*, existe um problema na leitura do python em relação a caracteres especiais. Bem provavel que esse erro ocorra caso a pasta que você criou para alocar as pastas do projeto esteja com c cedilha ou acentos. Esse erro provavelmente acontecerá no arquivo *models.py* dentro da pasta *modelagem*.
    Você pode seguir a solução abaixo ou simplesmente renomear a pasta.

    * **Solução para o problema acima**:
        Abra o arquivo *models.py* e na seguinte linha:

            LISTA_PARTIDOS = os.path.join('recursos/partidos.txt',MODULE_DIR)

        adicione um *.decode("utf-8")* no final, ficando da seguinte forma:
            
            LISTA_PARTIDOS = os.path.join('recursos/partidos.txt',MODULE_DIR).decode("utf-8")

3. Banco de dados
--------------------------

Você deve configurar um banco de dados PostgreSQL para ser utilizado pelo Radar.

Caso ainda não tenha instalado o PostgreSQL:

	$ sudo apt-get install postgresql postgresql-contrib

Configurando o banco:

    $ sudo su - postgres
    $ createdb radar
    $ createuser radar -P
    escolha a senha
    $ psql
    # GRANT ALL PRIVILEGES ON DATABASE radar TO radar;
    saia do psql (ctrl+d)
    volte a ser o usuário normal (ctrl+d)
    $ echo "localhost:5432:radar:radar:<SENHA>" > ~/.pgpass
    $ chmod 600 ~/.pgpass

Crie o arquivo settings/development.py com base no arquivo settings/development.py.template.
No arquivo development.py, insira a senha do usuário radar do PostgreSQL .

Ao rodar python manage.py runserver no ambiente de desenvolvimento, será usado as configurações settings/development.py.
    
Para criar as tabelas do Radar Parlamentar:

    $ python manage.py syncdb 
    $ python manage.py migrate
        
Agora, pode-se importar todos os dados com os Importadores!!


4. Importação dos Dados
-------------------

Primeiro crie um usuário administrativo do django:

     $python manage.py createsuperuser

Depois inicie o Celery na pasta onde fica o manage.py:

     $celery -A importadores worker -l info --concurrency 1
     
O Celery é um gerenciador de execução de tarefas assíncronas.

Para importar os dados basta acessar a URL: http://127.0.0.1:8000/importar/<nome-curto-da-casa-legislativa>/

Possíveis valores para <nome-curto-da-casa-legislativa>:

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


5. Configuração do South
-------------------------

South é uma ferramenta que funciona como uma camada de migração, independente do banco de dados. Eventualmente, seu models.py vai ser modificado e o South vai identificar e realizar as mudanças correspondentes no seu banco por você, sem a necessidade de utilizar comandos SQL e sem perda de dados.

Quando ocorrer alterações na model, digite no terminal:
	
	$ python manage.py schemamigration modelagem --auto
	$ python manage.py migrate modelagem
	
Observação: Cuidado ao diminuir o tamanho dos campos. Podem existir dados com tamanho superior ao tamanho desejado.

6. Conferindo se está tudo certo
---------------------------------
Execute o script de testes e testes unitários:
    
    $ source tests.sh


Inicie o servidor do Django:

    $ python manage.py runserver

Considerando que você importou os dados da Convenção Nacional Francesa, acesse **http://127.0.0.1:8000/analises/analise/conv** e verifique se o gráfico aparece corretamente (um gráfico estático com três circunferâncias, dispostos aproximadamente como um triângulo equilátero).




7. Instalação do Elasticsearch
-------------------

O Elasticsearch é um sistema de busca full-text em tempo real distribuido, escalável, altamente disponível e open-source.

Para instalar, primeiro é necessário baixar e descompactar o Elasticsearch disponível em: http://www.elastic.co/

    $ wget http://download.elastic.co/elasticsearch/elasticsearch/elasticsearch-1.5.1.zip
    $ unzip elasticsearch-1.5.1.zip

Também é necessário instalar o JDK7 do Java

Se o objetivo é iniciar o Elasticsearch apenas em um determinado endereço, é necessário editar o arquivo de configuração. No exemplo abaixo o Elasticsearch é iniciado apenas no endereço local 127.0.0.1.

    $ vim config/elasticsearch.yml
    descomentar e editar a linha network.bind_host=127.0.0.1

Por fim, iniciar o Elasticsearch

    $ ./bin/elasticsearch -d

checar o endereço http://127.0.0.1:9200 se retorna um json.

8. Engine de busca do Elasticsearch
-------------------

Para melhorar a qualidade nos resultados de busca, uma proposta é usar uma estrategia de reducao de palavras chamada de stem.

Com o stem, a palavra é reduzida para sua raiz e, através dessa, são buscadas todas suas ramificações. Por exemplo, se o usuário buscar ambientalista, o processo de stem reduzirá ambientalista para ambiental e buscará todas as suas flexões como ambientistas, ambientais, ambientalismo...

Existem duas propostas para essa redução: algoritmo ou dicionário

O algoritmo define um conjunto de regras para reduzir qualquer palavra. No dicionário, a redução e feita fazendo a busca da palavra em um dicionário.

Comparando o algoritmo com o dicionário,o dicionário e mais preciso, porém o tempo de buscar uma palavra é consideravel, enquanto isso, no algoritmo, a execução e rápida porém com redução na precisão da redução.

abaixo é mostrada a configuracao necessária para instalar o stem por dicionario em português num indice do Elasticsearch.

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

é necessário recriar o índice com a novo analisador. Supondo que o Elasticsearch está em localhost:9200: 
    
    $ curl -XDELETE 'http://localhost:9200/radar_parlamentar/'
    $ curl -XPUT http://localhost:9200/radar_parlamentar/ -d '
    {
    "settings": {
        "analysis": {
            "analyzer": {
                "my_analyzer": {
                    "tokenizer": "standard",
                    "filter": ["standard", "pt_BR", "lowercase","portuguese_stop","asciifolding"]
            }
            },
            "filter": {
                "my_stemmer": {
                    "type": "stemmer",
                "name": "brazilian"
                },
                 "portuguese_stop": {
                     "type":       "stop",
                     "stopwords":  "_brazilian_" 
                },
                 "pt_BR": {
                     "type":       "hunspell",
                     "language":  "pt_BR" 
                }
            }
        }
    }}'

    $ curl -XPUT http://localhost:9200/radar_parlamentar/radar/_mapping?ignore_conflicts=true -d '
    {
      "radar" : {
        "_all" : {"enabled" : true, "analyzer": "my_analyzer"},
        "properties" : {
          "casa_legilativa_local" : {
            "type" : "string"
          },
          "casa_legislativa_atualizacao" : {
            "type" : "date",
            "format" : "dateOptionalTime"
          },
          "casa_legislativa_esfera" : {
            "type" : "string"
          },
          "casa_legislativa_id" : {
            "type" : "long"
          },
          "casa_legislativa_nome" : {
            "type" : "string"
          },
          "casa_legislativa_nome_curto" : {
            "type" : "string"
          },
          "proposicao_ano" : {
            "type" : "string"
          },
          "proposicao_data_apresentacao" : {
            "type" : "date",
            "format" : "dateOptionalTime"
          },
          "proposicao_descricao" : {
            "type" : "string"
          },
          "proposicao_ementa" : {
            "type" : "string",
            "analyzer": "my_analyzer"
          },
          "proposicao_id" : {
            "type" : "long"
          },
          "proposicao_id_prop" : {
            "type" : "string"
          },
          "proposicao_indexacao" : {
            "type" : "string",
            "analyzer": "my_analyzer"
          },
          "proposicao_numero" : {
            "type" : "string"
          },
          "proposicao_sigla" : {
            "type" : "string"
          },
          "proposicao_situacao" : {
            "type" : "string"
          },
          "votacao_data" : {
            "type" : "date",
            "format" : "dateOptionalTime"
          },
          "votacao_descricao" : {
            "type" : "string",
            "analyzer": "my_analyzer"
          },
          "votacao_id" : {
            "type" : "long"
          },
          "votacao_id_vot" : {
            "type" : "string"
          },
          "votacao_resultado" : {
            "type" : "string"
          }
    }}}'

Por fim, para testar: 

    $ curl -XGET 'http://localhost:9200/radar_parlamentar/_analyze?analyzer=my_analyzer&text=ambientes
onde text é o texto que será analisado.

