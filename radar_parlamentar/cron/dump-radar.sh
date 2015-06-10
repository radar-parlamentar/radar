#!/bin/bash
# Argumento: arquivo de saída (onde o dump será salvo)
echo -e "Gerando dump completo do banco"
pg_dump -h localhost -U radar radar --inserts -t modelagem_* -f $1
