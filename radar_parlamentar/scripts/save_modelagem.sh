#!/bin/bash
# Faz dump das tabelas cujo nome começa com 'modelagem_' para o arquivo modelagem_.back. 
sqlite3 ../radar_parlamentar.db '.dump modelagem_%' > modelagem_.back
