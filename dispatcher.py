import csv
from hash import HashTable
from graph import Graph
from graph import Edge
from graph import Node
from logistics import Location
from logistics import Package
from logistics import Load
from queue import SimpleQueue

class DispatchService( object ):
    def __init__( self ):
        self.locations = self._getLocations()
        self.graph = Graph()
        self._createGraph()
        self.packages = self._getPackages()

    def getLoad( self, size ):
        # Push packages to new load queue based on size
        # Time Complexity: O(n)
        load = Load()
        while ( load.getCount() < size and self.packages.length() > 0 ):
            # Naive method for loading packages
            load.addPackage( self.packages.pop() )

        return load

    def _createGraph( self ):

        # Add locations to graph as nodes
        self._addLocationsToGraph()

        # Add distances to graph as edges
        self._addDistancesToGraph()

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
        for i in range( self.locations.length ):
            # Directly access each bucket for iteration
            bucket = self.locations._table[i]
            for value in bucket:
                self.graph.addNode( value[1] )

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

    def _getPackages( self ):
        packages = SimpleQueue()
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
                )
                packages.push( package )
        return packages