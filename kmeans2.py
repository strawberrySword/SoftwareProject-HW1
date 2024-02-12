import math
import sys

def kMeans(dataPoints, k, n, d, iter=200 ):
    # initialize centroids to first k data points
    epsilon = 0.001
    clusters = []
    centroids = []
    centroids2 = []
    for i in range(k):
        centroids.append(dataPoints[i].copy())
        centroids2.append({'center':dataPoints[i].copy(), 'size':0, 'newCenter': [0]*d})
        clusters.append(i)
    
    for i in range(k,n):
        clusters.append(-1)

    i = 0
    maxDelta = epsilon + 1
    while(i < iter and maxDelta > epsilon):
        for j in range(n):
            closestCluster = findClosestCluster(dataPoints[j], centroids)
            clusters[j] = closestCluster
            centroids2[closestCluster]['newCenter'] = [a + b for a, b in zip(centroids2[closestCluster]['newCenter'], dataPoints[j])]

        for j in range(k):
            size = clusters.count(j)
            centroids[j] = [0]*d
            for index in range(n):
                if clusters[index] == j:
                    for t in range(d):
                        centroids[j][t] += (dataPoints[index][t])/(size)
        
        i += 1
    
    for u in centroids:
        formatted = [ '%.4f' % elem for elem in u ]
        print(','.join(formatted))

def findClosestCluster(datapoint, centroids):
    minDistance = calcEclideanDistance(centroids[0], datapoint)
    closestCluster = 0
    for index, u in enumerate(centroids):
        distance = calcEclideanDistance(u, datapoint)
        if(distance < minDistance):
            minDistance = distance
            closestCluster = index
    return closestCluster

def calcEclideanDistance(u, v):
    squareSum = 0
    for i in range(len(u)):
        squareSum += (u[i] - v[i])*(u[i] - v[i])
    return math.sqrt(squareSum)

def parseArgs(args):
    try:
        n = int(args[2])
        if(n < 2):
            exit()
    except:
        print("Invalid number of points!")
        exit()
    try:
        k = int(args[1])
        if(k < 2 or k > n):
            exit()    
    except:
        print("Invalid number of clusters!")    
        exit()
    try:
        d = int(args[3])
        if(d<=0):
            exit()    
    except:
        print("Invalid dimension of point!")
        exit()
    if len(args) == 5:
        iter = 200
        filePath = args[4]
    if len(args) == 6:
        try:
            iter = int(args[4])
            if(iter < 2 or iter >= 1000):
                exit()
        except:
            print("Invalid maximum iteration!")
            exit()
        filePath = args[5]
    return k, n, d, iter, filePath

def parseDataPoints(filePath):
    f = open(filePath, 'r')
    raw = f.read()
    lines = raw.split('\n')
    dataPoints = [l.split(',') for l in lines if len(l) > 0 ]
    dataPoints = [[float(x) for x in dp] for dp in dataPoints]

    f.close()
    return dataPoints

if __name__ == '__main__':
    k, n, d, iter, filePath = parseArgs(sys.argv)
    list = parseDataPoints(filePath)
    kMeans(list, k, n, d, iter)

    try:
        kMeans(list, k, n, d, iter)
    except:
        print("An Error Has Occurred")
        exit()