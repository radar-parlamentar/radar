#!/bin/bash
# Argumento: arquivo de saída (onde o dump será salvo)
echo "Gerando dump completo do banco em '$(date)'"
pg_dump -h localhost -U radar radar --inserts -t modelagem_* -f $1
bzip2 -9 -f $1
