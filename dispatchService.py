import csv
import copy
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
    GROUP_ONE = [3, 13, 14, 15, 16, 18, 19, 20, 36, 38]
    DELAYED_PACKAGES = [6, 25, 28, 32]
    RUSH_PACKAGES = [6]
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

    # The update function
    def update( self, fleet ):
        self.currentTime += 1
        for truck in fleet:
            # Register deliveries in package ledger
            if truck.delivering:
                self.recordDelivery( truck.currentDelivery )
                package = self.packages.get( truck.currentDelivery.id )
                self.packages.remove( truck.currentDelivery.id, truck.currentDelivery )
                package.deliveredAt = self.currentTime
                self.packages.put( package.id, package )

    # Push packages to new load queue based on size
    # Time Complexity: O(n)
    def getLoad( self, truck = None ):
        load = Load()
        while ( load.charter.length() < Load.MAX_PACKAGES ):
            nextPackage = self._assignPackage( truck )
            if nextPackage is not False:
                load.addPackage( nextPackage )
                self.loadPackage( nextPackage )
            else:
                # Exit condition for while loop
                break

        # Optimize the load
        # If the load is too small, stop the operation
        if( load.charter.length() ) > Load.MIN_PACKAGES:
            load = self._optimizeLoad( load )
        else:
            return Load()

        return load

    # Swap data in and out of packages hash table
    # Time Complexity: O(1)
    def loadPackage( self, package ):
        tempPackage = self.packages.get( package.id )

        # Swap with package status changed
        self.packages.remove( package.id, tempPackage )
        tempPackage.setToInTransit()
        tempPackage.inTransitAt = self.currentTime
        self.packages.put( tempPackage.id, tempPackage)

    # Swap data in and out of packages hash table
    # Time Complexity: O(1)
    def recordDelivery( self, package ):
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

    # Greedy algorithm for load optimization
    # Time Complexity O(logN)
    # Complexity decreases as available nodes decreases in sort
    def _optimizeLoad( self, load ):
        outputLoad = Load()
        packages = []

        while load.charter.length() > 0:
            packages.append( load.charter.pop() )

        # Sort packages by distance from arbitrary item in list
        '''
        firstPackage = packages[4]
        packages.sort( key = lambda x: self._getDistanceBetweenPackages( firstPackage.location, x.location ))
        for package in packages:
            outputLoad.addPackage( package )
        '''

        # Nearest Neighbor sorting
        # Time Complexity: O(logN)
        sortedList = SimpleQueue()
        sortedList.push( packages[0] )
        packages.remove( packages[0] )
        for i in range( len( packages ) ):
            neighbor = self._getNearestPackage( sortedList.peek(), packages )
            sortedList.push( neighbor )
            index = packages.index( neighbor )
            packages.remove( packages[index] )

        while( sortedList.length() > 0 ):
            outputLoad.addPackage( sortedList.pop() )

        return outputLoad

    def _getNearestPackage( self, origin, group ):
        groupLocations = []
        for package in group:
            groupLocations.append( package.location )

        nearestLocation = self.graph.getNearestNeighbor( origin.location, groupLocations )

        for package in group:
            if package.location == nearestLocation:
                return package

    def _getDistanceBetweenPackages( self, origin, terminus ):
        # The graph distance functions use locations as arguments
        originLocation = origin
        nextLocation   = terminus

        distance = self.graph.getDistanceBetween( originLocation, nextLocation )

        return distance

    # The selection algorithm for packages uses a heuristic model
    # A queue is used to load highest priority first
    # The queue can be dumped if an extremely urgent package is found
    # Time Complexity: O(n) for each package and O(n*m) for nested heuristics
    def _assignPackage( self, truck ):
        allPackages = self.packages.getAll()
        priorityList = SimpleQueue()

        # Check if package needs a target truck
        for package in allPackages:
            if truck is not None:
                if truck.id == 2 and package.id in self.GROUP_ONE:
                    priorityList.push( package )
                    allPackages.remove( package )

        # Filter all packages for staged packages
        for package in allPackages:
            if package.status is Status.STAGED:
                # Check for packages with time sensitive requirements
                if self.currentTime >= self.DELAY_TIME:
                    if package.id in self.RUSH_PACKAGES:
                        priorityList.push( package )
                        allPackages.remove( package )
                    if package.id in self.DELAYED_PACKAGES:
                        priorityList.push( package )
                        #allPackages.remove( package )

                # Hotfix for incorrect postage
                if self.currentTime >= self.CORRECTION_TIME:
                    if package.id in self.INCORRECT_PACKAGES:
                        self._updatePackageNine()
                        priorityList.push( package )
                        allPackages.remove( package )

                # Push remaining packages if no heuristic is required
                if str( package.notes ) == '':
                    priorityList.push( package )
                    #allPackages.remove( package )

        # Pop items of the prioritized list until a suitable package returns
        # Time Complexity: O(n)
        for i in range( priorityList.length() ):
            selection = priorityList.peek()
            if selection.status is not Status.STAGED:
                priorityList.pop()
            elif selection.status:
                return selection

        # Return empty result
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

''' DEBUG CODE '''
# Nearest Neighbor Tests
'''
dispatch = DispatchService()
packages = dispatch.packages.getAll()
testPackage = packages[1]
packages.remove( testPackage )
result = dispatch._getNearestPackage( testPackage, packages )
print( str( testPackage.address ) + ' --> ' + str( result.address ) )
print( dispatch._getDistanceBetweenPackages( testPackage, result) )
'''
'''
dispatch = DispatchService()
unoptimized = dispatch.getLoad( 16 )
optimizedInput = copy.deepcopy( unoptimized )

print( unoptimized.charter.length() )
print( '-------- UNOPTIMIZED ---------')
for i in range( unoptimized.charter.length() ):
    print( unoptimized.charter.pop().address )

optimized = dispatch._optimizeLoad( optimizedInput )
print( '-------- OPTIMIZED ---------')
for i in range( optimized.charter.length() ):
    print( optimized.charter.pop().address )
'''

''' DEBUG CODE '''
'''
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