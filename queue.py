# Queue class is a First In-First Out data structure

class SimpleQueue( object ):
    # The queue is a set of methods applied to a linked list
    def __init__( self ):
        self.list = []

    # Add value to end of queue: O(1)
    def push( self, item ):
        self.list.append( item )

    # Extract values from head of queue: O(1)
    def pop( self ):
        value = self.list[0]
        self.list.pop(0)
        return value

    # Identify value at head of queue: O(1)
    def peek( self ):
        result = False
        if( len( self.list ) > 0 ):
            result = self.list[0]
        return result

    def length( self ):
        return len( self.list )