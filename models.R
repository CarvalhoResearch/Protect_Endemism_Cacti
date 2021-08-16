library(dismo)
library(raster)
library(maptools)
library(sf)
library(corrplot)
library(ggfortify)
library(SSDM)
library(argparse)

commands <- commandArgs(trailingOnly = TRUE)


occs<-commands[1]
num<-commands[2]


env<-load_var(path = "/home/eduardo/projetos/endemic_vs_desmat/data/env/selected/", files = NULL, format = ".tif",categorical = NULL, Norm = TRUE, tmp = TRUE, verbose = FALSE,GUI = FALSE)
occ <- load_occ(path= '/home/eduardo/projetos/endemic_vs_desmat/data',file=occs, env,verbose=FALSE, Xcol = 'longitude', Ycol = 'latitude', sep = ',')
modelo <-stack_modelling(algorithms = c('MAXENT'), Occurrences = occ,Env = env,Xcol='longitude',Ycol ="latitude",Spcol='scientificName',method = 'pSSDM',verbose = TRUE,rep = 1, ensemble.thresh = 0.7)


evaluate<-modelo@evaluation
import<-modelo@variable.importance

ev <- paste("/home/eduardo/projetos/endemic_vs_desmat/data/evaluate",num,".csv",sep='')
write.csv(evaluate, ev)

im <- paste("/home/eduardo/projetos/endemic_vs_desmat/data/var-import",num,".csv",sep='')
write.csv(import, im)

endemismo<-paste("/home/eduardo/projetos/endemic_vs_desmat/data/endemismo.caatinga",num,'.tif',sep="")
diversidade<-paste("/home/eduardo/projetos/endemic_vs_desmat/data/diversidade.caatinga",num,'.tif',sep="")

writeRaster(modelo@endemism.map,endemismo)
writeRaster(modelo@diversity.map,diversidade)





 
