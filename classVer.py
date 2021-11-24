import cv2
import numpy as np
import math

def projectPoint(point, planeBasis):
    transposedBasis = planeBasis.transpose()
    #print(transposedBasis)
    middle = np.matmul(transposedBasis, planeBasis)
    #print(middle)
    invMiddle = np.linalg.inv(middle)
    #print(invMiddle)
    return np.matmul(np.matmul(invMiddle, transposedBasis), point)

def get3dPoints(rad, angle, zDist):
    coorList = []
    coorList.append([[rad*math.cos(angle), rad*math.sin(angle), zDist], [rad*math.cos(angle+math.pi/2), rad*math.sin(angle+math.pi/2), zDist],[rad*math.cos(angle+math.pi), rad*math.sin(angle+math.pi), zDist],[rad*math.cos(angle+math.pi/2*3), rad*math.sin(angle+math.pi/2*3), zDist]])
    
    return np.float32([[rad*math.cos(angle), rad*math.sin(angle), zDist], [rad*math.cos(angle+math.pi/2), rad*math.sin(angle+math.pi/2), zDist],[rad*math.cos(angle+math.pi), rad*math.sin(angle+math.pi), zDist],[rad*math.cos(angle+math.pi/2*3), rad*math.sin(angle+math.pi/2*3), zDist]])

def zRotatePlanes(length, angle, zDist):
    center = [0,0,zDist]
    coorList = []
    rectPoints = []
    #point order: upper back left->clockwise->down back left->clockwise
    rectPoints.append([-length/2+300, math.sqrt(2)*length/2*math.cos(angle+math.pi)+30, math.sqrt(2)*length/2*math.sin(angle+math.pi)+zDist])
    rectPoints.append([length/2+300, math.sqrt(2)*length/2*math.cos(angle+math.pi)+30, math.sqrt(2)*length/2*math.sin(angle+math.pi)+zDist])
    rectPoints.append([length/2+300, math.sqrt(2)*length/2*math.cos(angle+math.pi/2)+30, math.sqrt(2)*length/2*math.sin(angle+math.pi/2)+zDist])
    rectPoints.append([-length/2+300, math.sqrt(2)*length/2*math.cos(angle+math.pi/2)+30, math.sqrt(2)*length/2*math.sin(angle+math.pi/2)+zDist])
    rectPoints.append([-length/2+300, math.sqrt(2)*length/2*math.cos(angle+math.pi*3/2)+30, math.sqrt(2)*length/2*math.sin(angle+math.pi*3/2)+zDist])
    rectPoints.append([length/2+300, math.sqrt(2)*length/2*math.cos(angle+math.pi*3/2)+30, math.sqrt(2)*length/2*math.sin(angle+math.pi*3/2)+zDist])
    rectPoints.append([length/2+300, math.sqrt(2)*length/2*math.cos(angle)+30, math.sqrt(2)*length/2*math.sin(angle)+zDist])
    rectPoints.append([-length/2+300, math.sqrt(2)*length/2*math.cos(angle)+30, math.sqrt(2)*length/2*math.sin(angle)+zDist])
    
    coorList.append(np.float32([rectPoints[4], rectPoints[5], rectPoints[6], rectPoints[7]]))
    coorList.append(np.float32([rectPoints[0], rectPoints[3], rectPoints[7], rectPoints[4]]))
    coorList.append(np.float32([rectPoints[3], rectPoints[7], rectPoints[6], rectPoints[2]]))
    coorList.append(np.float32([rectPoints[2], rectPoints[6], rectPoints[5], rectPoints[1]]))
    coorList.append(np.float32([rectPoints[1], rectPoints[5], rectPoints[4], rectPoints[0]]))
    coorList.append(np.float32([rectPoints[0], rectPoints[1], rectPoints[2], rectPoints[3]]))
    return coorList

def projectPlane(points3d, screenBasis):
    projectedPointList = []
    middlePoint = np.float32([(points3d[0][0]+points3d[2][0])/2, (points3d[0][1]+points3d[2][1])/2, (points3d[0][2]+points3d[2][2])/2])

    maxDist = 0
    for i in points3d:
        projectedCoor = projectPoint(i, screenBasis)
        projectedVec = np.matmul(screenBasis, projectedCoor)
        #print(projectedVec)
        orthoVec = i - projectedVec
        #print(orthoVec)
        dist = np.linalg.norm(orthoVec)
        if maxDist<dist:
            maxDist = dist
        projectedPointList.append([projectedCoor[0]/abs(dist)*100+screenWidth/2, projectedCoor[1]/abs(dist)*100+screenHeight/2])

    projectedMiddleCoor = projectPoint(middlePoint, screenBasis)
    return np.linalg.norm(middlePoint), np.float32(projectedPointList)

def traceRay(image, ray, planes, depth):
    if depth>=depthLimit:
        return np.array([0,0,0])
    intersectList = []
    intersectPnts = []
    dists = []
    minDist = 9999999999999
    finalIntersectPoint = ()
    for i in planes:
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

img = cv2.imread('diamond_ore.png', cv2.IMREAD_COLOR)
cv2.imshow("hello", img)
cv2.waitKey(1000)

print(math.pi)
print(math.cos(math.pi/2))

imgWidth = len(img)
imgHeight = len(img[0])
print(str(imgWidth)+" "+str(imgHeight))
whiteImg = np.ones_like(img)
screenWidth = 500
screenHeight = 500
originalPnts = np.float32([[0,0], [0,imgHeight], [imgWidth, imgHeight], [imgWidth, 0]])


screenBasis = np.float32([[0.5,0],[0,0.5],[0,0]])

planes = []

angle = 0
cv2.waitKey(3000)
while angle<math.pi*2:
    #print('\n\nangle:'+str(angle))
    plane = zRotatePlanes(500,angle,1000)
    #print('get3dPoints')
    #print(points3d)

    projectedPlaneCoor = []
    planeDists=[]
    masks = []
    projectedImgs = []
    projectedPlanes = []
    finalImg = np.zeros((screenWidth, screenHeight,3))

    for i in plane:
        dist, projectedPlaneCoor = projectPlane(i, screenBasis)
        projectedPlanes.append(projectedPlaneCoor)
        planeDists.append(dist)
    
    listLen = len(planeDists)
    for i in range(listLen):
        for j in range(i,listLen):
            if planeDists[i]<planeDists[j]:
                tmpDist = planeDists[i]
                planeDists[i] = planeDists[j]
                planeDists[j] = tmpDist
                tmpPlaneCoor = projectedPlanes[i]
                projectedPlanes[i] = projectedPlanes[j]
                projectedPlanes[j] = tmpPlaneCoor

    for i in range(listLen):
        m = cv2.getPerspectiveTransform(originalPnts, projectedPlanes[i])
        resultImg = cv2.warpPerspective(img, m, dsize = (screenWidth, screenHeight))
        mask = cv2.warpPerspective(whiteImg, m, dsize = (screenWidth, screenHeight))

        projectedImgs.append(resultImg)
        masks.append(mask)

    finalImg = np.zeros((screenWidth, screenHeight,3))
    for i in range(listLen):
        if i==0:
            finalImg = projectedImgs[0]
        else:
            mask_inv = cv2.bitwise_not(masks[i]*255)
            restImg = cv2.bitwise_and(mask_inv, finalImg)
            finalImg= restImg+projectedImgs[i]

    cv2.imshow('resultImg', finalImg)
    cv2.waitKey(1)
    angle+=math.pi/100

