#!/bin/bash
#Instalação das dependências no Ubuntu

sudo apt-get install python-numpy python-matplotlib python-pip sqlite3 python-mysqldb
sudo pip install svgwrite
wget "http://www.djangoproject.com/download/1.4/tarball/" -O Django-1.4.tar.gz
tar xzvf Django-1.4.tar.gz
cd Django-1.4
sudo python setup.py install 
