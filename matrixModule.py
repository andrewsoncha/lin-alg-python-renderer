import math
import numpy as np
from vectorModule import vector

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
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
            pivRow = tmpMatrix.findRow(i)
            if pivRow != i:
                self.switchRow(i, pivRow)

            pivot = tmpMatrix.columnVectors[i].get_element(i)
            if isclose(pivot, 0):
                return tmpMatrix
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
            pivRow = tmpMatrix.findRow(i)
            if pivRow != i:
                self.switchRow(i, pivRow)

            pivot = tmpMatrix.columnVectors[i].get_element(i)
            if isclose(pivot, 0):
                return tmpMatrix
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
                pivRow = tmpMatrix.findRow(i)
                if pivRow != i:
                    self.switchRow(i, pivRow)
                    v.switchRow(i, pivRow)
                pivot = tmpMatrix.columnVectors[i].get_element(i)
                if isclose(pivot, 0):
                    return newM
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
                pivRow = tmpMatrix.findRow(i)
                if pivRow != i:
                    self.switchRow(i, pivRow)
                    v.switchRow(i, pivRow)
                
                pivot = tmpMatrix.columnVectors[i].get_element(i)
                if isclose(pivot, 0):
                    return newM
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

    def getInverseMatrixNP(self):
        arr = self.toNumpyArray()
        inv = np.linalg.inv(arr)
        vecList=[]
        for i in inv:
            vecList.append(vector(i))
        newMat = matrix(vecList, self.colN)
        return newMat

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

    def getDeterminantNP(self):
        arr = self.toNumpyArray()
        det = np.linalg.det(arr)
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
    
    def findRow(self, column):
        for i in range(self.rowN):
            if not(isclose(self.getMatrixElement(i, column), 0)):
                return i
    def switchRow(self, row1, row2):
        a = self.columnVectors[row1]
        self.columnVectors[row1] = self.columnVectors[row2]
        self.columnVectors[row2] = a

    def toNumpyArray(self):
        vecList = []
        for i in range(self.rowN):
            vecList.append(self.columnVectors[i].coorList)
        arr = np.array(vecList)
        return arr
