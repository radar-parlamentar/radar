#!/bin/bash
# invoca rotinas de análise para que os resultados fiquem guardados no cache

nome_script=`basename "$0"`

echo "Iniciando a execucao do '$nome_script' em '$(date)'"
inicio=$(date '+%s')

periodicidades=("QUADRIENIO" "BIENIO" "ANO" "SEMESTRE")
casas_legislativas=("cmsp" "cdep" "sen")

for casa in ${casas_legislativas[*]}; do
    for periodicidade in ${periodicidades[*]}; do
        url="http://localhost/analises/json_analise/$casa/$periodicidade/"
        echo "Executando o curl para $url"
        curl --fail --silent --show-error $url > /dev/null
        
        rc=$?
        if [[ $rc != 0 ]]; then
            echo "Erro executando o curl para $url"
        fi
    done
done

fim=$(date '+%s')
dt=$((fim - inicio))
ds=$((dt % 60))
dm=$(((dt / 60) % 60))
dh=$((dt / 3600))

echo "Terminando a execucao do '$nome_script' em '$(date)'."
printf "Se passaram %dh %02dmin %02ds\n\n" $dh $dm $ds