#!/bin/bash
# Invoca rotinas de análise para que os resultados fiquem guardados no cache

periodicidades=("QUADRIENIO" "BIENIO" "ANO" "SEMESTRE")
casas_legislativas=("cmsp" "cdep" "sen")
porta_development=8000

if [[ "$DJANGO_SETTINGS_MODULE" == "settings.development" ]]; then
	base_url="http://localhost:$porta_development"
else
	base_url="http://localhost"
fi

echo "Iniciando a rotina de cache das analises em '$(date)'"
inicio=$(date '+%s')

for casa in ${casas_legislativas[*]}; do
    for periodicidade in ${periodicidades[*]}; do
        url="$base_url/analises/json_analise/$casa/$periodicidade/"
        echo "curl $url"
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

echo "Finalizando a rotina de cache das analises em '$(date)'."
printf "Se passaram %dh %02dmin %02ds\n\n" $dh $dm $ds