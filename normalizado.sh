#!/bin/sh

#Script de normalizado de la expresion por la longitud.
#El archivo_blast con salida m8 y archivo_long tipo: nombre_gen longitud

if [ $# -lt 3 ]; then
    echo -e "\nSe necesitan los parametros: archivo_blast (salida m8), archivo_long (tipo: nombre_gen longitud), archivo_salida\n"
    exit 1
fi

BLAST_FILE=$1
LONG_FILE=$2
OUT_FILE=$3

HITSxGEN=$(awk '{print $2}' $BLAST_FILE | sort | uniq -c) # $2 blast, $3 bowtie
GENES=$(cat "$LONG_FILE"|awk '{print $1}')

for gen in $GENES; do
    expresa=$(echo "$HITSxGEN" | grep -w "$gen" | awk '{print $1}')
    if [ "$expresa" ]; then    
        long=$(grep -w "$gen" $LONG_FILE | awk '{print $2}')
        normalizado=$(echo "scale=4; $expresa/$long" | bc -l)
        echo -e "$gen \t $normalizado" >> $OUT_FILE 
    else
	echo -e "$gen \t -1" >> $OUT_FILE
    fi
done
