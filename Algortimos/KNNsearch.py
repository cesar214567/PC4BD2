from scipy.spatial.distance import cdist
from extractFeatures import Collection, initCollection, getFeatures
import heapq, math, os
from scipy.spatial import distance

def KNNsearch(query, k, metric):
    result = []
    unique_names = list(set(Collection["names"]))
    if k >= len(unique_names):
        return unique_names
    for i in range(len(unique_names)):
        start = Collection["names"].index(unique_names[i])
        dist = math.inf
        while start<len(Collection["names"]) and Collection["names"][start] == unique_names[i]:
            if(metric=="eucledian"):
                ndist = distance.euclidean(query, Collection["encodings"][i])
            elif(metric=="manhattan"):
                ndist = distance.cityblock(query, Collection["encodings"][i])
            dist = min(dist,ndist)
            start += 1
        if(len(result)<k):
            heapq.heappush(result,(-dist,unique_names[i]))
        elif(heapq.nsmallest(1,result)[0][0]<-dist):
            heapq.heapreplace(result,(-dist,unique_names[i]))
    return [pp[1] for pp in sorted(result)][::-1]


path_name = "00000002.jpg"
metric = ["eucledian", "manhattan"]

imagePath = os.path.relpath(path_name)
print(imagePath)
query = getFeatures(imagePath)

ans = KNNsearch(query,4,metric[1])
for i in ans:
    print(i)
