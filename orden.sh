#Ordenado de genes que agrega no expresados con -1
lista_genes=$(awk '{print $1}' nombres_cruzi )
for gen in $lista_genes; do
	expresado=$(grep -w "$gen" expresion_cruzi | awk '{print $1}')
	if [ -z "$expresado" ] 
	then
		expresado=-1
	fi
	echo -e "$gen \t $expresado"  
done
