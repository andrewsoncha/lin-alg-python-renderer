class vector:
    def __init__(coorList, dimension):
        self.coorList = coorList
        self.dimension = dimension
        self.norm = findNorm(coorList)
    def findNorm(coorList):
        cnt = 0
        for i in coorList:
            cnt+=i*i
        return sqrt(cnt)
    def normalize():
        normalizedCoorList = coorList
        for i in normalizedCoorList:
            i /= norm
        normalizedVec = __init__(normalizedCoorList, dimension)
        normalizedVec.norm = 1 #Manually set norm as 1 to prevent cases where floating point arithmetic causes the norm to be something like 1.000000001
        return normalizedVec
    def __add__(self, other):
        if self.dimension != other.dimension:
            
            #todo: make and raise exception where the dimension doesn't match
        newCoors = []
        for i in range(self.dimension):
            newCoors.append(self.coorList[i]+other.coorList[i])
        return __init__(newCoors, self.dimension)
    def __sub__(self, other):
        if self.dimension != other.dimension:
            #todo: make and raise exception where the dimension doesn't match
        newCoors = []
        for i in range(self.dimension):
            newCoors.append(self.coorList[i]-other.coorList[i])
        return __init__(newCoors, self.dimension)
    def __mul__(self, other):
        if isinstance(other, int):
            if self.dimension != other.dimension:
                #todo: make and raise exception where the dimension doesn't match
            newCoors = []
            for i in range(self.dimension):
                newCoors.append(self.coorList[i]*other)
            return __init__(newCoors, self.dimension)
        else:
            #raise some other exception
            return null
    def __div__(self, other):
        if isinstance(other, float):#check if other is a int
            if self.dimension != other.dimension:
                #todo: make and raise exception where the dimension doesn't match
            newCoors = []
            for i in range(self.dimension):
                newCoors.append(self.coorList[i]/other)
            return __init__(newCoors, self.dimension)
        else:
            #raise some other exception
            return null

class matrix:
    def __init__(columnList):
        self.columnVectors = columnList
        self.rowN = columnList[0].dimension
        self.colN = size(columnList)
    def findDim():
        #todo
    def spans(v):
        #todo: finds column vectors of the matrix spans v(==v is an element of the column space)
    def __add__(self, other):
        if isinstance(other, matrix):
            newVecs = []
            for i in colN:
                if self.rolN != other.rolN or self.colN != other.colN:
                newVecs.append(self.columnVectors[i]+other.columnVectors[i])
            return __init__(newVecs)

    def __mul__(self, other):
        #todo: implement scalar multiplication and matrix multiplication

class Vec3(vector):
    def __init__(coorList):
        super(coorList, 3)
    def __init__(x_coor, y_coor, z_coor):
        coorList = [x_coor, y_coor, z_coor]
        super(coorList, 3)

class Point:   #represents a point in a 3-dimensional space
    #currently the Point class only has one field memeber: Vec3 coordinates. Might add other field members like color later
    def __init__(coorList):
        self.coordinates = Vec3(coorList)
    def __init__(x_coor, y_coor, z_coor):
        self.coordinates = Vec3(x_coor, y_coor, z_coor)

class Line:   #represents a line in a 3-dimensional space. Consists of one starting point(Point class) and a normalized 3d direction vector(Vec3 class)
    def __init__(startingPoint, direction):
        self.startingPoint = startingPoint
        self.direction = direction
        if self.direction.norm != 1:
            self.direction = self.direction.normalize()

    def isOnLine(point):
        
