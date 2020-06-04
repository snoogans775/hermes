# WGUPS Routing Application
# Kevin Fredericks 2020
# Student ID: 001227342

from logistics import Truck
from dispatchService import DispatchService
from logistics import Load

# Create dispatcher to control routing
dispatch = DispatchService()
graph = dispatch.graph

# Create two new trucks at the WGU address
HUB = dispatch.locations.get(0)
truckOne = Truck( 1, HUB, graph )
truckTwo = Truck( 2, HUB, graph )

# Create a fleet with the available trucks
fleet = [ truckOne, truckTwo ]

'''
# Assign initial loads
# Time Complexity: O(n)
for truck in fleet:
    if truck.location == truck.hub:
        truck.assignLoad( dispatch.getLoad( 16, truck ) )
        truck.setDestination( truck.load.charter.pop().location )
'''

# Main Loop
while( dispatch.isActive() is True and dispatch.currentTime < 16 * dispatch.SECONDS_PER_HOUR ):

    # Update dispatch service
    # Advances time forward and checks for docked trucks
    dispatch.update( fleet )

    # Moves truck forward and checks for delivery state
    for truck in fleet:
        truck.update()
        if truck.loading:
            truck.assignLoad( dispatch.getLoad( truck ) )

    # Log status of trucks
    time          = dispatch.currentTime
    hour          = int( time / dispatch.SECONDS_PER_HOUR )
    minute        = int( time % 60 )
    formattedTime = str( hour ) + ':' + str( minute )

    for truck in fleet:
        if truck.delivering:
            print( formattedTime )
            print( 'Truck ' + str(truck.id) + ': ' + str(truck.location.address) )
            print( 'Packages on truck: ' + str( truck.load.charter.length() ) )
            for p in dispatch.packages.getAll():
                print( str( p.id ) + ': ' + str( p.status ) + ' @ ' + str( p.deliveredAt ) )

            #print( '------- Current status ------')
            #print( 'Total Distance: ' + str( truckOne.totalDistance + truckTwo.totalDistance ) )

print( '--------- End State -----------')
for p in dispatch.packages.getAll():
    print( str( p.id ) + ': ' + str( p.status ) + ' @ ' + str( p.deliveredAt ) )
for truck in fleet:
    print( 'Truck ' + str( truck.id ) + ': ' + str( truck.location.address ) )
    print( 'Total Distance: ' + str( truck.totalDistance ) )

print( str( dispatch.packages.get( 6 ).inTransitAt )  )
print( '-------- LOGS ----------')
for log in dispatch.log:
    print( '------ LOAD --------')
    print( log.charter.length() )
