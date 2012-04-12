#!/bin/bash
# Envelope do script listarid.py, salva os resultados no arquivo
# 'resultados/ids_que_existem.txt'.
# Os argumentos numéricos são o id mínimo e máximo a requisitar.

timer=$(date -d now +%s)
echo ""
./ids_que_existem.py 513100 513200 > resultados/ids_que_existem.txt
echo ""
printf "Terminado. %7d segundos." $(( $(date -d now +%s) - $timer ))
echo ""
echo "Resultado salvo em resultados/ids_que_existem.txt "
echo ""