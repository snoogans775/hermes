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
        self.deliveredAt = 0
        self.inTransitAt = 0

    def setToInTransit( self ):
        self.status = Status.IN_TRANSIT

    def setToDelivered( self ):
        self.status = Status.DELIVERED

    def setToInTransit( self ):
        self.status = Status.IN_TRANSIT

    def setLocation( self, location ):
        self.location = location

    def setDeliveryTime( self, time ):
        self.deliveredAt = time

class Load( object ):
    MIN_PACKAGES = 8
    MAX_PACKAGES = 14
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
            return 'Maximimum Load reached'

    # Remove package from load: O(1)
    def removePackage( self ):
        self.charter.pop()
        self.count -= 1

    def getCount( self ):
        return self.count

    def _isFull( self ):
        return self.charter.length() > self.max

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
        self.loading = False
        self.log = []

    def update( self ):
        # Register when a truck reaches a location
        if ( self.distanceToNextStop <= 0 ):
            self.location = self.destination

        # Deliver package when at location and choose next destination
        if not ( self.location.id == self.destination.id ):
            # The truck is in transit
            self.delivering = False

            # Move truck forward
            self.distanceToNextStop -= self.velocity
            self.totalDistance += self.velocity

        else:
            # The truck has arrived at a destination
            if self.location is self.hub:
                self.loading = True
            else:
                self.delivering = True

                if ( self.load.charter.length() > 0 ):
                    self._deliverPackage()


    def assignLoad( self, load ):
        self.load = load
        self.destination = self._findNextDestination()
        self.loading = False

    def setDestination( self, location ):
        self.destination = location

    def setLocation( self, location ):
        self.location = location

    def _deliverPackage( self ):
        # Check next package and set destination
        self.currentDelivery = self.load.charter.peek()

        if ( self.location == self.currentDelivery.location ):
            # Remove package from load
            self.load.removePackage()

        # Set new destination
        self.setDestination( self._findNextDestination() )

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