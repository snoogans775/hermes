from queue import SimpleQueue
from status import Status

class Package( object ):

    def __init__( self, id, address, city, state, zip, deadline, weight, notes ):
        self.id = int( id )
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = Status.STAGED
        self.location = None

    def setToInTransit( self ):
        self.status = Status.IN_TRANSIT

    def setToDelivered( self ):
        self.status = Status.DELIVERED

    def setLocation( self, location ):
        self.location = location

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

    def __init__( self, id, hub, graph ):
        self.id = int( id )
        self.load = Load()
        self.hub = hub
        self.location = self.hub
        self.destination = self.hub
        self.distanceToNextStop = 0
        self.totalDistance = 0
        self.velocity = self._getVelocity()
        self.graph = graph
        self.currentDelivery = None
        self.delivering = False

    def update( self ):
        # Register when a truck reaches a location
        if (self.distanceToNextStop <= 0):
            self.location = self.destination

        # Deliver package when at location and choose next destination
        if not (self.location.id == self.destination.id):
            # The truck is in transit
            self.delivering = False
            # Move truck forward
            self.distanceToNextStop -= self.velocity
            self.totalDistance += self.velocity

        else:
            # The truck has arrived at destination
            self.delivering = True
            # Deliver package at location
            # Direct truck to node of next package in load
            # Time Complexity: O(1)
            if ( self.load.charter.peek() is not False ):
                # Check next package
                nextPackage = self.load.charter.peek()
                # Remove package from load and report as delivered
                self.load.removePackage() #FIXME: Attempting to pop empty list at end of day
                self.currentDelivery = nextPackage

                # Select next destination
                nextLocation = self._findNextDestination()

                # Set new destination
                self.setDestination( nextLocation )

    def assignLoad( self, load ):
        self.load = load
        self.destination = self._findNextDestination()

    def setDestination( self, location ):
        self.destination = location

    def setLocation( self, location ):
        self.location = location

    # Select next destination based on current location
    # Time Complexity: O(n)
    def _findNextDestination( self ):
        # Check if another package exists in load
        nextPackage = self.load.charter.peek()
        if ( nextPackage ):
            # Next destination is the next package address
            nextLocation = nextPackage.location
        else:
            # Destination changes to hub
            nextLocation = self.hub

        # Calculate distance to next package location
        self.distanceToNextStop = self.graph.getDistanceBetween(
            self.location,
            nextLocation
        )

        return nextLocation

    def _getVelocity( self ):
        return self.VELOCITY / self.SECONDS_PER_HOUR

class Location( object ):
    # Location data is contained in .csv form
    # The three columns are read without headers
    def __init__( self, id, name, address ):
        self.id = int( id )
        self.name = name
        self.address = address