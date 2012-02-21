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
	barplot(gcxaa(id), beside=T, ylim=c(0,0.8), names.arg=c("Phe", "Leu", "Ile", "Val", "Ser", "Pro", "Thr", "Ala", "Tyr", "His", "Gln", "Asn", "Lys", "Asp","Glu", "Cys", "Arg", "Gly"), main=paste("Frecuencia de uso de codones terminados en G/C por aa en",id), col=c("darkblue","darkgrey"), border=NA, ylab="Frecuencia")
	legend("topright",c("Mayor exp", "Menor exp"),fill=c("darkblue","darkgrey"),bty="n")

}

#Calculo de los histogramas y lineas de densidad 
calc_his<-function(gcmayor, gcmenor, titulo){
	# Calcula histogramas 
	hcmayor <- hist(gcmayor,breaks=100,plot = FALSE)
	hcmenor <- hist(gcmenor,breaks=100,plot = FALSE)
	# Rango del eje y
	ylim <- range(0,hcmenor$intensities,max(hcmayor$intensities))
	#Dibuja 1era grafica
	plot(hcmayor,xaxt='n', ylim = ylim,
	col = rgb(0,1,0,0.4),xlab = 'Frecuencia', ylab='Genes',	freq = FALSE,main = paste('Contenido de',titulo))
	#Mejoro eje x
	axis(1,at=seq(0,1,.05),seq(0,1,.05))
	#Dibuja 2da grafica encima
	plot(hcmenor,
	xaxt = 'n', yaxt = 'n', #sin ejes
	col = rgb(0,0,1,0.4), add = TRUE, freq = FALSE) 
	legend('topleft',c('Mayor exp.','Menor exp.'),fill = rgb(0,1:0,0:1,0.4), bty = 'n',)	
	#Agrega lineas de densidad
	dmayor<-density(gcmayor)
	lines(dmayor, col="darkgreen",lwd=2)
	dmenor<-density(gcmenor)
	lines(dmenor, col="darkblue",lwd=2)
}

#Grafica de la frecuencia de uso de codones terminados en G, C y G/C para cada gen
hist_gyc<-function(id){
	gcmayor<-read.csv(file=paste(id,"_gc_mayor",sep=""), sep=",", header=FALSE)
	gcmenor<-read.csv(file=paste(id,"_gc_menor",sep=""), sep=",", header=FALSE)

	layout(matrix(c(1,4,2,3), 2, 2, byrow = TRUE))

	calc_his(gcmayor[,1],gcmenor[,1],paste('GC en',id))
	calc_his(gcmayor[,2],gcmenor[,2],paste('G en',id))
	calc_his(gcmayor[,3],gcmenor[,3],paste('C en',id))
}
