# Graficas 
#graf_gc : promedio de uso de codones terminados en G/C por codon
#graf_gcxaa : frecuencia de uso de codones terminados en G/C por aa
#his_gyc: promedio de uso de codones terminados en G, C y G/C para cada gen

#Cargar archivo con funciones de procesado de datos para graficar
source ("procdatos.R")
#Grafica para los codones pares (menos met, stop y trp) la frecuencia de uso
#de los codones terminados en G/C
graf_gc<-function(id){
	datos<-codonesgc(id)
	barplot(datos, beside=T, names.arg=c(2,4,6,8,10,14,16,18,20,22,24,26,28,30,32,34,38,40,42,44,46,48,50,54,56,58,60,62,64), main=paste("Frecuencia de uso de codones terminados en G/C en",id), col=c("darkblue","darkgrey"), border=NA, ylab="Frecuencia",ylim=c(0,0.8))
	legend("topright",c("Mayor exp", "Menor exp"),fill=c("darkblue","darkgrey"),bty="n")
}

#Grafica del promedio de la frecuencia de uso de codones terminados en G/C agrupados por aa 
graf_gcxaa<-function(id){
	barplot(gcxaa(id), beside=T, ylim=c(0,0.8), names.arg=c("Phe", "Leu", "Ile", "Val", "Ser", "Pro", "Thr", "Ala", "Tyr", "His", "Gln", "Asn", "Lys", "Asp","Glu", "Cys", "Arg", "Gly"), main=paste("Frecuencia de uso de codones terminados en G/C por aa en",sub(x=id,pattern=".*/", replacement="")), col=c("darkgrey",rgb(0,0,1,0.8)), border=NA, ylab="Frecuencia")
	legend("topright",c("Mayor exp", "Menor exp"),fill=c("darkgrey",rgb(0,0,1,0.8)),bty="n")

}

#Calculo de los histogramas y lineas de densidad 
calc_his<-function(gcmayor, gcmenor, titulo){
	# Calcula histogramas 
	b<-100
	if (titulo=='cruzi'){b<-200}
	hcmayor <- hist(gcmayor,breaks=b,plot = FALSE)
	hcmenor <- hist(gcmenor,breaks=b,plot = FALSE)
	# Rango del eje y
	#Dibuja 1era grafica
	plot(hcmenor, xaxt='n',yaxt='n',
	xlim=c(0.1,1),#c(min(gcmenor,gcmayor),max(gcmenor,gcmayor)),
	ylim=c(0,max(hcmayor$count,hcmenor$count)),#xaxt='n', yaxt='n',# ylim = ylim,
	col = rgb(0,0,1,0.3),
xlab ='Contenido de G+C', 
#xlab='',
ylab='Genes',	main = paste('Contenido de G+C en',sub(x=titulo,pattern=".*/", replacement="")
),freq = TRUE)
	#Mejoro eje x
	axis(1,at=seq(0,1,by=0.05),lwd=1,lwd.ticks=1)
	axis(2,at=seq(0,max(hcmayor$count,hcmenor$count),10),seq(0,max(hcmayor$count,hcmenor$count),10))
	#Dibuja 2da grafica encima
	plot(hcmayor,
	xaxt = 'n', yaxt = 'n', #sin ejes
	col = rgb(0,1,0,0.2), add = TRUE, freq = TRUE) 
	legend('topleft',c('Mayor exp.','Menor exp.'),fill = rgb(0,1:0,0:1,0.4), bty = 'n',)	
}


#Grafica de la frecuencia de uso de codones terminados en G, C y G/C para cada gen
hist_gyc<-function(id){
	gcmayor<-read.csv(file=paste(id,"_gc_mayor",sep=""), sep=",", header=FALSE)
	gcmenor<-read.csv(file=paste(id,"_gc_menor",sep=""), sep=",", header=FALSE)

	calc_his(gcmayor[,1],gcmenor[,1],paste('GC en',id))
}
histodos<-function(){
        gcmayor<-read.csv(file="mayor2", sep=",", header=FALSE)
        gcmenor<-read.csv(file="menor2", sep=",", header=FALSE)

        calc_his(gcmayor[,1],gcmenor[,1],paste('vivax'))
}
