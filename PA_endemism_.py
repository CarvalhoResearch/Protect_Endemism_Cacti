#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 14:21:11 2020

@author: eduardo
"""
#==============================================================================
'''                     Usual Python Libraries                           '''

#import shapefile as shp
#from glob import glob
import pandas as pd
#import rasterio
import matplotlib.pyplot as plt
#import matplotlib as mpl
#import numpy as np
#import time
#from matplotlib.colors import ListedColormap, BoundaryNorm
#from matplotlib.patches import Patch
import geopandas as gpd
#import rasterstats as rs
import seaborn as sns 
#import gdal
from rasterstats import zonal_stats

sns.set(font_scale=2)
#==============================================================================

uc = gpd.read_file("/home/eduardo/Documents/projetos/endemic_vs_desmat/data/protected/caatinga_areas_protegidas.shp")

fig, ax = plt.subplots(figsize=(15, 10))

ax.grid(which='major', axis='y', linestyle='-', color='#fc8560', linewidth=5)
ax.annotate('Very High',xy=(0,0.95),weight='bold')
ax.annotate('High',xy=(0,0.75),weight='bold')
ax.annotate('Medium',xy=(0,0.55),weight='bold')
ax.annotate('Low',xy=(0,0.35),weight='bold')
ax.annotate('Very Low',xy=(0,0.15),weight='bold')

uc["cwei_max"].plot.area(ax=ax,color='#fc8560',lw=5)
ax.set_xlabel("Protected Area")
ax.set_ylabel("Maximum Corrected Weighted Endemism Index")

# ordena as ucs por cwei e plota
#----------------------------------------------

uc_cortado=gpd.read_file("/home/eduardo/Documents/projetos/endemic_vs_desmat/data/protected/caatinga_areas_protegidas.shp")
# uc_cortado.plot()
gpd.GeoDataFrame(geometry=list(uc_cortado.unary_union)).to_file("/home/eduardo/t1.shp")

total=zonal_stats("/home/eduardo/t1.shp", "/home/eduardo/Documents/projetos/endemic_vs_desmat/data/category.endemism.tif",categorical=True,stats="count")
total=pd.DataFrame(total) 
total.columns=['very low','count','low','medium','high','very high','nada']
total = total.drop(['count','nada'],axis=1)
total.index = total.index+1

total_protec=total.sum()
#----------------------------------------------

uc = gpd.read_file("/home/eduardo/Documents/projetos/endemic_vs_desmat/data/protected/caatinga_areas_protegidas.shp")
protegido=zonal_stats("/home/eduardo/Documents/projetos/endemic_vs_desmat/data/protected/caatinga_areas_protegidas.shp", "/home/eduardo/Documents/projetos/endemic_vs_desmat/data/category.endemism.tif",categorical=True,stats="count")
protegido=pd.DataFrame(protegido) 
protegido['categoria']= uc.GRUPO4
protegido['grupo']= uc.CATEGORI3

siglas=['RPPN','FLONA','ESEC','PARNA','ARIE','REBIO','APA','RESEX','REVIS','RDS','MONA']

protegido['siglas'] = [siglas[protegido.grupo.unique().tolist().index(i)] for i in protegido['grupo']]
protegido.columns=['Very low','count','na','Low','Medium','High','Very high','categoria','grupo','siglas']
protegido = protegido.drop(['count','na'],axis=1)

color_map = plt.cm.get_cmap('magma')

p=protegido.groupby(['categoria']).sum()
p.index=['Full Protection','Sustainable Use']
ax=p.plot.bar(figsize=(15,10),rot=0,logy=True,ylim=10,cmap=color_map.reversed(),edgecolor='black',width=.7)
ax.set_xlabel("")
ax.set_ylabel("Log(Area km²)")

uc['NOME_UC1'] = [i.title() for i in uc['NOME_UC1']]

data = uc.drop(['ESFERA5','NOME_ORG12','CATEGORI3','geometry',"cwei_max"],axis=1)
data['tipo'] = protegido['siglas'] 

p2=protegido.groupby(['siglas']).sum()
ax2=p2.plot.bar(figsize=(15,12),rot=0,logy=True,cmap=color_map.reversed(),edgecolor='black',width=.7)
ax2.set_ylabel("Log(Area km²)")
ax2.set_xlabel("")
 

desprotegido=zonal_stats("/home/eduardo/Documents/projetos/endemic_vs_desmat/data/caatinga/caatinga_sem_ucs.shp", "/home/eduardo/Documents/projetos/endemic_vs_desmat/data/category.endemism.tif",categorical=True,stats="count")
desprotegido=pd.DataFrame(desprotegido) 
desprotegido.columns=['count','na','Very low','Low','Medium','High','Very high']
desprotegido = desprotegido.drop(['count','na'],axis=1)
desprotegido = desprotegido.sum()
protegido    = protegido.sum()
protegido    = protegido.drop(['categoria','grupo','siglas'],axis=0)
t = pd.concat([protegido, desprotegido],axis=1)
t.columns = ['Protected','Unprotected']

ax3=t.transpose().plot.bar(figsize=(15,10),rot=0,logy=True,ylim=10,cmap=color_map.reversed(),edgecolor='black',width=.7)
ax3.set_ylabel("Log(Area km²)")
ax3.set_xlabel("")
 







