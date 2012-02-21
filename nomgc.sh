#!/bin/sh
#Script que dada la posicion de un gen en una tabla ordenada, devuelve su nombre, nivel de expresion y contenido gc

#POS_FILE es el archivo id_posmayor/menor que devuelve guardar_codones() en promedioexp.R 
POS_FILE=$1 
#NOM_FILE es un archivo de nombres de genes ordenado
NOM_FILE=$2
#GC_FILE es id_gc_mayor/menor que devuelve guardar_gc() en promedioexpr.R
GC_FILE=$3
#EXP_FILE es el archivo_expresion 
EXP_FILE=$4

if [ $# -lt 4 ]; then
    echo -e "\nSe necesitan los parametros: 
        archivo_posicion
        archivo_nombres
        archivo_gc
        archivo_expresion\n"
    exit 1
fi


POS_GEN=$(cat $POS_FILE)
NOM_PROD=$(cat $NOM_FILE| sed 's/is_pseudo=true |//'|awk -F\| '{print $2"|"$3"|"$4 }' | sed 's/product=//'>temp_nom)

for pos in $POS_GEN; do
	gen=$(sed -n "$pos"p temp_nom)
	exp=$(sed -n "$pos"p $EXP_FILE| awk '{print $2}')
	echo -e "$exp $gen">>temp_file
done

gc_gen=$(paste $3 temp_file)
rm temp_file
rm temp_nom
echo "$gc_gen"| while read LINE; do
	echo $LINE| awk -F\, '{$1=$1" "}{$2=$2" "}1'
done
