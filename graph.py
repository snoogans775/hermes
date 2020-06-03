from hash import HashTable

#Directional weighted graph
class Graph( object ):
    def __init__( self ):
        self.nodes = HashTable( 10 )

    # Add a vertex to the graph
    # Time Complexity: O(n)
    def addNode( self, location):
        self.nodes.put( int( location.id ), Node( location ) )

    # Add edge between two nodes bidirectionally
    # Time Complexity: O(n)
    def addWeightedEdge( self, origin, terminus, weight ):
        originEdge = Edge( origin, weight )
        terminusEdge = Edge( terminus, weight )
        self.nodes.get( origin.id ).addEdge( terminusEdge )
        self.nodes.get( terminus.id ).addEdge( originEdge )

    # Get id of a vertex at a location
    # Time Complexity: O(n)
    def getNode( self, location ):
        return self.nodes.get( location.id )

    # Get first node returned by location name: O(n)
    def getNodeByAddress( self, address ):
        for node in self.nodes.getAll():
            if( node.location.address == address ):
                return node

    # Get distance between two points
    def getDistanceBetween( self, origin, terminus ):
        return self.nodes.get( origin.id ).getDistance( terminus )

    # Get nearest neighbor of node: O(n * m) n = buckets, m = bucket items
    def getNearestNeighbor( self, node ):
        edges = node.edges.getAll()
        # Find smallest distance to node in list
        nearestNeighbor = edges[0].weight
        minDistance = 100
        for edge in edges:
            distance = edge.weight
            if distance < minDistance:
                minDistance = edge.weight
                nearestNeighbor = edge.location

        return nearestNeighbor

class Node( object ):
    def __init__( self, location ):
        self.edges = HashTable(10)
        self.location = location

    #Time Complexity: O(n) where n is the number of edges
    def addEdge( self, edge ):
        self.edges.put( int( edge.id ), edge )

    #Time Complexity: O(n) where n is the number of edges
    def findEdge( self, id ):
        return self.edges.get( id )

    #Time Complexity: O(n) where n is the number of edges
    def getDistance( self, location ):
        return self.edges.get( location.id ).weight

class Edge( object ):
    def __init__( self, location, weight = 0 ):
        self.id = int( location.id )
        self.location = location
        self.weight = weight