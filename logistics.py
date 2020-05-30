from hash import HashTable

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
        self.charter = HashTable()
        self.weight = 0.0
        self.count = 0 #FIXME: implement getSize() method for hashtable
        self.max = self.MAX_PACKAGES

    # Add a package to the load
    # Time Complexity: O(n)
    def addPackage( self, package ):
        if not _isFull():
            self.charter.put( package )
            self.count += 1
        else:
            return 'Maxmimum Load reached'

    def removePackage( self, id ):
        self.charter.remove( id, package )
        self.count -= 1

    def _isFull( self ):
        return count > max

class Truck( object ):
    VELOCITY = 18.0
    SECONDS_PER_HOUR = 3200.0

    def __init__( self, id, startTime, location ):
        self.id = int( id )
        self.currentTime = startTime
        self.location = location
        self.distanceTraveled = 0
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

