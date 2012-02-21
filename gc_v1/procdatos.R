#Tablas de procesado de datos
#datos_aa : frecuencia de uso de codones terminados en G/C por aa
#datos_media : media de la frecuencia de uso de codones G/C
#datos_codones : frecuencia de uso de cada codon

#En todos los casos id es el prefijo identificador del archivo
#Obtener codones terminados en G/C (salvo met, stop, trp)
codonesgc<-function(id){
    prom_mayor<-read.table(file=paste(id,"_prom_mayor",sep=""))
    prom_menor<-read.table(file=paste(id,"_prom_menor",sep=""))
    promedio<-matrix(nrow=2, ncol=29)
    j<-0
    for (i in 0:64){
        if (i%%2==0 & i!=12 & i!=36 & i!=52){
            promedio[,j]<-cbind(prom_mayor[i,],prom_menor[i,]);
            j<-j+1
        }   
    }   
    return(promedio)
}

#Promedio de la frecuencia de uso de codones terminados en G/C agrupados por aa 
gcxaa<-function(id){
    datos<-codonesgc(id)
    aa<-matrix(nrow=2, ncol=18)
    for(i in 1:2){
        aa[i,1]<-datos[i,1]            	 	  #Phe
        aa[i,2]<-sum(datos[i,2:4])    	          #Leu
        aa[i,3]<-datos[i,5]             	  #Ile
        aa[i,4]<-sum(datos[i,6:7])         	  #Val 
        aa[i,5]<-sum(datos[i,8:9],datos[i,26])    #Ser 
        aa[i,6]<-sum(datos[i,10:11])              #Pro 
        aa[i,7]<-sum(datos[i,12:13])              #Thr 
        aa[i,8]<-sum(datos[i,14:15])           	  #Ala 
        aa[i,9]<-datos[i,16]               	  #Tyr
        aa[i,10]<-datos[i,17]             	  #His
        aa[i,11]<-datos[i,18]            	  #Gln
        aa[i,12]<-datos[i,19]             	  #Asn
        aa[i,13]<-datos[i,20]           	  #Lys
        aa[i,14]<-datos[i,21]   	          #Asp
        aa[i,15]<-datos[i,22]	                  #Glu
        aa[i,16]<-datos[i,23]              	  #Cys
        aa[i,17]<-sum(datos[i,24:25],datos[i,27]) #Arg 
        aa[i,18]<-sum(datos[i,28:29]) 		  #Gly 
    }
    return (aa)
}


#Obtener la frec de codones para cada gen
promgc<-function(inputfile,pos){
    cod<-read.csv(file=inputfile)
    codgc<-matrix(ncol=length(pos), nrow=nrow(cod))
    for(i in 1:length(pos)){
        codgc[,i]<-cod[,pos[i]]
    }
    prom<-matrix(ncol=1, nrow=nrow(cod))
    for(i in 1:nrow(cod)){
        prom[i,]<-sum(codgc[i,])/length(pos)
    }
    return(prom)
}

#Obtener la frecuencia de uso de codones 
codonestotal<-function(id){
    prom_mayor<-read.table(file=paste(id,"_prom_mayor",sep=""))
    prom_menor<-read.table(file=paste(id,"_prom_menor",sep=""))
    promedio<-matrix(nrow=2, ncol=64)
    for (i in 0:64){
        promedio[,i]<-cbind(prom_mayor[i,],prom_menor[i,]);
    }
    return(promedio)
}

#Devuelve los datos de la tabla frec. G/C por aa
datos_aa<-function(id){
    gc<-gcxaa(id)
    aa=c("Phe", "Leu", "Ile", "Val", "Ser", "Pro", "Thr", "Ala", "Tyr", "His", "Gln", "Asn", "Lys",      "Asp","Glu", "Cys", "Arg", "Gly")
    cbind(aa,mayor_exp=gc[1,],menor_exp=gc[2,])
}

#Devuelve el valor de la media de uso de codones G/C 
datos_media<-function(id){
    cod<-codonesgc(id)
    print(cbind(mayor_exp=mean(cod[1,]),menor_exp=mean(cod[2,])))
    aa<-datos_aa(id)
    print(cbind(aa_mayor_exp=mean(as.numeric(aa[,2])),aa_menor_exp=mean(as.numeric(aa[,3]))))

}

#Devuelve la tabla de frecuencia de uso de cada codon
datos_codones<-function(id){
    codon<-c("UUU","UUC","UUA","UUG","CUU","CUC","CUA","CUG","AUU","AUC","AUA","AUG","GUU","GUC","GUA",  "GUG","UCU","UCC","UCA","UCG","CCU","CCC","CCA","CCG","ACU","ACC","ACA","ACG","GCU","GCC","GCA","GCG",   "UAU","UAC","UAA","UAG","CAU","CAC","CAA","CAG","AAU","AAC","AAA","AAG","GAU","GAC","GAA","GAG","UGU",   "UGC","UGA","UGG","CGU","CGC","CGA","CGG","AGU","AGC","AGA","AGG","GGU","GGC","GGA","GGG")
    aa<-c("Phe","Phe","Leu","Leu","Leu","Leu","Leu","Leu","Ile","Ile","Ile","Met","Val","Val","Val",     "Val","Ser","Ser","Ser","Ser","Pro","Pro","Pro","Pro","Thr","Thr","Thr","Thr","Ala","Ala","Ala","Ala",   "Tyr","Tyr","Stop","Stop","His","His","Gln","Gln","Asn","Asn","Lys","Lys","Asp","Asp","Glu","Glu","Cys", "Cys","Stop","Trp","Arg","Arg","Arg","Arg","Ser","Ser","Arg","Arg","Gly","Gly","Gly","Gly")
    frec_cod<-codonestotal(id)
    cbind(as.data.frame(codon),as.data.frame(aa),mayor_exp=frec_cod[1,],menor_exp=frec_cod[2,])
}

