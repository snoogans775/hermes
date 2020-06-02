import csv
from hash import HashTable
from graph import Graph
from logistics import Location
from logistics import Package
from logistics import Load
from queue import SimpleQueue
from status import Status

class DispatchService( object ):
    SECONDS_PER_HOUR = 3600
    GROUPED_PACKAGES = [13, 15, 19]
    DELAYED_PACKAGES = [6, 25, 28, 32]
    DELAY_TIME = 9.1 * 3600 # 9:05am
    SECOND_TRUCK_PACKAGES = [3, 36, 38]

    # Package statuses
    #FIXME: implement as enumeration
    STAGED = 'STAGED',
    IN_TRANSIT = 'IN TRANSIT',
    DELIVERED = 'DELIVERED'


    def __init__( self ):
        self.locations = self._getLocations()
        self.graph = Graph()
        self._createGraph()
        self.packages = self._getPackages()
        self.currentTime = 8 * self.SECONDS_PER_HOUR

    def getLoad( self, size, truck = None ):
        # Push packages to new load queue based on size
        # Time Complexity: O(n)
        load = Load()
        packageLength = len( self.packages.getAll() )
        while ( load.getCount() < size and packageLength > 0 ):
            # Naive method for loading packages
            nextPackage = self._getNextPackage()
            load.addPackage( nextPackage )
            #self._loadPackage( nextPackage ) #FIXME: nextPackage is bool?

        return load

    def _getNextPackage( self, truck = None ):
        # The selection algorithm for packages uses a heuristic model
        # A queue is used to load highest priority first
        # The queue can be dumped if an extremely urgent package is found
        # Time Complexity: O(n)
        allPackages = self.packages.getAll()
        priorityList = SimpleQueue()
        for package in allPackages:
            if package.status == Status.STAGED:
                print( package.id )
                # Check for packages that must ship together
                if package.id in self.GROUPED_PACKAGES:
                    priorityList.push( package )
                # Check for packages that must be delayed
                elif package.id in self.DELAYED_PACKAGES:
                    if self.currentTime > self.DELAY_TIME:
                        priorityList.push( package )
                # Check if package needs a target truck
                elif truck.id == 2:
                    if package.id in self.SECOND_TRUCK_PACKAGES:
                        priorityList.push( package )
                else:
                    priorityList.push( package )

        print( priorityList.length() )
        return priorityList.peek()

    def _loadPackage( self, package ):
        # The packages array is a hash table
        # A hash table requires a swap to change the status of an item
        # Time Complexity: O(1)
        print( 'Loading package: ' + str( package.id ) )
        tempPackage = self.packages.get( package.id )

        # Swap with package status changed
        self.packages.remove( package.id, tempPackage )
        tempPackage.setToInTransit()
        self.packages.put( tempPackage.id, tempPackage)

    def _deliverPackage( self, id ):
        # The packages object is a hash table
        # A hash table requires a swap to change the status of an item
        # Time Complexity: O(1)
        tempPackage = self.packages.get( id )

        # Swap with package status changed
        self.packages.remove( id, tempPackage )
        tempPackage.setToDelivered()
        self.packages.put( tempPackage.id, tempPackage )

    def getLocationByAddress( self, address ):
        node = self.graph.getNodeByAddress( address )
        return node.location

    # Directly modify status of package in packages
    # Time Complexity: O(n)
    def advancePackageStatus( self, package ):
        id = package.id
        return True

    # Method to determine when all packages have been delivered
    def isActive( self ):
        #FIXME: implement as SimpleQueue
        return True

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
                packages.put( package.id, package )
        return packages

dispatch = DispatchService()
print( dispatch.getLoad( 10 ) )