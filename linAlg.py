import math
import numpy as np
import cv2
from vectorModule import vector
from matrixModule import matrix

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

class point:  # represents a point in a 3-dimensional space
    # currently the Point class only has one field memeber: Vec3 coordinates. Might add other field members like color later
    def __init__(self, coorList, y_coor=None, z_coor=None):
        if isinstance(y_coor, float) or isinstance(y_coor, int):
            self.coorVec = vector([coorList, y_coor, z_coor])
        else:
            print('coorList:'+str(coorList))
            if isinstance(coorList, vector):
                self.coorVec = coorList
            else:
                self.coorVec = vector(coorList)

    def getX(self):
        return self.coorVec.coorList[0]

    def getY(self):
        return self.coorVec.coorList[1]

    def getZ(self):
        return self.coorVec.coorList[2]


# represents a line in a 3-dimensional space. Consists of one starting point(Point class) and a normalized 3d direction vector(Vec3 class)
class line:
    def __init__(self, startingPoint, direction):
        self.startingPoint = startingPoint
        if direction.norm != 1:
            self.direction = direction.normalize()
        else:
            self.direction = direction

    @classmethod
    def fromTwoPoints(cls, startingPoint, endPoint):
        diffVec = endPoint-startingPoint
        direction = diffVec.normalize()
        return cls(startingPoint, direction)

    def getDirX(self):
        return self.direction.get_element(0)

    def getDirY(self):
        return self.direction.get_element(1)

    def getDirZ(self):
        return self.direction.get_element(2)

    def isOnLine(self, point):
        # line <-> point distance <== 0 (floating point comparing)
        a = point.getX() - self.startingPoint.getX()
        b = point.getY() - self.startingPoint.getY()
        c = point.getZ() - self.startingPoint.getZ()
        xratio = a / self.getDirX()
        yratio = b / self.getDirY()
        zratio = c / self.getDirZ()
        if(isclose(xratio, yratio) and isclose(xratio, zratio)):
            return True
        else:
            return False

    def isPointFront(self, point):
        if self.isOnLine(point):
            a = point.getX() - self.startingPoint.getX()
            b = point.getY() - self.startingPoint.getY()
            c = point.getZ() - self.startingPoint.getZ()
            xratio = a / self.getDirX()
            yratio = b / self.getDirY()
            zratio = c / self.getDirZ()
            if(xratio > 0):
                return True
            else:
                return False


class plane:
    def __init__(self, originPoint, vector1, vector2):
        #point : point
        #vector1 : vector
        #vector2 : vector
        #print('plane init')
        #print('vector1:'+str(vector1))
        #print('vector2:'+str(vector2))
        self.originPoint = originPoint
        self.v1 = vector1.normalize()
        self.v2 = vector2.normalize()
        self.normalVec = vector.outer_product(vector1, vector2)
        self.normalVec = self.normalVec.normalize()
        #print('normalVec:'+str(self.normalVec))

    def is_intersection(self, line):
        #line : Line
        """print('ray:'+str(line.startingPoint.coorVec)+','+str(line.direction))
        print('plane:'+str(self.originPoint.coorVec)+','+str(self.v1)+","+str(self.v2))
        print('\n')"""
        x = self.originPoint.getX() - line.startingPoint.getX()
        y = self.originPoint.getY() - line.startingPoint.getY()
        z = self.originPoint.getZ() - line.startingPoint.getZ()

        list = [x]
        vec1 = vector(list)
        list = [y]
        vec2 = vector(list)
        list = [z]
        vec3 = vector(list)
        list = [vec1, vec2, vec3]
        mat_B = matrix(list, 3)
        list = [line.getDirX(), -self.v1.get_element(0), -self.v2.get_element(0)]
        vec4 = vector(list)
        list = [line.getDirY(), -self.v1.get_element(1), -self.v2.get_element(1)]
        vec5 = vector(list)
        list = [line.getDirZ(), -self.v1.get_element(2), -self.v2.get_element(2)]
        vec6 = vector(list)
        list = [vec4, vec5, vec6]
        mat_A = matrix(list, 9)
        """print('a:'+str(mat_A))
        print('mat_A determinant:'+str(mat_A.getDeterminantNP()))
        print('inverse:'+str(mat_A.getInverseMatrixNP()))
        print('mat_A*inverse'+str(mat_A*mat_A.getInverseMatrixNP()))
        print('mat_B:'+str(mat_B))"""
        if mat_A.getDeterminantNP() == 0:
            #print('determinant false')
            return False
        else:
            #return list[the scalar coefficient of line, the coefficient of basis1, the coefficient of basis2]
            #mat_x = mat_A.getInverseMatrix()*mat_B
            mat_x = mat_A.getInverseMatrixNP()*mat_B
            """print('mat_x:')
            print(str(mat_x))
            print('inverse:')
            print(str(mat_A.getInverseMatrix()))
            print('mat_B:')
            print(str(mat_B))
            print('x*a:')
            print(str(mat_A*mat_x))"""
            a = mat_x.getMatrixElement(0, 0)
            m = mat_x.getMatrixElement(1, 0)
            n = mat_x.getMatrixElement(2, 0)
            #print('m and n:'+str(m)+','+str(n))
            list = [a, m, n]
            #print('line span:'+str(line.startingPoint.coorVec)+"+"+str(line.direction)+"*"+str(a)+"="+str(line.startingPoint.coorVec+line.direction*a))
            #print('plane span:'+str(self.originPoint.coorVec)+"+"+str(self.v1)+"*"+str(m)+"+"+str(self.v2)+'*'+str(n)+"="+str(self.originPoint.coorVec+self.v1*m+self.v2*n))
            return list

    def coorToVec(self, coorList):
        """print('v1:'+str(self.v1))
        print(coorList[1])
        print('v2:'+str(self.v2))
        print(coorList[2])
        print('v1*cL1='+str(self.v1*coorList[1]))
        print('v2*cL2='+str(self.v2*coorList[2]))
        print('sum='+str(self.v1*coorList[1]+self.v2*coorList[2]))"""
        return self.originPoint.coorVec+self.v1*coorList[1]+self.v2*coorList[2]


class face(plane):#face of the cube or one of the walls
    def __init__(self, pointList, num=0, image=None):#pointList must be ordered as follows: Upper Left->Lower left->Lower Right->Upper Right
        #print('face init')
        leftUp = point(pointList[0])
        xAxis = vector(pointList[1])-vector(pointList[0])
        yAxis = vector(pointList[3])-vector(pointList[0])
        self.num = num
        self.pointList = pointList
        """print('leftUp:'+str(leftUp.coorVec))
        print('xAxis:'+str(xAxis))
        print('yAxis:'+str(yAxis))"""
        super(face, self).__init__(leftUp, xAxis.normalize(), yAxis.normalize())
        self.width = xAxis.findNorm()
        self.height = yAxis.findNorm()
        print("width and height:"+str(self.width)+','+str(self.height)+')')
        self.image = image
        #print('self.image type:'+str(type(self.image)))
    def getCoorColor(self, coor):
        #print('self.image type:'+str(type(self.image)))
        print('getCoorColor('+str(coor[0])+','+str(coor[1]))
        if isinstance(self.image, type(np.array(np.int32))):
            return self.image[int(coor[0]/self.width*len(self.image))%len(self.image)][int(coor[1]/self.height*len(self.image[0]))%len(self.image[0])]
        else:
            return np.array([125,125,125])

class ray(line):
    def __init__(self, startingPoint, direction):
        super().__init__(startingPoint, direction)

    @classmethod
    def fromTwoPoints(cls, startingPoint, endPoint):
        diffVec = endPoint-startingPoint
        direction = diffVec.normalize()
        super().__init__(startingPoint, direction)
    def intersect(faceObj):
        coor = faceObj.is_intersection(self)
        if coor == 0:
            return False, False
        else:
            if coor[0]<0 or coor[1]<0:
                return False, False
            elif coor[0]>faceObj.width or coor[1]>faceObj.height:
                return False, False
            else:
                point = coor[0]*faceObj.v1+coor[1]*faceObj.v2
                return point, coor
    def reflectRay(self, faceObj):
        coorList = faceObj.is_intersection(self)
        print('coorList:'+str(coorList))
        newStartingPoint = point(self.startingPoint.coorVec+self.direction*coorList[0])
        if newStartingPoint!=False:
            print('dot product:'+str(vector.dot_product(self.direction, faceObj.normalVec)))
            newDirection = -2*faceObj.normalVec*vector.dot_product(self.direction, faceObj.normalVec)+self.direction
            return ray(newStartingPoint, newDirection)
        else:
            return False
