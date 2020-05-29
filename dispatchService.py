import csv
from hash import HashTable
from graph import Graph
from logistics import Location

class Dispatcher( object ):
    def __init__( self ):
        self.locations = self._getLocations()
        self.graph = self._createGraph()
        self.packages = self._getPackages()

    def _createGraph( self ):
        graph = Graph()

        # Add locations to graph as vertices
        # Time Complexity: O(n)
        locations = self._getLocations()
        for i in range( locations.length ):
            # Directly access each bucket for iteration
            bucket = locations._table[i]
            for value in bucket:
                graph.addNode( value[1] )

        # Add distances to graph as edges
        with open( 'data/distanceTable.csv' ) as file:
            distanceData = csv.reader( file, delimiter=',' )

            # Iterate through distance columns and rows
            # Enumerate is alternative to row and column indexes
            # Time Complexity: O(n^2)
            for x, row in enumerate( distanceData ):
                for y, weight in enumerate( row ):
                    if not weight == '':
                        graph.addWeightedEdge(
                            locations.get( x ),
                            locations.get( y ),
                            float( weight )
                        )

        return graph

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

    def _getPackages( self ):
        #FIXME: implement
        return HashTable( 10 )


dispatch = Dispatcher()
locations = dispatch._getLocations()
print( dispatch.graph.getNode( locations.get( 0 ) ).location.name )

# newTable = HashTable(10)
# newLocation = Location( [11,'hobbokin', '4 E St'] )
# newTable.put( newLocation.id, newLocation )
# print( newTable.get( 11 ) )