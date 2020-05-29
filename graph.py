from hash import HashTable

#Bidirectional weighted graph
class Graph( object ):
    def __init__( self ):
        self.nodes = HashTable( 50 )

    # Add a vertex to the graph
    # Time Complexity: O(n)
    def addNode( self, location):
        self.nodes.put( location.id, Node( location ) )

    # Add edge between two nodes
    # Time Complexity: O(n)
    def addWeightedEdge( self, origin, terminus, weight ):
        originEdge = Edge( origin, weight )
        terminusEdge = Edge( terminus, weight )
        self.nodes.get( origin.id ).addEdge( originEdge )
        self.nodes.get( terminus.id ).addEdge( terminusEdge )

    # Get id of a vertex at a location
    # Time Complexity: O(n)
    def getNode( self, location ):
        return self.nodes.get( location.id )

    # Get distance between two points
    def getDistanceBetween( self, origin, terminus ):
        return self.nodes.get( origin.id ).getDistance( terminus )

    #FIXME: Find distance between non-adjacent points

class Node( object ):
    def __init__( self, location ):
        self.edges = HashTable()
        self.location = location

    #Time Complexity: O(n) where n is the number of edges
    def addEdge( self, edge ):
        self.edges.put( edge.id, edge )

    #Time Complexity: O(n) where n is the number of edge
    def findEdge( self, id ):
        return self.edges.get( id )

    #Time Complexity: O(n) where n is the number of edge
    def getDistance( self, location ):
        return self.edges.get( location.id ).weight


class Edge( object ):
    def __init__( self, location, weight = 0 ):
        self.location = location
        self.id = location.id
        self.weight = weight