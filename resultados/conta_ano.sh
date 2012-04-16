#!/bin/bash

for (( i = 1955 ; i <= 2012 ; i++))
do
	`cat ids_que_existem.txt | grep /$i > ids`
    echo "Número de id's em $i: `wc -l ids`"
done
rm ids
