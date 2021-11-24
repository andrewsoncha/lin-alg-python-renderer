import numpy
import cv2
import linAlg

class rayTracer:

    def __init__(self, originPoint=[0,0,0], direction=[1,0,0], dist=5, resolution=[300,300],depthLimit=5,alpha=0.7):
        self.originPoint = linAlg.Point(originPoint)
        self.direction = linAlg.vector(direction)
        rayList = []
        xAxisVec = linAlg.vector([0,1,0])#todo: change it to be adaptive to the direction vector 
        yAxisVec = linAlg.vector([0,0,1])#todo: change it to be adaptive to the direction vector
        for i in range(resolution[0]):
            rayRowList = []
            for j in range(resolution[1]):
                bla = self.originPoint+self.direction*dist+xAxisVec*(i-resolution[0]/2)+yAxisVec*(i-resolution[1]/2)
                endPoint = bla
                rayRowList.append(Ray(originPoint, endPoint))
            rayList.append(rayRowList)
        self.rayList = rayList
                
    def render(objList):
        resultImg = np.array(resolution)
        for i in range(resolution):
            for j in range(resolution):
                resultImg[i][j] = rayTrace(ray[i][j], objList, 1)
        return resultImg
    
    def rayTrace(ray, objList, depth):
        if depth>=depthLimit:
            return np.array([0,0,0])
        intersectList = []
        intersectPnts = []
        dists = []
        distMax = 9999999999999
        minDist = distMax
        finalIntersectPoint = ()
        finalHitObj = None
        for i in objList:
            if ray.doesHit(i):
                intersectPnt = ray.intersect(i)
                diff = ray.startPnt-intersectPnt
                if minDist < diff.norm:
                    minDist = diff.norm
                    finalHitobj = i
                    finalIntersectPoint = intersectPnt
        if minDist<distMax:
            coor = changeToCoor(intersectPnt, finalHitObj)
            reflectanceRay = getReflectance(ray, finalHitObj)
            color = finalHitObj.getCoorColor(coor)
            return alpha*color+traceRay(image, reflectanceRay, planes, depth+1)
        else:
            return np.array([125,125,125])
