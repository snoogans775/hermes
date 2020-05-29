class HashTable( object ):
    #The hash table constructs with an immutable length
    def __init__( self, size = 10):
        self._table = self._createTable( size )
        self.length = size

    #Chained hash table stores multiple entries at an index
    #Time complexity: O(n)
    def put( self, key, value ):
        hashedKey = hash ( key )
        bucket = self._findBucket( hashedKey )
        depth = self._findKeyValuePair( hashedKey, bucket )

        #Add key-value pair to next available link
        if len( depth ) == 0:
            bucket.append( [hashedKey, value] )
        else:
            depth[1] = value
        return True

    #Hash a key and extract correct bucket
    #Time complexity: O(n) where n is the length of the bucket
    def get( self, key ):
        hashedKey = hash( key )
        bucket = self._findBucket( hashedKey )

        #Compare search id to keys
        keyValuePair = self._findKeyValuePair( hashedKey, bucket )

        if keyValuePair:
            return keyValuePair[1]

        raise Exception('requested key-value pair not found')

    #Remove a key from the hash table
    # Time complexity: O(n)
    def remove( self, key, value ):
        hashedKey = hash( key )
        bucket = self._findBucket( hashedKey )

        #Remove delivery if exists at hashIndex
        #Time Complexity: O(n)
        for entry in bucket:
            if entry[1] == value:
                bucket.remove( entry )
                break

    # Directly return values of a bucket
    def getBucket( self, index ):
        return self._table[index]

    #Method to initialize structure of the hash table
    # Time complexity: O(n)
    def _createTable( self, size ):
        emptyTable = []
        for i in range( size ):
            emptyTable.append([])

        return emptyTable

    def _findBucket( self, key ):
        return self._table[key % len(self._table)]

    #Loop through a bucket to find the requested key
    #Time complexity: O(n)
    def _findKeyValuePair( self, key, bucket ):
        for keyValuePair in bucket:
            if keyValuePair[0] == key:
                return keyValuePair
        return []