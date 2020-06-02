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
truck = Truck( 1, HUB )

# Load trucks with minimal load
load = dispatch.getLoad(10, 1)
truck.assignLoad( load )
firstAddress = truck.load.charter.peek().address
firstLocation = dispatch.getLocationByAddress( firstAddress )
truck.setDestination( firstLocation )
# Calculate distance to next package location
truck.distanceToNextStop = graph.getDistanceBetween(
    truck.location,
    firstLocation
)

# Main Loop
while( True and dispatch.currentTime < 28810 ):
    #time.sleep( 0.5 )

    # Tick time forward by one second
    print( 'CURRENT TIME: ' + str( currentTime ) )
    dispatch.currentTime += 1

    # Register when a truck reaches a location
    truck.distanceToNextStop -= truck.velocity
    print( 'Distance to next stop: ' + str( truck.distanceToNextStop ) )
    if( truck.distanceToNextStop <= 0 ):
        truck.location = truck.destination

    # Deliver package when at location and choose next destination
    print( "Current: " + str( truck.location.name ) )
    if not( truck.location.id == truck.destination.id ):
        print( "Traveling to: " + str( truck.destination.name ) )
    else:
        print( "Arrived at location: " + str( truck.location.name ) )
        # Deliver package at location
        # Direct truck to node of next package in load
        # Time Complexity: O(1)
        if( truck.load.getCount() > 0 ):
            # Change package status to next state in dispatch service
            dispatch.advancePackageStatus( truck.load.charter.peek() )

            # Remove package from load
            truck.load.removePackage()

            nextPackage = truck.load.charter.peek()
            if( nextPackage ):
                print( 'Changing destination to ' + str( nextPackage.address ) )
                # Next destination is the next package address
                nextLocation = dispatch.getLocationByAddress( nextPackage.address )
            else:
                # Destination changes to hub
                nextLocation = dispatch.locations.get( 0 )

            # Set new destination
            truck.setDestination( nextLocation )

            # Find distance to next package location
            truck.distanceToNextStop = graph.getDistanceBetween(
                truck.location,
                nextLocation
            )




