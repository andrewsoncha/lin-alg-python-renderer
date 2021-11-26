import numpy as np
import cv2
import linAlg
class rayTracer:

    def __init__(self, originPoint=[0,0,0], direction=[0,0,1], dist=5, resolution=[300,300, 3],depthLimit=5,alpha=0.8):
        self.originPoint = linAlg.point(originPoint)
        rayList = []
        xAxisVec = linAlg.vector([0,-1,0])#todo: change it to be adaptive to the direction vector 
        yAxisVec = linAlg.vector([1,0,0])#todo: change it to be adaptive to the direction vector
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
                endPoint = self.originPoint.coorVec+self.direction*dist+xAxisVec*(i-resolution[0]/2)+yAxisVec*(j-resolution[1]/2)
                rayRowList.append(linAlg.ray(self.originPoint, endPoint))
            rayList.append(rayRowList)
        self.rayList = rayList
        self.alpha = alpha
                
    def render(self, objList):
        resultImg = np.zeros(self.resolution)
        refImg = np.zeros(self.resolution)
        for i in range(self.resolution[0]):
            for j in range(self.resolution[1]):
                num, resultImg[i][j] = self.traceRay(self.rayList[i][j], objList, 1)
                refImg[i][j] = [num*30,num*30,num*30]
        print('refImg:')
        print(refImg)
        cv2.imshow('refImg', refImg.astype(dtype='uint8'))
        cv2.waitKey(10)
        #print('resultImg:')
        #print(resultImg)
        return resultImg


    def traceRay(self, ray, objList, depth):
        if depth>=self.depthLimit:
            return np.array([0,0,0])
        dists = []
        distMax = 9999999999999
        minDist = distMax
        finalIntersectPoint = ()
        finalHitObj = None
        for i in objList:
            intersectList = i.is_intersection(ray)
            if intersectList!=False:
                """print('intersectList:'+str(intersectList))
                print('intersectPoint:'+str(i.coorToVec(intersectList)))
                print('line span:'+str(ray.startingPoint.coorVec+ray.direction*intersectList[0]))
                print(i.originPoint.coorVec)"""
                if intersectList[0]>0:
                    intersectPnt = ray.startingPoint.coorVec+ray.direction*intersectList[0]
                    diff = ray.startingPoint.coorVec-intersectPnt
                    if minDist > diff.norm:
                        #print('coor: ('+str(intersectList[1])+','+str(intersectList[2])+')')
                        #print('width, height:'+str(i.width)+" "+str(i.height))
                        if intersectList[1]<0 or intersectList[2]<0:
                            break
                        if intersectList[1]>i.width or intersectList[2]>i.height:
                            break
                        minDist = diff.norm
                        finalHitObj = i
                        finalIntersectPoint = intersectPnt
                        #print('intersectPnt:'+str(intersectPnt))
                        intersectCoor = [intersectList[1], intersectList[2]]
                        #print('intersectCoor:'+str(intersectCoor))
        #print('finalHitobj:'+str(finalHitObj))
        #print('minDist:'+str(minDist))
        if minDist<distMax:
            #print('the ray finally hit something!!!')
            coor = intersectCoor
            reflectanceRay = ray.reflectRay(finalHitObj)
            color = finalHitObj.getCoorColor(coor)
            reflectCol = self.traceRay(reflectanceRay, objList, depth+1)
            print('reflectCol:'+str(reflectCol[1]))
            return finalHitObj.num, self.alpha*color+(1-self.alpha)*reflectCol[1]
            print('finalHitObj.num:'+str(finalHitObj.num))
            #return finalHitObj.num, self.alpha*color
            #return color
        else:
            #print('ray did not hit anything')
            if ray.direction.coorList[1]>0:
                return 0, np.array([200,200,200],np.float32)
            else:
                return 0, np.array([30,30,30],np.float32)
