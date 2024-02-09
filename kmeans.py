import math
import sys

def kMeans(dataPoints, k, n, d, iter=200 ):
    # initialize centroids to first k data points
    epsilon = 0.001
    clusters = []
    centroids = []
    for i in range(k):
        centroids.append({'center': dataPoints[i].copy(), 'size': 1, 'lastDelta': 1 + epsilon})
        clusters.append(i)
    
    for i in range(k,n):
        clusters.append(-1)

    i = 0
    maxDelta = epsilon + 1
    while(i < iter and maxDelta > epsilon ):
        oldCluster = clusters[i%n]
        closestCluster = findClosestCluster(dataPoints[i%n], centroids)
        
        clusters[i%n] = closestCluster
        
        if(oldCluster == -1):
            centroids[closestCluster] = addDataPoint(centroids[closestCluster], dataPoints[i%n])  
            
        if(oldCluster != -1 and oldCluster != closestCluster):
            centroids[closestCluster] = addDataPoint(centroids[closestCluster], dataPoints[i%n])  
            centroids[oldCluster] = removeDataPoint(centroids[oldCluster], dataPoints[i%n])
            
        maxDelta = 0
        for u in centroids:
            if(u['lastDelta'] > maxDelta):
                maxDelta = u['lastDelta']
        i += 1
    print(centroids)
    print(i)

def findClosestCluster(datapoint, centroids):
    minDistance = calcEclideanDistance(centroids[0]['center'], datapoint)
    closestCluster = 0
    for index, u in enumerate(centroids):
        distance = calcEclideanDistance(u['center'], datapoint)
        if(distance < minDistance):
            minDistance = distance
            closestCluster = index
    return closestCluster

def calcEclideanDistance(u, v):
    squareSum = 0
    for i in range(len(u)):
        squareSum += (u[i] - v[i])*(u[i] - v[i])
    return math.sqrt(squareSum)
    

def addDataPoint(centroid, datapoint):
    oldCenter = centroid['center'].copy()
    for index, w in enumerate(centroid['center']):
        # ( x - 1 / x ) * oldAverage + ( 1 / x ) * newElement
        centroid['center'][index] = (centroid['size'] * w + datapoint[index])/(centroid['size'] + 1)
    newDelta = calcEclideanDistance(oldCenter, centroid['center'])
    centroid['size'] +=1
    centroid['lastDelta'] = newDelta
    return centroid

def removeDataPoint(centroid, datapoint):
    oldCenter = centroid['center'].copy()
    for index, w in enumerate(centroid['center']):
        centroid['center'][index] = ((w*centroid['size']) - datapoint[index])/(centroid['size']-1)
    newDelta = calcEclideanDistance(oldCenter, centroid['center'])
    centroid['size'] -=1
    centroid['lastDelta'] = newDelta
    return centroid

if __name__ == '__main__':
    if(len(sys.argv) < 5):
        print("An Error Has Occurred")
        exit
    try:
        k = int(sys.argv[1])
        n = int(sys.argv[2])
        d = int(sys.argv[3])
        if len(sys.argv == 5):
            iter = 200
            filePath = sys.argv[4]
        if len(sys.argv) == 6:
            iter = int(sys.argv[4])
            filePath = sys.argv[5]
        
            
        kMeans(list, k, n, d)
    except:
        print("An Error Has Occurred")

