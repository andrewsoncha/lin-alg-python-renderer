import linAlg as linearAlgebra
from random import random
import numpy as np

line_point = linearAlgebra.point(0, 0, 0)
line_vec = linearAlgebra.vector([1,0,1])
testLine = linearAlgebra.line(line_point, line_vec)
plane_point = linearAlgebra.point(1,0,0)
plane_basis1 = linearAlgebra.vector([1, 0, 0])
plane_basis2 = linearAlgebra.vector([0,1,0])
testPlane = linearAlgebra.plane(plane_point, plane_basis1, plane_basis2)
print(testPlane.is_intersection(testLine))
print('\n\n\n\n\n\n')
coorList = testPlane.is_intersection(testLine)
print('coorList:'+str(coorList))
print('line span:'+str(testLine.startingPoint.coorVec+testLine.direction*coorList[0]))
print('plane span:'+str(testPlane.originPoint.coorVec+testPlane.v1*coorList[1]+testPlane.v2*coorList[2]))



vec1 = linearAlgebra.vector([1,0,1])
vec2 = linearAlgebra.vector([1,0,0])
vec3 = linearAlgebra.vector([0,1,0])
print('making matrix')
matrix = linearAlgebra.matrix([vec1,vec2,vec3], 3)
print(matrix)
print(matrix.getInverseMatrixNP())
print(matrix*matrix.getInverseMatrixNP())
npArr = matrix.toNumpyArray()
print(npArr)
print('det:'+str(np.linalg.det(npArr)))

print('\n\n\n\n')
print(testPlane.originPoint.coorVec-testLine.startingPoint.coorVec)
print(testPlane.v1*coorList[0]+testPlane.v2*coorList[1]-testLine.direction*coorList[2])
