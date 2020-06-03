# WGUPS Routing Application
# Kevin Fredericks 2020
# Student ID: 001227342

from logistics import Truck
from dispatchService import DispatchService

# Create dispatcher to control routing
dispatch = DispatchService()
graph = dispatch.graph

# Create two new trucks at the WGU address
HUB = dispatch.locations.get(0)
truckOne = Truck( 1, HUB, graph )
truckTwo = Truck( 2, HUB, graph )

# Create a fleet with the available trucks
fleet = [ truckOne, truckTwo ]

# Assign initial loads
# Time Complexity: O(n)
for truck in fleet:
    if truck.location == truck.hub:
        truck.assignLoad( dispatch.getLoad( 16, truck ) )
        truck.setDestination( truck.load.charter.pop().location )


# Main Loop
while( True and dispatch.isActive() == True ):

    # Update dispatch service
    # Advances time forward and checks for docked trucks
    dispatch.update( fleet )

    # Moves truck forward and checks for delivery state
    for truck in fleet:
        truck.update()

    # Log status of trucks
    time = dispatch.currentTime
    hour = int( time / dispatch.SECONDS_PER_HOUR )
    minute = int( time / 60 )
    formattedTime =  str( hour ) + ':' + str( minute )
    for truck in fleet:
        if truck.delivering:
            print( formattedTime )
            print( 'Truck ' + str(truck.id) + ': ' + str(truck.location.address) )
            print( 'Packages on truck: ' + str( truck.load.charter.length() ) )

            print( '------- Current status ------')
            print( 'Total Distance: ' + str( truckOne.totalDistance + truckTwo.totalDistance ) )
            for package in dispatch.packages.getAll():
                print( package.status )
