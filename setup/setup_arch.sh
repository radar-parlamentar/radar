#!/bin/bash
#Instalação das dependências no Arch Linux

su
pacman -S python2 python2-pip sqlite3
sudo pip install -r requirements.txt
mkdir /tmp/django_cache
