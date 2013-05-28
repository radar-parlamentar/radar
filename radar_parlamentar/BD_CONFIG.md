Projeto Django
====================

Para configurar o MySql como banco de dados de acordo com o já configurado settings.py:
-Instalação:
    $ sudo apt-get install mysql-server
    $ sudo apt-get install python-mysqldb

Deve-se criar um usuário "root" e o banco dentro do próprio MySQL. 
	$ mysql -u root -p 
	Enter password: root
	#Entra no shell do mysql
	
	mysql>CREATE DATABASE radar;
	mysql>quit
	
Como o Django já está configurado para funcionar com o MySQL:

    $ python manage.py syncdb #Cria todas as tabelas
	
Agora, pode-se importar todos os dados com os Importadores!!
