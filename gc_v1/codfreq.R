#Devuelve la frecuencia de uso de un codon como una tabla en orden estandar
#La frecuencia es el conteo(codon)/conteo(grupo de codones)
#Se eliminan los codones stop, met y trp
#mat debe ser de tipo lista (ej x[3,])
codfreq<-function(mat) {
    x<-mat[1,]
    x<-x-x
    if (sum(mat[1:2])>0) {x[1:2]<-mat[1:2]/sum(mat[1:2])}
    if (sum(mat[3:8])>0) {x[3:8]<-mat[3:8]/sum(mat[3:8])}
    if (sum(mat[9:11])>0) {x[9:11]<-mat[9:11]/sum(mat[9:11])}
    if ((mat[12])>0) {x[12]<-1}
    if (sum(mat[13:16])>0) {x[13:16]<-mat[13:16]/sum(mat[13:16])}
    if (sum(mat[17:20])+sum(mat[57:58])>0) {x[17:20]<-mat[17:20]/(sum(mat[17:20])+sum(mat[57:58]))}
    if (sum(mat[21:24])>0) {x[21:24]<-mat[21:24]/sum(mat[21:24])}
    if (sum(mat[25:28])>0) {x[25:28]<-mat[25:28]/sum(mat[25:28])}
    if (sum(mat[29:32])>0) {x[29:32]<-mat[29:32]/sum(mat[29:32])}
    if (sum(mat[33:34])>0) {x[33:34]<-mat[33:34]/sum(mat[33:34])}
    stop<-(mat[35]+mat[36]+mat[51])
    if (stop>0) { x[35]<-mat[35]/stop; x[36]<-mat[36]/stop}
    if (sum(mat[37:38])>0) {x[37:38]<-mat[37:38]/sum(mat[37:38])}
    if (sum(mat[39:40])>0) {x[39:40]<-mat[39:40]/sum(mat[39:40])}
    if (sum(mat[41:42])>0) {x[41:42]<-mat[41:42]/sum(mat[41:42])}
    if (sum(mat[43:44])>0) {x[43:44]<-mat[43:44]/sum(mat[43:44])}
    if (sum(mat[45:46])>0) {x[45:46]<-mat[45:46]/sum(mat[45:46])}
    if (sum(mat[47:48])>0) {x[47:48]<-mat[47:48]/sum(mat[47:48])}
    if (sum(mat[49:50])>0) {x[49:50]<-mat[49:50]/sum(mat[49:50])}
    if (stop>0)  {x[51]<-mat[51]/stop}
    if (mat[52]>0) {x[52]<-1}
    if (sum(mat[53:56])+sum(mat[59:60])>0) {x[53:56]<-mat[53:56]/(sum(mat[53:56])+sum(mat[59:60]))}
    if (sum(mat[17:20])+sum(mat[57:58])>0) {x[57:58]<-mat[57:58]/(sum(mat[17:20])+sum(mat[57:58]))}
    if (sum(mat[53:56])+sum(mat[59:60])>0) {x[59:60]<-mat[59:60]/(sum(mat[53:56])+sum(mat[59:60]))}
    if (sum(mat[61:64])>0) {x[61:64]<-mat[61:64]/sum(mat[61:64])}
    return(x)
}
