import numpy as np
import cv2
import linAlg
from rayTracerModule import rayTracer
import cv2
import math

def zRotatePlanes(length, angle, zDist, img):
    center = [0,0,zDist]
    planeList = []
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

    """
    rectPoints.append(-length,-length,zDist+length)
    rectPoints.append(length, -length,zDist+length)
    
    rectPoints.append(-length,length,zDist+length)
    rectPoint.append()

    a = linAlg.face([rectPoints[4], rectPoints[5], rectPoints[6], rectPoints[7]], None)"""
    planeList.append(linAlg.face([rectPoints[4], rectPoints[7], rectPoints[6], rectPoints[5]], 1, None))
    #planeList.append(linAlg.face([rectPoints[0], rectPoints[4], rectPoints[7], rectPoints[3]], 2, img))
    #planeList.append(linAlg.face([rectPoints[3], rectPoints[7], rectPoints[6], rectPoints[2]], 3, img))
    #planeList.append(linAlg.face([rectPoints[2], rectPoints[6], rectPoints[5], rectPoints[1]], 4, img))
    planeList.append(linAlg.face([rectPoints[1], rectPoints[5], rectPoints[4], rectPoints[0]], 5, img))
    #planeList.append(linAlg.face([rectPoints[0], rectPoints[3], rectPoints[2], rectPoints[1]], 6, img))
    
    return planeList

def zRotatePlane(angle, zDist, img):
    rectPoints = []
    rectPoints.append([-30,0,zDist])
    rectPoints.append([0,-30*math.cos(angle),zDist-30*math.sin(angle)])
    rectPoints.append([30,0,10])
    rectPoints.append([0,30*math.cos(angle),zDist+30*math.sin(angle)])
    planeList = [linAlg.face(rectPoints, 1, img)]
    return planeList
a = linAlg.vector([1,2,3])
print(a.normalize())
planeImg = cv2.imread('diamond_ore.png', cv2.IMREAD_COLOR)
renderer = rayTracer(resolution = [50,50, 3], alpha=0.65)
planeList = zRotatePlanes(300,math.pi/10,150, planeImg)
print(len(planeList))
b = linAlg.face([[-30,0,10],[0,-30,10],[30,0,10],[0,30,10]], 1, planeImg)
#render_result = renderer.render([b]).astype(dtype='uint8')
render_result = renderer.render(planeList).astype(dtype='uint8')
#render_result = renderer.render(zRotatePlane(math.pi/10,10,planeImg))
render_result = cv2.resize(render_result, dsize=(200,200))
#render_result = cv2.rotate(render_result, cv2.ROTATE_180)
cv2.imshow('result', render_result)
cv2.imshow('planeImg', planeImg)
print(type(render_result))
print(type(planeImg))
print(render_result)
cv2.imwrite('render_result.jpg', render_result)
cv2.waitKey(10)
