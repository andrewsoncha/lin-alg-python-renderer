import numpy
import cv2
class rayTracer:
    def __init__(self, originPoint=[0,0,0], direction=[1,0,0], dist=5, resolution=[300,300],depthLimit=5,alpha=0.7):
        self.point = originPoint
        #todo
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
        minDist = 9999999999999
        finalIntersectPoint = ()
        for i in objList:
            if ray.doesHit(i):
                intersectPnt = ray.intersect(i)
                diff = ray.startPnt-intersectPnt
                if minDist < diff.norm:
                    minDist = diff.norm
                    finalIntersectPoint = intersectPnt
                    coor = changeToCoor(intersectPnt, i)
                    reflectanceRay = getReflectance(ray, i)
        color = image[int(coor[0])][int(coor[1])]
        return alpha*color+traceRay(image, reflectanceRay, planes, depth+1)
