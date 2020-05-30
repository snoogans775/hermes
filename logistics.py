from queue import SimpleQueue

class Package( object ):
    def __init__( self, id, address, deadline, city, zip, weight, status ):
        self.id = int( id )
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zip = zip
        self.weight = weight
        self.status = status

class Load( object ):
    MAX_PACKAGES = 16
    # A load is a set of packages to be assigned to a truck
    # Time Complexity: O(1)
    def __init__( self ):
        self.charter = SimpleQueue()
        self.count = 0
        self.max = self.MAX_PACKAGES

    # Add a package to the load: O(1)
    def addPackage( self, package ):
        if not self._isFull():
            self.charter.push( package )
            self.count += 1
        else:
            return 'Maxmimum Load reached'

    # Remove package from load: O(1)
    def removePackage( self ):
        self.charter.pop()
        self.count -= 1

    def getCount( self ):
        return self.count

    def _isFull( self ):
        return self.charter.length() >= self.max

class Truck( object ):
    VELOCITY = 18.0
    SECONDS_PER_HOUR = 3200.0

    def __init__( self, id, startTime, location ):
        self.id = int( id )
        self.currentTime = startTime
        self.location = location
        self.distanceToNextStop = 0
        self.load = Load()

    def assignLoad( self, load ):
        self.load = load

    def updateTime( self, time ):
        self.currentTime = time

class Location( object ):
    # Location data is contained in .csv form
    # The three columns are read without headers
    def __init__( self, id, name, address ):
        self.id = int( id )
        self.name = name
        self.address = address

