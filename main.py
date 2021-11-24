import numpy
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
    rectPoints.append([-length/2+300, math.sqrt(2)*length/2*math.cos(angle+math.pi)+30, math.sqrt(2)*length/2*math.sin(angle+math.pi)+zDist])
    rectPoints.append([length/2+300, math.sqrt(2)*length/2*math.cos(angle+math.pi)+30, math.sqrt(2)*length/2*math.sin(angle+math.pi)+zDist])
    rectPoints.append([length/2+300, math.sqrt(2)*length/2*math.cos(angle+math.pi/2)+30, math.sqrt(2)*length/2*math.sin(angle+math.pi/2)+zDist])
    rectPoints.append([-length/2+300, math.sqrt(2)*length/2*math.cos(angle+math.pi/2)+30, math.sqrt(2)*length/2*math.sin(angle+math.pi/2)+zDist])
    rectPoints.append([-length/2+300, math.sqrt(2)*length/2*math.cos(angle+math.pi*3/2)+30, math.sqrt(2)*length/2*math.sin(angle+math.pi*3/2)+zDist])
    rectPoints.append([length/2+300, math.sqrt(2)*length/2*math.cos(angle+math.pi*3/2)+30, math.sqrt(2)*length/2*math.sin(angle+math.pi*3/2)+zDist])
    rectPoints.append([length/2+300, math.sqrt(2)*length/2*math.cos(angle)+30, math.sqrt(2)*length/2*math.sin(angle)+zDist])
    rectPoints.append([-length/2+300, math.sqrt(2)*length/2*math.cos(angle)+30, math.sqrt(2)*length/2*math.sin(angle)+zDist])

    a = linAlg.face([rectPoints[4], rectPoints[5], rectPoints[6], rectPoints[7]], None)
    planeList.append(linAlg.face([rectPoints[4], rectPoints[5], rectPoints[6], rectPoints[7]], img))
    planeList.append(linAlg.face([rectPoints[0], rectPoints[3], rectPoints[7], rectPoints[4]], img))
    planeList.append(linAlg.face([rectPoints[3], rectPoints[7], rectPoints[6], rectPoints[2]], img))
    planeList.append(linAlg.face([rectPoints[2], rectPoints[6], rectPoints[5], rectPoints[1]], img))
    planeList.append(linAlg.face([rectPoints[1], rectPoints[5], rectPoints[4], rectPoints[0]], img))
    planeList.append(linAlg.face([rectPoints[0], rectPoints[1], rectPoints[2], rectPoints[3]], img))
    return planeList

a = linAlg.point([0,1,1])
b = linAlg.point([1,1,0])
print(a.coorVec+b.coorVec)
planeImg = cv2.imread('diamond_ore.png', cv2.IMREAD_COLOR)
renderer = rayTracer(resolution = [10,10])
planeList = zRotatePlanes(500,0,1000, planeImg)
print(len(planeList))
render_result = renderer.render(planeList)
cv2.imshow('result', render_result)
cv2.waitKey(10)