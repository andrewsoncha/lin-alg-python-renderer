import math
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
        normalizedCoorList = []
        for i in range(self.dimension):
            normalizedCoorList.append(self.coorList[i]/self.norm)
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
            if a.dimension == b.dimension:
                count = 0
                newCoors = []
                for i in range(a.dimension):
                    count += a.coorList[i]*b.coorList[i]

                return count
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
        for i in range(self.dimension):
            msg += "{} ".format(str(self.coorList[i]))
        return msg
