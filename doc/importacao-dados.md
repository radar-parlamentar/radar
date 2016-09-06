
# Importando os dados do Radar em sua máquina local para análises exploratórias

## Instalando o Postgresql

Primeiro passo é instalar o Postgresql em sua máquina. O Postgresql (ou postgres) é o banco de dados. No Ubuntu basta fazer:

    sudo apt-get update
    sudo apt-get install postgresql postgresql-contrib

Pra Windows ou outros sistemas você pode baixar daqui: http://www.postgresql.org/download/

Uma boa forma de interagir com postgres é por meio do pgadmin, que é uma ferramenta gráfica.

Pra instalar o pgadmin no Ubuntu: `sudo apt-get install pgadmin3`.

## Configurando o Postgresql

Se você estiver no Linux, o mais fácil é simplesmente executar esses comandos:

    $ sudo su - postgres
    $ createdb radar
    $ createuser radar -P
    escolha a senha
    $ psql
    # GRANT ALL PRIVILEGES ON DATABASE radar TO radar;
    saia do psql (ctrl+d)
    volte a ser o usuário normal (ctrl+d)

Mas dá pra fazer tudo isso também pelo pgadmin. O que fizemos foi criar um banco de dados chamado radar, um usuário chamado radar, e deixamos o usuário radar com todas as permissões sobre o banco radar. 

## Importando

Depois de baixar o dump, você tem que descompactar o arquivo (`bzip2 -d radar.sql.bz2`) e depois importar no postgres com o pgadmin (botão "execute arbitrary SQL queries") ou com o comando `psql -U radar -d radar < radar.sql`. A importação pode demorar!

## Explorando o banco

Aí por fim você pode explorar as tabelas com os comandos SQL usando o pgadmin (botão "execute arbitrary SQL queries") ou a linha de comando (`psql -U radar -d radar`).  Um exemplo de comando SQL é esse que lista os partidos existentes no banco: `select distinct * from modelagem_partido;`.

Para saber mais sobre SQL: http://www.w3schools.com/sql/.

