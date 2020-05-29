import csv
from hash import HashTable
from graph import Graph
from graph import Edge
from graph import Node
from logistics import Location

class Dispatcher( object ):
    def __init__( self ):
        self.locations = self._getLocations()
        self.graph = Graph()
        self._createGraph()
        self.packages = self._getPackages()

    def _createGraph( self ):

        # Add locations to graph as nodes
        self._addLocationsToGraph()

        # Add distances to graph as edges
        #self._addDistancesToGraph()

    def _getLocations( self ):
        table = HashTable(10)

        # Add locations to hash table
        with open( 'data/locations.csv' ) as file:
            locationData = csv.reader( file, delimiter=',' )
            # Iterate through locations
            # Time Complexity: O(n)
            for row in locationData:
                location = Location( row )
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
                        self.graph.addWeightedEdge(
                            self.locations.get( x ),
                            self.locations.get( y ),
                            float( weight )
                        )

    def _getPackages( self ):
        #FIXME: implement
        return HashTable( 10 )


dispatch = Dispatcher()
locations = dispatch._getLocations()
origin = locations.get( 0 )
terminus = locations.get( 1 )
graph = dispatch.graph
print( type( graph.nodes.get(26).location.id ) )

# newTable = HashTable(10)
# newLocation = Location( [11,'hobbokin', '4 E St'] )
# newTable.put( newLocation.id, newLocation )
# print( newTable.get( 11 ) )