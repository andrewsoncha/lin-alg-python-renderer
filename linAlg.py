import math

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

class vector(object):
    def __init__(self, coorList, asdf = None):  # coorList : list
        self.coorList = coorList
        self.dimension = len(coorList)
        cnt = 0
        for i in self.coorList:
            cnt += i*i
        self.norm = math.sqrt(cnt)

    def findNorm(self):
        cnt = 0
        for i in self.coorList:
            cnt += i*i
        return math.sqrt(cnt)

    def normalize(self):  # return new normalized Vector
        normalizedCoorList = self.coorList[:]
        for i in normalizedCoorList:
            i /= self.norm
        normalizedVec = vector(normalizedCoorList)
        normalizedVec.norm = 1  # Manually set norm as 1 to prevent cases where floating point arithmetic causes the norm to be something like 1.000000001
        return normalizedVec

    def __add__(self, other):
        if self.dimension != other.dimension:
            raise Exception("the dimension of vectors are different")
        newCoors = []
        for i in range(self.dimension):
            newCoors.append(self.coorList[i]+other.coorList[i])
        return vector(newCoors, self.dimension)

    def __sub__(self, other):  # self - other
        if self.dimension != other.dimension:
            raise Exception("the dimension of adding vectors are different")
        newCoors = []
        for i in range(self.dimension):
            newCoors.append(self.coorList[i]-other.coorList[i])
        return vector(newCoors, self.dimension)

    def __mul__(self, other):  # matrix times scalar
        newCoors = []
        if isinstance(other, int) or isinstance(other, float):
            for i in range(self.dimension):
                newCoors.append(self.coorList[i]*other)
            return vector(newCoors, self.dimension)
        else:
            raise Exception("the scalar is not an Integer")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, float) or isinstance(other, int):  # check if other is a int
            newCoors = []
            for i in range(self.dimension):
                newCoors.append(self.coorList[i]/other)
            return vector(newCoors)
        else:
            raise Exception("the scalar is not an Float")

    def get_element(self, index):
        return self.coorList[index]

    def dot_product(a, b):
        if isinstance(a, vector):
            if a.dimension != b.dimension:
                newCoors = []
                for i in range(a.dimension):
                    newCoors.append(a.coorList[i] * b.coorList[i])

                return vector(newCoors, a.dimension)
            else:
                raise Exception("the dimensions are different")
        else:
            raise Exception("can not product with non-matrix object")

    def outer_product(vector1, vector2):
        if vector1.dimension != 3 or vector2.dimension != 3:
            raise Exception("outer product parameters have a dimension that is not 3")
        resultCoor = [vector1.coorList[1]*vector2.coorList[2]-vector1.coorList[2]*vector2.coorList[1],
                      vector1.coorList[2]*vector2.coorList[0]-vector1.coorList[0]*vector2.coorList[2],
                      vector1.coorList[0]*vector2.coorList[1]-vector1.coorList[1]*vector2.coorList[0]]
        return vector(resultCoor)

    def __str__(self):
        msg = ""
        msg += "Dimension : "
        msg += str(self.dimension)
        msg += "\n"
        for i in range(self.dimension):
            msg += "{} ".format(str(self.coorList[i]))
        return msg


class matrix(object):
    # SW : I wrote this code assuming that the columnList is an array of vectors
    def __init__(self, columnList, dimension=None):
        if dimension:
            self.columnVectors = columnList
            self.rowN = len(columnList)
            self.colN = columnList[0].dimension
            self.dimension = self.rowN * self.colN
            self.determinant = -1
            self.rank = -1
        elif isinstance(columnList, matrix):
            vecList = []
            list = []
            for i in range(columnList.rowN):
                for j in range(columnList.colN):
                    list.append(columnList.columnVectors[i].get_element(j))
                vecList.append(vector(list))
                list = []
            self.columnVectors = vecList
            self.rowN = len(vecList)
            self.colN = vecList[0].dimension
            self.dimension = self.rowN * self.colN
        else:
            raise Exception(
                "can not make matrix with non-matrix and non-array-of-vector object")

    def createIdentity(self, size):  # create (size) X (size) identity matrix
        vecList = []
        for i in range(size):
            list = []
            for j in range(size):
                if i == j:
                    list.append(1)
                else:
                    list.append(0)
            vecList.append(vector(list))
        p = matrix(vecList, size * size)
        return p

    # following index parameters used in functions starts from 0

    def getDim(self):
        return self.rowN * self.colN

    def getMatrixElement(self, row, col):
        return self.columnVectors[row].get_element(col)

    def divideRow(self, indexRow, scalar):
        self.columnVectors[indexRow] = self.columnVectors[indexRow] / scalar

    def addRow(self, addingRow, subjectRow, scalar):
        # subjectRow -> subjectRow + addingRow * scalar
        self.columnVectors[subjectRow] = self.columnVectors[subjectRow] + \
            self.columnVectors[addingRow] * scalar

    def subRow(self, addingRow, subjectRow, scalar):
        if isinstance(scalar, float) or isinstance(scalar, int):
            self.addRow(addingRow, subjectRow, -scalar)
        else:
            raise Exception("the scalar is not a float")

    def GE(self):  # Return new Ref Matrix (Gauss Elimination
        tmpMatrix = matrix(self)
        for i in range(tmpMatrix.rowN):
            pivot = tmpMatrix.columnVectors[i].get_element(i)
            tmpMatrix.divideRow(i, pivot)
            for j in range(i + 1, tmpMatrix.colN):
                tmpMatrix.subRow(
                    i, j, tmpMatrix.columnVectors[j].get_element(i))
            if i == (tmpMatrix.rowN - 1):
                break
        return tmpMatrix

    def GEBS(self):
        tmpMatrix = matrix(self)
        for i in range(tmpMatrix.rowN):
            pivot = tmpMatrix.columnVectors[i].get_element(i)
            tmpMatrix.divideRow(i, pivot)
            for j in range(i + 1, tmpMatrix.colN):
                tmpMatrix.subRow(
                    i, j, tmpMatrix.columnVectors[j].get_element(i))
            if i == (tmpMatrix.rowN - 1):
                break
        for i in range(tmpMatrix.rowN - 1, 0, -1):
            for j in range(i - 1, -1, -1):
                pivot = tmpMatrix.columnVectors[j].get_element(i)
                tmpMatrix.subRow(i, j, pivot)
        return tmpMatrix

    def doGE(self, v):  # Retur matrix v that does same ERO
        if isinstance(v, matrix):
            tmpMatrix = matrix(self)
            newM = matrix(v)
            for i in range(tmpMatrix.rowN):
                pivot = tmpMatrix.columnVectors[i].get_element(i)
                newM.divideRow(i, pivot)
                tmpMatrix.divideRow(i, pivot)
                for j in range(i + 1, tmpMatrix.colN):
                    newM.subRow(
                        i, j, tmpMatrix.columnVectors[j].get_element(i))
                    tmpMatrix.subRow(
                        i, j, tmpMatrix.columnVectors[j].get_element(i))
                if i == (tmpMatrix.rowN - 1):
                    break
            return newM

    def doGEBS(self, v):
        if isinstance(v, matrix):
            tmpMatrix = matrix(self)
            newM = matrix(v)
            for i in range(tmpMatrix.rowN):
                pivot = tmpMatrix.columnVectors[i].get_element(i)
                newM.divideRow(i, pivot)
                tmpMatrix.divideRow(i, pivot)
                for j in range(i + 1, tmpMatrix.colN):
                    newM.subRow(
                        i, j, tmpMatrix.columnVectors[j].get_element(i))
                    tmpMatrix.subRow(
                        i, j, tmpMatrix.columnVectors[j].get_element(i))
                if i == (tmpMatrix.rowN - 1):
                    break
            for i in range(tmpMatrix.rowN - 1, 0, -1):
                for j in range(i - 1, -1, -1):
                    pivot = tmpMatrix.columnVectors[j].get_element(i)
                    newM.subRow(i, j, pivot)
                    tmpMatrix.subRow(i, j, pivot)
            return newM

    def getInverseMatrix(self):
        iM = self.createIdentity(self.rowN)
        tmpMatrix = self.doGEBS(iM)
        return tmpMatrix

    def getRank(self):
        tmpMatrix = self.doGEBS()
        cnt = 0
        for i in range(tmpMatrix.rowN):
            if isclose(tmpMatrix.getMatrixElement(i, i), 1):
                cnt = cnt + 1
        self.rank = cnt
        return cnt

    def getDeterminant(self):
        tmpMatrix = self.GEBS()
        det = 1
        for i in range(self.rowN):
            det *= self.getMatrixElement(i, i)
        self.determinant = det
        return det

    def spans(self, v):
        # todo: finds column vectors of the matrix spans v(==v is an element of the column space)
        # self * x = v (x, v = vector)
        if isinstance(v, vector):
            rrefMatrix = self.doGEBS(v)
            return rrefMatrix
        else:
            raise Exception("matrix can not span non-vector object")

    def __add__(self, other):
        if isinstance(other, matrix):
            newVecs = []
            for i in self.colN:
                if self.rolN != other.rolN or self.colN != other.colN:
                    newVecs.append(
                        self.columnVectors[i] + other.columnVectors[i])
            return matrix(newVecs)

    def __mul__(self, other):
        # todo: implement scalar multiplication and matrix multiplication
        if isinstance(other, int) or isinstance(other, float):
            newMatirx = []
            for i in self.rowN:
                newRow = []
                for j in self.colN:
                    newRow.append(self.columVectors[i][j]*other)
                newMatirx.append(newRow)
        elif isinstance(other, matrix):
            if self.colN != other.rowN:
                raise Exception(
                    "the column number of subject matrix and row number of multiplier matrix is not same")
            newMatrix = []
            for i in range(self.rowN):
                newRow = []
                for j in range(other.colN):
                    sum = 0
                    for k in range(self.colN):
                        sum += self.columnVectors[i].get_element(
                            k) * other.columnVectors[k].get_element(j)
                    newRow.append(sum)
                newMatrix.append(vector(newRow, len(newRow)))
            return matrix(newMatrix, 25)

    def getLittleMatrix(self, startRow, endRow, startCol, endCol):
        vecList = []
        for i in range(startRow, endRow + 1):
            list = []
            for j in range(startCol, endCol + 1):
                list.append(self.getMatrixElement(i, j))
            vecList.append(vector(list, len(list)))
        return matrix(vecList, (endRow - startRow + 1) * (endCol - startCol + 1))

    def __str__(self):
        msg = ""
        msg += "Dimension : {} X {}\n".format(self.rowN, self.colN)
        for i in range(self.rowN):
            for j in range(self.colN):
                msg += "{} ".format(self.columnVectors[i].get_element(j))
            msg += "\n"
        return msg


class point:  # represents a point in a 3-dimensional space
    # currently the Point class only has one field memeber: Vec3 coordinates. Might add other field members like color later
    def __init__(self, coorList, y_coor=None, z_coor=None):
        if isinstance(y_coor, float) or isinstance(y_coor, int):
            self.coorVec = vector([coorList, y_coor, z_coor])
        else:
            print('coorList:'+str(coorList))
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
    def __init__(self, point, vector1, vector2):
        #point : point
        #vector1 : vector
        #vector2 : vector
        print('plane init')
        print('vector1:'+str(vector1))
        print('vector2:'+str(vector2))
        self.point = point
        self.v1 = vector1
        self.v2 = vector2
        self.normalVec = vector.outer_product(vector1, vector2)
        self.normalVec = self.normalVec.normalize()

    def is_intersection(self, line):
        #line : Line
        x = self.point.getX() - line.startingPoint.getX()
        y = self.point.getY() - line.startingPoint.getY()
        z = self.point.getZ() - line.startingPoint.getZ()

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
        if mat_A.getDeterminant == 0:
            return False
        else:
            #return list[the scalar coefficient of line, the coefficient of basis1, the coefficient of basis2]
            mat_x = mat_A.getInverseMatrix()*mat_B
            a = mat_x.getMatrixElement(0, 0)
            m = mat_x.getMatrixElement(1, 0)
            n = mat_x.getMatrixElement(2, 0)
            list = [a, m, n]
            return list


class face(plane):#face of the cube or one of the walls
    def __init__(self, pointList, image=None):#pointList must be ordered as follows: Upper Left->Lower left->Lower Right->Upper Right
        print('face init')
        leftUp = point(pointList[0])
        xAxis = vector(pointList[1])-vector(pointList[0])
        yAxis = vector(pointList[2])-vector(pointList[0])
        self.pointList = pointList
        print('leftUp:'+str(leftUp.coorVec))
        print('xAxis:'+str(xAxis))
        print('yAxis:'+str(yAxis))
        super(face, self).__init__(leftUp, xAxis.normalize(), yAxis.normalize())
        self.width = xAxis.findNorm()
        self.height = yAxis.findNorm()
        self.image = image
    def getCoorColor(coor):
        if isinstance(image, np.array):
            return image[int(coor[0])][int(coor[1])]
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
    def reflectRay(faceObj):
        newStartingPoint, coor = intersect(faceObj)
        if newStartingPoint!=False:
            newDirection = -2*vector.dot(direction, faceObj.normalVec)*faceObj.normalVec+direction
            return ray(newStartingPoint, newDirection)
        else:
            return False
