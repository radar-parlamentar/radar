# Configuração do ambiente do desenvolvedor

## 1. Clonando o repositório

A primeira coisa que deve ser feita é o clone do projeto no *Github*. Para isso basta fazer:

        $ git clone https://github.com/radar-parlamentar/radar.git

## 2. Configuração do ambiente

O Radar Parlamentar funciona, tanto em produção quanto em desenvolvimento,
utilizando containers docker.
Para tanto, você precisa ter instalado em seu sistema operacional tanto o
*Docker* quanto o *docker-compose*.
Nossa instalação foi testada utilizando:

    * Docker 18.02.0-ce (Community Edition) build __fc4de44__
    * docker-compose 1.17.1

## 3. Rodar o projeto

Para rodar o projeto, agora precisamos de mais dois containers. O container
(**django**) que tem o projeto do radar em si e o servidor de aplicação (**uwsgi**) e o
container que possui o webserver (**nginx**).

Primeiro iniciaremos o servidor de aplicação.

    docker-compose up django

Pronto, o projeto já deve estar acessível via "http://localhost". =)

Caso queira que o console não fique preso o docker, utilize a flag `-d`.

Na primeira vez em que o projeto for criado, será necessário criar o usuário
administrativo do Django (que é persistido no banco). Para tanto utilize o
comando:

     docker-compose exec django python manage.py createsuperuser

### 3.1. Comandos úteis

Para limpar tudo, rode o comando:

    docker-compose down -v; -docker-compose rm -fsv; docker volume prune -f

Para interagir diretamente com o shell do django em execução:

    docker-compose exec django python manage.py shell

Para ver o log do Django:

     docker-compose exec django tail -n 100 -f /var/log/radar/radar.log

Para ver o log do Celery:

    docker-compose logs --tail=100 -t -f celery

### 3.2. Rodar o projeto em produção

Para rodar o radar em produção você precisa definir duas variáveis de ambiente:

    - `RADAR_IS_PRODUCTION`: Define que o projeto está sendo executado em
        ambiente de produção. Isso habilita o Cache do Django e coloca o DEBUG
        como 'FALSE'
    - `RADAR_DB_PASSWORD`: Define a senha do banco de dados do radar em
        produção

    RADAR_IS_PRODUCTION=True RADAR_DB_PASSWORD=senha docker-compose up -d django

## 4. Importação dos dados

Para importar os dados basta acessar a URL:

    http://localhost/importar/<nome-curto-da-casa-legislativa>/

Obs: Você precisará colocar login/senha para ter acesso a esta página. Este
login e senha são os criados com o comando `createsuperuser` (Seção 3).

Possíveis valores para `<nome-curto-da-casa-legislativa>`:

* Convenção Francesa: "conv"
* Camara Municipal de São Paulo: "cmsp"
* Senado: "sen"
* Câmara dos Deputados: "cdep"

Exemplo: para importar dados da Câmara Municipal de São Paulo basta acessar:

    http://127.0.0.1:8000/importar/cmsp

Recomendamos inicialmente que você realize a importação dos dados Convenção
Nacional Francesa (uma casa legislativa fictícia).

Obs: todas as importações são relativamente rápidas, exceto a da Câmara dos
Deputados, que pode levar horas.

- Criando novos importadores:

http://radarparlamentar.polignu.org/importadores/

## 6. Executando os testes

Rode o comando:

    docker-compose up test
