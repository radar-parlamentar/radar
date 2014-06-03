Passo a Passo da instalação
============================

1. Clonando o repositório
------------------------------
    
A primeira coisa que deve ser feita é o clone do projeto no *Github*. Para isso basta fazer:

        $ git clone https://github.com/leonardofl/radar_parlamentar.git

2. Configuração do ambiente
------------------------------

Após clonar o repositório você tem as 3 opções abaixo para instalação:


* **Configuração Manual**

    * **Django 1.4.5**: Framework web utilizado no desenvolvimento do projeto. Download: [Django](https://www.djangoproject.com/download/)

    * **numpy**: Biblioteca que permite a criação de arrays de objetos n-dimensionais e realização de operações diversas sobre o mesmo.
        Download: [numpy](http://sourceforge.net/projects/numpy/files/)

    * **matplotlib**: Biblioteca utilizada no projeto para plotar gráficos 2D que são usados na apresentação dos dados abertos obtidos.
        Download: [matplotlib](http://matplotlib.org/downloads.html)

    * É preciso também criar o diretório /tmp/django_cache.


* **Configuração utilizando Scripts**

    * **Arch Linux**

    Depois de clonar o repositório, basta executar o script específico para o Arch Linux que se encontra no projeto:

        $ ./setup/setup_arch.sh

    E o script fará todo o trabalho para você.

    * **Ubuntu**

    Depois de clonar o repositório, basta executar o script específico para o Ubuntu que se encontra no projeto:

        $ ./setup/setup_ubuntu.sh

    E o script fará todo o trabalho para você.


* **Configuração utilizando o virtualenv**

Para quem não conheçe, o [virtualenv](http://www.virtualenv.org "Virtual Env") cria um *conteiner* com todo um ambiente Python "limpo" para você instalar os pacotes separadamente do seu Sistema Operacional.

Depois de clonar o projeto, vamos preparar o ambiente para utilizar o *virtualenv* e o *pip*, para isto vamos executar as seguintes instalações (os comandos abaixo são baseados em sistemas debian-like, para outros sistemas, basta modificar o gerenciador de pacotes e fazer os ajustes):

    $ sudo apt-get install python-pip
    $ sudo pip install virtualenv

Feito isso, vamos criar agora o nosso "Virtual Enviroment":

    $ virtualenv path/para/a/pasta/do/projeto/clonado
    $ cd path/para/a/pasta/do/projeto/clonado
    $ source bin/activate

Agora, dentro da nossa pasta do projeto teremos disponíveis todas variáveis de ambiente em um conteiner vazio para trabalharmos a vontade sem interferir no nosso Sistema Operacional

Para instalar todas as dependencias Python necessárias para o nosso projeto rodar, basta executar:

    $ sudo pip install -r requirements.txt

Este comando vai buscar todas as dependencias definidas no arquivo *requirements.txt* e as intalará em nosso *conteiner* do *virtualenv*

Caso queira sair do *virtualenv* basta digitar:

    $ deactivate


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

Você deve configurar um banco de dados MySQL para ser utilizado pelo Radar.

Para configurar o MySql como banco de dados:
Instalação:

	$ sudo apt-get install mysql-server
	$ sudo apt-get install python-mysqldb

Deve-se criar um usuário "root" e o banco dentro do próprio MySQL.

    $ mysql -u root -p 
    Enter password: root
    #Entra no shell do mysql
    
    mysql>CREATE DATABASE radar;
    mysql>quit

Edite o arquivo settings/development.py* e insira a senha do seu usuário do mysql (pode ser o root).

Ao rodar python manage.py runserver no ambiente de desenvolvimento, será usado as configurações settings/development.py.

<b>Em ambiente de desenvolvimento:</b>

Criar development.py baseado em development.py.template.


<b>Em ambiente de produção:</b>

Criar production.py baseado em production.py.template.

No ambiente de produção é necessário exportar a variável de ambiente export 	DJANGO_SETTINGS_MODULE='settings.production'. Para isso basta executar o script is_prod.sh. Referência do DJANGO: (https://code.djangoproject.com/wiki/SplitSettings)


*Importante dizer que deve-se atribuir False a variável DEBUG em settings/development.py ou production.py (em ambiente de produção) para ativar a visualização da página de erro default 404.

    
Para criar as tabelas do Radar Parlamentar:

    $ python manage.py syncdb #Cria todas as tabelas
    
Agora, pode-se importar todos os dados com os Importadores!!



4. Importação dos Dados
-------------------

Para importar os dados basta digitar o comando:
$ python manage.py shell
$ from importadores import importador

Para selecionar os dados que serão importados, basta passar como parametro uma lista com os nomes reduzidos das casas legislativas. 

* Convenção Francesa: conv
* Camara Municipal de São Paulo: cmsp
* Senado: sen
* Câmara dos Deputados: cdep

Por exemplo, caso deseje importar somente a base Convencao e Senado, então faça:

        $importador.main(['conv', 'sen']) 


Caso deseje importar todos:

        $ importador.main(['conv', 'sen', 'cmsp', 'cdep'])

- Criando novos importadores:

http://radarparlamentar.polignu.org/importadores/



Recomendamos inicialmente que você realize a importação dos dados Convenção Nacional Francesa (uma casa legislativa fictícia).

5. Configuração do South
-------------------------

South é uma ferramenta que funciona como uma camada de migração, independente do banco de dados. Eventualmente, seu models.py vai ser modificado e o South vai identificar e realizar as mudanças correspondentes no seu banco por você, sem a necessidade de utilizar comandos SQL e sem perda de dados.

* Instalação:

	$ sudo pip install South 
	
Adicionar o South no `INSTALLED_APPS` no arquivo `settings/defaults.py`.

	$ python manage.py syncdb 
	$ python manage.py convert_to_south modelagem

* Como usar:

Quando ocorrer alterações na model, digite no terminal:
	
	$ python manage.py schemamigration modelagem --auto
	$ python manage.py migrate modelagem
	
Observação: Cuidado ao diminuir o tamanho dos campos. Podem existir dados com tamanho superior ao tamanho desejado.

6. Conferindo se está tudo certo
---------------------------------
Execute o script de testes e testes unitários:
    
    $ ./tests.sh
    $ ./unit_tests.sh


Inicie o servidor do Django:

    $ python manage.py runserver

Considerando que você importou os dados da Convenção Nacional Francesa, acesse **http://127.0.0.1:8000/analises/analise/conv** e verifique se o gráfico aparece corretamente (um gráfico estático com três circunferâncias, dispostos aproximadamente como um triângulo equilátero).




