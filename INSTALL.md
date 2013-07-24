Passo a Passo da instalação
============================

Clonando o repositório
------------------------------
    
    A primeira coisa que deve ser feita é o clone do projeto no *Github*. Para isso basta fazer:

        $ git clone https://github.com/leonardofl/radar_parlamentar.git

Configuração do ambiente
------------------------------

Após clonar o repositório você tem as 3 opções abaixo para instalação


* **Configuração Manual**

    * **Django 1.4.5**: Framework web utilizado no desenvolvimento do projeto. Download: [Django](https://www.djangoproject.com/download/)

    * **numpy**: Biblioteca que permite a criação de arrays de objetos n-dimensionais e realização de operações diversas sobre o mesmo.
        Download: [numpy](http://sourceforge.net/projects/numpy/files/)

    * **matplotlib**: Biblioteca utilizada no projeto para plotar gráficos 2D que são usados na apresentação dos dados abertos obtidos.
        Download: [matplotlib](http://matplotlib.org/downloads.html)


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

    $ pip install -r requirements.txt

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

Banco de dados
--------------------------

Você deve configurar um banco de dados MySQL para ser utilizado pelo Radar.

Para mais detalhes, confira o arquivo **radar_parlamentar/BD_CONFIG.md**.

Para que seu banco possua dados, você deve realizar os processos de importação de dados descritos em **radar_parlamentar/importadores/HOWTO.md**.

Recomendamos inicialmente que você realiza a importação dos dados Convenção Nacional Francesa (uma casa legislativa fictícia).


Conferindo se está tudo certo
---------------------------------

Execute os testes:

    $ python manage.py <module_name>

Onde `<module_name>` pode ser `analises, modelagem, importadores, exportadores ou importadorInterno`.

Inicie o servidor do Django:

    $ python manage.py runserver

Considerando que você importou os dados da Convenção Nacional Francesa, acesse **http://127.0.0.1:8000/analises/analise/conv** e verifique se o gráfico aparece corretamente (um gráfico estático com três circunferâncias, dispostos aproximadamente como um triângulo equilátero).




