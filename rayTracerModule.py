import numpy as np
import cv2
import linAlg
class rayTracer:

    def __init__(self, originPoint=[0,0,0], direction=[1,0,0], dist=5, resolution=[300,300],depthLimit=5,alpha=0.7):
        self.originPoint = linAlg.point(originPoint)
        rayList = []
        xAxisVec = linAlg.vector([0,1,0])#todo: change it to be adaptive to the direction vector 
        yAxisVec = linAlg.vector([0,0,1])#todo: change it to be adaptive to the direction vector
        self.direction = linAlg.vector(direction)
        self.resolution = resolution
        self.depthLimit = depthLimit
        for i in range(resolution[0]):
            rayRowList = []
            for j in range(resolution[1]):
                '''print('originPoint:'+str(originPoint))
                print('self.direction*dist:'+str(self.direction*dist))
                print('xAxisVec*(i-resolution[0]/2):'+str(xAxisVec*(i-resolution[0]/2)))
                print('yAxisVec*(i-resolution[1]/2):'+str(yAxisVec*(j-resolution[1]/2)))'''
                print(self.originPoint.coorVec+self.direction*dist+xAxisVec*(i-resolution[0]/2)+yAxisVec*(j-resolution[1]/2))
                endPoint = self.originPoint.coorVec+self.direction*dist+xAxisVec*(i-resolution[0]/2)+yAxisVec*(j-resolution[1]/2)
                rayRowList.append(linAlg.ray(originPoint, endPoint))
            rayList.append(rayRowList)
        self.rayList = rayList
                
    def render(self, objList):
        resultImg = np.array(self.resolution)
        for i in range(self.resolution[0]):
            for j in range(self.resolution[1]):
                resultImg[i][j] = self.traceRay(self.rayList[i][j], objList, 1)
        return resultImg

    def traceRay(self, ray, objList, depth):
        if depth>=self.depthLimit:
            return np.array([0,0,0])
        intersectList = []
        intersectPnts = []
        dists = []
        distMax = 9999999999999
        minDist = distMax
        finalIntersectPoint = ()
        finalHitObj = None
        for i in objList:
            if i.is_intersection(ray):
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
            return self.alpha*color+traceRay(image, reflectanceRay, planes, depth+1)
        else:
            return np.array([125,125,125])
