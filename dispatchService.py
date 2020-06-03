import csv
from hash import HashTable
from graph import Graph
from logistics import Location
from logistics import Package
from logistics import Load
from logistics import Truck
from queue import SimpleQueue
from status import Status

class DispatchService( object ):
    SECONDS_PER_HOUR = 3600
    GROUP_ONE = [13, 14, 15, 16, 19, 20]
    GROUP_TWO = [3, 36, 18, 38]
    DELAYED_PACKAGES = [6, 25, 28, 32]
    INCORRECT_PACKAGES = [9]
    DELAY_TIME = 9.1 * SECONDS_PER_HOUR # 9:05am
    CORRECTION_TIME = 10.4 * SECONDS_PER_HOUR # 10:20am

    def __init__( self ):
        self.locations = self._getLocations()
        self.graph = Graph()
        self._createGraph()
        self.packages = self._getPackages()
        self.currentTime = 8 * self.SECONDS_PER_HOUR
        self.log = []

    def update( self, fleet ):
        self.currentTime += 1
        for truck in fleet:
            # Check if truck is ready to be loaded
            if truck.location is truck.hub and truck.load.charter.length() is 0:
                truck.assignLoad( self.getLoad( Load.MAX_PACKAGES, truck ) )
            else:
                # Register deliveries in package ledger
                if truck.delivering and truck.currentDelivery is not False:
                    self.deliverPackage( truck.currentDelivery )

    # Push packages to new load queue based on size
    # Time Complexity: O(n)
    def getLoad( self, size, truck = None ):
        load = Load()
        while ( load.getCount() < size ):
            nextPackage = self._assignPackage( truck )
            if nextPackage is not False:
                load.addPackage( nextPackage )
                self.loadPackage( nextPackage )
            else:
                self.log.append( 'No more packages to load ' )
                # Exit condition for while loop
                break

        self.log.append( 'Load Size: ' + str( load.getCount() ) )
        return load

    # Swap data in and out of packages hash table
    # Time Complexity: O(1)
    def loadPackage( self, package ):
        tempPackage = self.packages.get( package.id )

        # Swap with package status changed
        self.packages.remove( package.id, tempPackage )
        tempPackage.setToInTransit()
        self.packages.put( tempPackage.id, tempPackage)

    # Swap data in and out of packages hash table
    # Time Complexity: O(1)
    def deliverPackage( self, package ):
        tempPackage = self.packages.get( package.id )

        # Swap with package status changed
        self.packages.remove( package.id, tempPackage )
        tempPackage.setToDelivered()
        self.packages.put( tempPackage.id, tempPackage )

    def getLocationByAddress( self, address ):
        node = self.graph.getNodeByAddress( address )
        return node.location

    # Return True if any packages need to be delivered
    def isActive( self ):
        result = False

        for package in self.packages.getAll():
            if package.status is not Status.DELIVERED:
                result = True
        return result

    def _assignPackage( self, truck ):
        # The selection algorithm for packages uses a heuristic model
        # A queue is used to load highest priority first
        # The queue can be dumped if an extremely urgent package is found
        # Time Complexity: O(n) for each heuristic
        allPackages = self.packages.getAll()
        priorityList = SimpleQueue()

        # Check for packages that must ship together
        for package in allPackages:
            if package.id in self.GROUP_ONE:
                priorityList.push( package )

        # Check for packages with time sensitive requirements
        for package in allPackages:
            if package.id in self.DELAYED_PACKAGES:
                if self.currentTime > self.DELAY_TIME:
                    priorityList.push( package )

            # Hot fix for incorrect postage
            elif package.id in self.INCORRECT_PACKAGES:
                if self.currentTime >= self.CORRECTION_TIME:
                    self._updatePackageNine()
                    priorityList.push( package )

        # Check if package needs a target truck
        if truck is not None:
            for package in allPackages:
                if truck.id == 2 and package.id in self.GROUP_TWO:
                    priorityList.push( package )

        # Push remaining packages if no heuristic is required
        for package in allPackages:
            if str( package.notes ) == '':
                priorityList.push( package )

        # Pop items of the prioritized list until a suitable package returns
        # Time Complexity: O(n)
        for i in range( priorityList.length() ):
            selection = priorityList.peek()
            if selection.status is not Status.STAGED:
                priorityList.pop()
            elif selection.status:
                return selection

        # Catch empty result
        return False

    def _updatePackageNine( self ):
        if self.currentTime >= self.CORRECTION_TIME:
            # Swap out object with corrected object
            tempPackage = self.packages.get( 9 )
            self.packages.remove( 9, tempPackage )
            tempPackage.address = '410 S State St.'
            tempPackage.city = 'Salt Lake City'
            tempPackage.state = 'UT'
            tempPackage.zip = '84111'
            tempPackage.notes = ''
            self.packages.put( tempPackage.id, tempPackage )

    # Add nodes and edges to graph
    # Time Complexity: O(n)
    def _createGraph( self ):

        # Add locations to graph as nodes
        self._addLocationsToGraph()

        # Add distances to graph as edges
        self._addDistancesToGraph()

    # Pull locations from spreadsheet
    # Time Complexity: O(n)
    def _getLocations( self ):
        table = HashTable(10)

        # Add locations to hash table
        with open( 'data/locations.csv' ) as file:
            locationData = csv.reader( file, delimiter=',' )
            # Iterate through locations
            # Time Complexity: O(n)
            for row in locationData:
                location = Location( row[0], row[1], row[2] )
                # Add location to hash table of locations
                table.put( int( location.id ), location )

        return table

    # Add all locations to graph as nodes
    # Time Complexity: O(n)
    def _addLocationsToGraph( self ):
        locations = self.locations.getAll()
        for location in locations:
            self.graph.addNode( location )

    # Add all distances to graph as edges based on existing nodes
    # Time Complexity: O(n^2)
    def _addDistancesToGraph( self ):
        with open( 'data/distanceTable.csv' ) as file:
            distanceData = csv.reader( file, delimiter=',' )

            # Iterate through distance columns and rows
            # Enumerate is alternative to row and column indexes
            for x, row in enumerate( distanceData ):
                for y, weight in enumerate( row ):
                    if not weight == '':
                        # Add directional edges
                        self.graph.addWeightedEdge(
                            self.locations.get( x ),
                            self.locations.get( y ),
                            float( weight )
                        )

    # Pull data from spreadsheet
    # Time Complexity: O(n)
    def _getPackages( self ):
        packages = HashTable(10)
        with open('data/packageFile.csv') as file:
            packageData = csv.reader( file, delimiter = ',' )
            for row in packageData:
                package = Package(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5],
                    row[6],
                    row[7]
                )
                package.setLocation( self.getLocationByAddress( row[1] ) )
                packages.put( package.id, package )
        return packages

''' DEBUG CODE
dispatch = DispatchService()
HUB = dispatch.locations.get(0)
truck = Truck( 1, HUB )
truck.assignLoad( dispatch.getLoad( 16, truck ) )
print( '-------------')
truck = Truck( 2, HUB )
truck.assignLoad( dispatch.getLoad( 16, truck ) )
dispatch.currentTime = dispatch.CORRECTION_TIME
print( '-------------')
truck = Truck( 1, HUB )
truck.assignLoad( dispatch.getLoad( 16, truck ) )
for package in dispatch.packages.getAll():
    if package.status == Status.STAGED:
        print( str( package.id ) + ': ' + package.notes )
'''