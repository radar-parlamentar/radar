#!/bin/bash
# Aplica as linhas SQL do arquivo modelagem_.back, restaurando as tabelas cujo nome começa com 'modelagem_'.
sqlite3 ../radar_parlamentar.db '.read modelagem_.back'
