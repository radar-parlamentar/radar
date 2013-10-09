#!/bin/bash
#Instalação das dependências no Ubuntu

sudo apt-get install sqlite3 python-pip 
sudo pip install -r requirements.txt
mkdir /tmp/django_cache
