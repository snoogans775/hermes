from logistics import Package

class HashTable( object ):
    #Chaining hash table
    #The hash table constructs with an immutable length
    def __init__( self, length = 10):
        self._table = self._createTable( length )

    #Insert a delivery by id
    #Chained hash table stores multiple entries at an index
    #Time complexity: O(n) where n is the length of the bucket
    def put( self, key, value ):
        hashedKey = hash ( key )
        bucket = self._findBucket( hashedKey )

        depth = self._findKeyValuePair( hashedKey, bucket )

        #Add key value pair to next available link
        if len( depth ) == 0:
            bucket.append( [hashed_key, value] )
        else:
            depth[1] = value

        return True

    #Hash a key and extract correct bucket
    #Time complexity: O(n) where n is the length of the bucket
    def get( self, key ):
        hashedKey = hash( key )
        bucket = self._findBucket( hashedKey )

        #Compare search id to deliveries at hashIndex
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
            if entry.value == value:
                bucket.remove( entry )
                break

    #Method to initialize structure of the hash table
    # Time complexity: O(n)
    def _createTable( self, length ):
        emptyTable = [False] * length

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

newTable = HashTable(10)
newPackage = Package(
    2,
    '5 W St',
    '12:05pm',
    'SLC',
    89504,
    5.6,
    'pending'
)
newTable.put( newPackage.id, newPackage )

print( len(table.table) )
