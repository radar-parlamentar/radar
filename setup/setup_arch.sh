#!/bin/bash
#Instalação das dependências no Arch Linux

su
pacman -S python2 python2-numpy python2-matplotlib python2-pip sqlite3 mysql-python
pip2 install svgwrite
wget "http://www.djangoproject.com/download/1.4/tarball/" -O Django-1.4.tar.gz
tar xzvf Django-1.4.tar.gz
cd Django-1.4
python2 setup.py install 
