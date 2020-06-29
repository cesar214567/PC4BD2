from scipy.spatial.distance import cdist
from Algoritmos.extractFeatures import Collection, initCollection, getFeatures
import heapq, math, os
from scipy.spatial import distance

#KNN busqueda secuencial euclídeana o manhattan
def KNNsearch(query, k, metric):
    result = []
    for i in range(len(Collection["names"])):
        dist = math.inf
        ndist=0
        if(metric=="eucledian"):
            ndist = distance.euclidean(query, Collection["encodings"][i])
        elif(metric=="manhattan"):
            ndist = distance.cityblock(query, Collection["encodings"][i])
        dist = min(dist,ndist)
        if(len(result)<k):
            heapq.heappush(result,(-dist,Collection["names"][i]))
        elif(heapq.nsmallest(1,result)[0][0]<-dist):
            heapq.heapreplace(result,(-dist,Collection["names"][i]))
    return [heapq.heappop(result) for i in range(len(result))]