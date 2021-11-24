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
    rectPoints.append([-length/2, math.sqrt(2)*length/2*math.cos(angle+math.pi), math.sqrt(2)*length/2*math.sin(angle+math.pi)+zDist])
    rectPoints.append([length/2, math.sqrt(2)*length/2*math.cos(angle+math.pi), math.sqrt(2)*length/2*math.sin(angle+math.pi)+zDist])
    rectPoints.append([length/2, math.sqrt(2)*length/2*math.cos(angle+math.pi/2), math.sqrt(2)*length/2*math.sin(angle+math.pi/2)+zDist])
    rectPoints.append([-length/2, math.sqrt(2)*length/2*math.cos(angle+math.pi/2), math.sqrt(2)*length/2*math.sin(angle+math.pi/2)+zDist])
    rectPoints.append([-length/2, math.sqrt(2)*length/2*math.cos(angle+math.pi*3/2), math.sqrt(2)*length/2*math.sin(angle+math.pi*3/2)+zDist])
    rectPoints.append([length/2, math.sqrt(2)*length/2*math.cos(angle+math.pi*3/2), math.sqrt(2)*length/2*math.sin(angle+math.pi*3/2)+zDist])
    rectPoints.append([length/2, math.sqrt(2)*length/2*math.cos(angle), math.sqrt(2)*length/2*math.sin(angle)+zDist])
    rectPoints.append([-length/2, math.sqrt(2)*length/2*math.cos(angle), math.sqrt(2)*length/2*math.sin(angle)+zDist])
    
    coorList.append([rectPoints[4], rectPoints[5], rectPoints[6], rectPoints[7]])
    coorList.append([rectPoints[0], rectPoints[3], rectPoints[7], rectPoints[4]])
    coorList.append([rectPoints[3], rectPoints[7], rectPoints[6], rectPoints[2]])
    coorList.append([rectPoints[2], rectPoints[6], rectPoints[5], rectPoints[1]])

    coorList.append([rectPoints[1], rectPoints[5], rectPoints[4], rectPoints[0]])
    coorList.append([rectPoints[0], rectPoints[1], rectPoints[2], rectPoints[3]])
    return np.float32(coorList)

def projectPlane(points3d, screenBasis):
    projectedPointList = []
    middlePoint = np.float32([(points3d[0][0]+points3d[2][0])/2, (points3d[0][1]+points3d[2][1])/2, (points3d[0][2]+points3d[2][2])/2])

    for i in points3d:
        projectedCoor = projectPoint(i, screenBasis)
        projectedVec = np.matmul(screenBasis, projectedCoor)
        #print(projectedVec)
        orthoVec = i - projectedVec
        #print(orthoVec)
        dist = np.linalg.norm(orthoVec)
        #print('dist')
        #print(dist)
        #print(dist*projectedCoor)
        #print('projectedCoor:')
        #print(projectedCoor)
        projectedPointList.append([projectedCoor[0]/abs(dist)*500+screenWidth/2, projectedCoor[1]/abs(dist)*500+screenHeight/2])

    projectedMiddleCoor = projectPoint(middlePoint, screenBasis)
    projectedMiddleVec = np.matmul(screenBasis, projectedMiddleCoor)
    orthoMiddleVec = i - projectedMiddleVec
    middleDist = np.linalg.norm(orthoMiddleVec)
    return middleDist, np.float32(projectedPointList)

print(math.pi)
print(math.cos(math.pi/2))

screenWidth = 500
screenHeight = 500
screenBasis = np.float32([[1,0],[0,1],[0,0]])

planes = []

angle = 0


while angle<math.pi*2:
    #print('\n\nangle:'+str(angle))
    plane = zRotatePlanes(500,angle,1000)
    #print(plane)

    projectedPlanes = []
    planeDists=[]
    masks = []
    projectedImgs = []
    finalImg = np.zeros((screenWidth, screenHeight, 3))
    #print('shape:'+str(finalImg.shape))

    for i in plane:
        dist, projectedPlaneCoor = projectPlane(i, screenBasis)
        projectedPlanes.append(projectedPlaneCoor)
        planeDists.append(planeDists)

    for i in projectedPlanes:
        #print('i:'+str(i))
        finalImg = cv2.line(finalImg, (int(i[0][0]), int(i[0][1])), (int(i[1][0]), int(i[1][1])), (0,255,0), 5)
        finalImg = cv2.line(finalImg, (int(i[1][0]), int(i[1][1])), (int(i[2][0]), int(i[2][1])), (0,255,0), 5)
        finalImg = cv2.line(finalImg, (int(i[2][0]), int(i[2][1])), (int(i[3][0]), int(i[3][1])), (0,255,0), 5)
        finalImg = cv2.line(finalImg, (int(i[3][0]), int(i[3][1])), (int(i[0][0]), int(i[0][1])), (0,255,0), 5)
        finalImg = cv2.circle(finalImg, (int(i[0][0]), int(i[0][1])), 7, (0,0,255), -1)
        finalImg = cv2.circle(finalImg, (int(i[1][0]), int(i[1][1])), 7, (0,0,255), -1)
        finalImg = cv2.circle(finalImg, (int(i[2][0]), int(i[2][1])), 7, (0,0,255), -1)
        finalImg = cv2.circle(finalImg, (int(i[3][0]), int(i[3][1])), 7, (0,0,255), -1)
    
    cv2.imshow('resultImg', finalImg)
    cv2.waitKey(1)
    angle+=math.pi/100
