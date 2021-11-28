import numpy as np
import cv2
import linAlg
from rayTracerModule import rayTracer
import cv2
import math

def zRotatePlanes(length, angle, alphaInput, zDist, img):
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
    planeList.append(linAlg.face([rectPoints[4], rectPoints[7], rectPoints[6], rectPoints[5]], 1, alpha=alphaInput, image=None))
    #planeList.append(linAlg.face([rectPoints[0], rectPoints[4], rectPoints[7], rectPoints[3]], 2, alpha=alphaInput, image=img))
    planeList.append(linAlg.face([rectPoints[3], rectPoints[7], rectPoints[6], rectPoints[2]], 3, alpha = alphaInput, image=img))
    #planeList.append(linAlg.face([rectPoints[2], rectPoints[6], rectPoints[5], rectPoints[1]], 4, alpha=alphaInput, image = img))
    #planeList.append(linAlg.face([rectPoints[1], rectPoints[5], rectPoints[4], rectPoints[0]], 5, alpha = alphaInput, image = img))
    planeList.append(linAlg.face([rectPoints[0], rectPoints[3], rectPoints[2], rectPoints[1]], 6, alpha=alphaInput, image=img))
    
    return planeList

def zRotatePlane(angle, zDist, img):
    rectPoints = []
    rectPoints.append([-30,0,zDist])
    rectPoints.append([0,-30*math.cos(angle),zDist-30*math.sin(angle)])
    rectPoints.append([30,0,10])
    rectPoints.append([0,30*math.cos(angle),zDist+30*math.sin(angle)])
    planeList = [linAlg.face(rectPoints, 1, img)]
    return planeList

alpha = 0
fps = 20
width = 200
height = 200
fcc = cv2.VideoWriter_fourcc('H', '2', '5', '6')
out = cv2.VideoWriter('wireframe result.mp4', fcc, fps, (width, height))

planeImg = cv2.imread('diamond_ore.png', cv2.IMREAD_COLOR)
renderer = rayTracer(resolution = [100,100, 3])
while alpha<=math.pi*2:
    planeImg = cv2.imread('diamond_ore.png', cv2.IMREAD_COLOR)
    planeList = zRotatePlanes(300,alpha, alphaInput = 1, zDist = 310,img=planeImg)
    render_result = renderer.render(planeList).astype(dtype='uint8')
    render_result = cv2.resize(render_result, dsize=(200,200))
    cv2.imshow('result', render_result)
    out.write(render_result)
    cv2.waitKey(10)
    alpha+=0.05
out.release()
