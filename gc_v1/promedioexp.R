# Obtener el promedio de uso de codones para el 10% de los genes de
# mayor y de menor expresion. Se guardan en los archivos prom_mayor
# y prom_menor
# inputblast es la salida de un blast con con col. 2 de expresion
# inputcodones es el archivo de uso de codones obtenidos con cod_freq.pl
# id es el identificador o prefijo para nombre de archivos
# valor es el porcentaje de genes a estudira
#Cargar funcion codfreq
source("codfreq.R")

guardar_codones<-function (inputexpr, inputcodones, id, valor){
   	#Cargar archivo del blast en variable exp
  	exp<-read.table(file=inputexpr)
   
	#Ordenar la tabla por la columna 2 (expresion)
   	ord<-exp[order(exp[,2]),]
	
	#Guardar en ordm todos los que se expresan (col.2>0)
   	ordexp<-ord[ord[,2]>0,]

	# Guardar 10% mas y menos expresado
	mayor_exp<-ordexp[(nrow(ordexp)+1-as.integer(nrow(ordexp)/(100/as.numeric(valor)))):nrow(ordexp),]
   	menor_exp<-ordexp[(1:as.integer(nrow(ordexp)/(100/as.numeric(valor)))),]

	#Cargar el archivo de codones (obtenido con cod_freq.pl)
	codones<-read.csv(file=inputcodones, sep=",", header=FALSE)

	#Obtener num de fila de los genes mas y menos expresados
	idmayor<-as.numeric(rownames(mayor_exp))
	idmenor<-as.numeric(rownames(menor_exp))
	
	#Lista de csv de codones p/c/gen (mas y menos expresados)
	codmayor<-codones[idmayor[1],]
	for(i in 2:length(idmayor)){
		codmayor[i,]<-codones[idmayor[i],]
	}
	codmenor<-codones[idmenor[1],]
	for(i in 2:length(idmenor)){
		codmenor[i,]<-codones[idmenor[i],]
	}
	write.table(codmayor,file=paste(id,"_codmayor",sep=""),sep=",",col.names=FALSE, row.names=FALSE)
	write.table(codmenor,file=paste(id,"_codmenor",sep=""),sep=",",col.names=FALSE, row.names=FALSE)

	#Guardar posiciones de los genes
	write.table(as.numeric(row.names(codmayor)),file=paste(id,"_posmayor",sep=""),col.names=FALSE,row.names=FALSE)
	write.table(as.numeric(row.names(codmenor)),file=paste(id,"_posmenor",sep=""),col.names=FALSE,row.names=FALSE)
}

guardar_frec<-function(id){
	codmayor<-read.csv(file=paste(id,"_codmayor",sep=""),header=FALSE)
	codmenor<-read.csv(file=paste(id,"_codmenor",sep=""),header=FALSE)

	#Calcular la frecuencia de uso de codones para los genes de mayor expresion (uso codfreq.R)
	frec_codmayor<-codmayor[1,]
	frec_codmayor<-frec_codmayor-frec_codmayor
	for(i in 1:nrow(codmayor)){
		frec_codmayor[i,]<-codfreq(codmayor[i,])
	}
	write.table(frec_codmayor,file=paste(id,"_frec_codmayor",sep=""),col.names=FALSE,row.names=FALSE, sep=",")

	frec_codmenor<-codmenor[1,]
	frec_codmenor<-frec_codmenor-frec_codmenor
	for(i in 1:nrow(codmenor)){
		frec_codmenor[i,]<-codfreq(codmenor[i,])
	}
	write.table(frec_codmenor,file=paste(id,"_frec_codmenor",sep=""),col.names=FALSE,row.names=FALSE, sep=",")
}

#Promedio de uso de codones para genes de mayor y menor expresion
guardar_prom<-function(id){
	frec<-read.csv(file=paste(id,"_frec_codmayor",sep=""), sep=",", header=FALSE)
	prom<-promedio(frec)
	write.table(prom,file=paste(id,"_prom_mayor",sep=""),col.names=FALSE,row.names=FALSE,sep=",")

	frec<-read.csv(file=paste(id,"_frec_codmenor",sep=""), sep=",", header=FALSE)
	prom<-promedio(frec)
	write.table(prom,file=paste(id,"_prom_menor",sep=""),col.names=FALSE,row.names=FALSE,sep=",")
}

promedio<-function(frec){
	#Sumatoria de la frecuencia de codones p/c/gen
	prom<-1:64
	prom<-prom-prom
	#Cuenta el uso de codones sinonimos en cada gen
	cont<-contador(frec)
	#Promedio para uso para cada codon
	for(i in 1:64){
		if(i==1|i==2){prom[i]<-sum(frec[i]/cont[1])}
		if(i>=3 & i<=8){prom[i]<-sum(frec[i]/cont[2])}
		if(i>=9 & i<=11){prom[i]<-sum(frec[i]/cont[3])}
		if(i==12){prom[i]<-sum(frec[i]/cont[4])}
		if(i>=13 & i<=16){prom[i]<-sum(frec[i]/cont[5])}
		if(i>=17 & i<=20 | i==57 | i==58){prom[i]<-sum(frec[i]/cont[6])}
		if(i>=21 & i<=24){prom[i]<-sum(frec[i]/cont[7])}
		if(i>=25 & i<=28){prom[i]<-sum(frec[i]/cont[8])}
		if(i>=29 & i<=32){prom[i]<-sum(frec[i]/cont[9])}
		if(i==33 | i==34){prom[i]<-sum(frec[i]/cont[10])}
		if(i==35 | i==36 | i==51){prom[i]<-sum(frec[i]/cont[11])}
		if(i==37 | i==38){prom[i]<-sum(frec[i]/cont[12])}
		if(i==39 | i==40){prom[i]<-sum(frec[i]/cont[13])}
		if(i==41 | i==42){prom[i]<-sum(frec[i]/cont[14])}
		if(i==43 | i==44){prom[i]<-sum(frec[i]/cont[15])}
		if(i==45 | i==46){prom[i]<-sum(frec[i]/cont[16])}
		if(i==47 | i==48){prom[i]<-sum(frec[i]/cont[17])}
		if(i==49 | i==50){prom[i]<-sum(frec[i]/cont[18])}
		if(i==52){prom[i]<-sum(frec[i]/cont[19])}
		if(i>=53 & i<=56 | i>=59 & i<=60){prom[i]<-sum(frec[i]/cont[20])}
		if(i>=61 & i<=64){prom[i]<-sum(frec[i]/cont[21])}
	}
	return(prom)
}

#Contador de existencia codones sinonimos en gen
contador<-function(frec){
	aa<-1:21
	aa<-aa-aa
	for(i in 1:nrow(frec)){
		if(sum(frec[i,1:2])>0){aa[1]=aa[1]+1}
		if(sum(frec[i,3:8])>0){aa[2]=aa[2]+1}
		if(sum(frec[i,9:11])>0){aa[3]=aa[3]+1}
		if(frec[i,12]>0){aa[4]=aa[4]+1}
		if(sum(frec[i,13:16])>0){aa[5]=aa[5]+1}
		if(sum(frec[i,17:20])+sum(frec[i,57:58])>0){aa[6]=aa[6]+1}
		if(sum(frec[i,21:24])>0){aa[7]=aa[7]+1}
		if(sum(frec[i,25:28])>0){aa[8]=aa[8]+1}
		if(sum(frec[i,29:32])>0){aa[9]=aa[9]+1}
		if(sum(frec[i,33:34])>0){aa[10]=aa[10]+1}
		if(sum(frec[i,35:36])+frec[i,51]>0){aa[11]=aa[11]+1}
		if(sum(frec[i,37:38])>0){aa[12]=aa[12]+1}
		if(sum(frec[i,39:40])>0){aa[13]=aa[13]+1}
		if(sum(frec[i,41:42])>0){aa[14]=aa[14]+1}
		if(sum(frec[i,43:44])>0){aa[15]=aa[15]+1}
		if(sum(frec[i,45:46])>0){aa[16]=aa[16]+1}
		if(sum(frec[i,47:48])>0){aa[17]=aa[17]+1}
		if(sum(frec[i,49:50])>0){aa[18]=aa[18]+1}
		if(frec[i,52]>0){aa[19]=aa[19]+1}
		if(sum(frec[53:56])+sum(frec[i,59:60])>0){aa[20]=aa[20]+1}
		if(sum(frec[i,61:64])>0){aa[21]=aa[21]+1}
	}
	return(aa)
} 

#Calcular contenido G,C y G+C y devolverlo para guardarlo
calcular_gc<-function(codones){
	posgc<-1:32; j<-1
	for(i in 1:64){if(i%%2==0){posgc[j]<-i; j<-j+1}}
	posg<-c(4,8,12,16,20,24,28,32,36,40,44,48,52,56,60,64)
	posc<-c(2,6,10,14,18,22,26,30,34,38,42,46,50,54,58,62)

	gcdatos<-matrix(nrow=nrow(codones), ncol=3,data=0)

	for (i in 1:nrow(codones)){
		for (j in 1:length(posgc)){
			gcdatos[i,1]<-gcdatos[i,1]+codones[i,posgc[j]]
		}
	}
	for(i in 1:nrow(codones)){
		for(j in 1:length(posg)){
			gcdatos[i,2]<-gcdatos[i,2]+codones[i,posg[j]]
		}
	}
	for(i in 1:nrow(codones)){
		for (j in 1:length(posc)){
			gcdatos[i,3]<-gcdatos[i,3]+codones[i,posc[j]]
		}
	}
	for(i in 1:nrow(codones)){
		gcdatos[i,]<-gcdatos[i,]/sum(codones[i,])
	}
	return(gcdatos)
}	

#Guardar el promedio de contenido en G, C y G+C de cada gen
guardar_gc<-function(id){ 
	codmayor<-read.csv(file=paste(id,"_codmayor",sep=""),header=FALSE)
	codmenor<-read.csv(file=paste(id,"_codmenor",sep=""),header=FALSE)

	gcmenor<-calcular_gc(codmenor)
	gcmayor<-calcular_gc(codmayor)

	write.table(gcmenor,file=paste(id,"_gc_menor",sep=""),col.names=FALSE,row.names=FALSE,sep=",")
	write.table(gcmayor,file=paste(id,"_gc_mayor",sep=""),col.names=FALSE,row.names=FALSE,sep=",")
}

guardar_todo<-function(inputexpr,inputcodones,id,valor){
	guardar_codones(inputexpr,inputcodones,id,valor)
	guardar_frec(id)
	guardar_prom(id)
	guardar_gc(id)
}
