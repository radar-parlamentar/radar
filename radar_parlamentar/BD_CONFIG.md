Projeto Django
====================

Para configurar o MySql como banco de dados:
-Instalação:
    $ sudo apt-get install mysql-server
    $ sudo apt-get install python-mysqldb

Deve-se criar um usuário "root" e o banco dentro do próprio MySQL. 
	$ mysql -u root -p 
	Enter password: root
	#Entra no shell do mysql
	
	mysql>CREATE DATABASE radar;
	mysql>quit

Edite o arquivo settings/development.py* e insira a senha do seu usuário do mysql (pode ser o root).
* confira settings/README.md
	
Para criar as tabelas do Radar Parlamentar:

    $ python manage.py syncdb #Cria todas as tabelas
	
Agora, pode-se importar todos os dados com os Importadores!!
