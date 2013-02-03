#!/bin/bash
echo "Esta operação irá apagar todas as análises salvas no bd."
echo "Os dados das votações em si continuarão intactos."
read -p "Tem certeza?[y|n] " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]
then
    sqlite3 radar_parlamentar.db 'delete from analises_analisetemporal; delete from analises_analiseperiodo; delete from analises_analiseperiodo_posicoes; delete from analises_posicaopartido;'
    echo ' '
    echo 'Todas as analises foram excluidas do banco de dados.'
fi
