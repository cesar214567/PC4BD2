from rtree import index
from Algoritmos.extractFeatures import Collection
import os,sys

#Borrar indice anterior
os.popen('rm 128d_index.data 128d_index.index')

#Caracteristicas del arbol
p = index.Property()
p.dimension = 128
p.buffering_capacity = 128
p.dat_extension = 'data'
p.idx_extension = 'index'
rtree = index.Index('128d_index',properties=p,interleaved = False)

#Insertar las imagenes en R-Tree
for i in range(len(Collection["names"])):    
    tupla=[]
    for j in Collection["encodings"][i]:
        tupla.append(j)
        tupla.append(j)
    realTupla=tuple(tupla)
    dic = {}
    dic['nombre'] = Collection["names"][i]
    rtree.insert(id = i,coordinates = realTupla, obj = dic)