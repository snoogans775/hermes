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
truckTwo = Truck(2, HUB )

# Load trucks with minimal load
load = dispatch.getLoad(10, truck)
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

    # Update dispatch service
    # Advances time forward and checks for docked trucks
    dispatch.update()

    # Moves truck forward and checks for delivery state
    truck.update()

    # Register when a truck reaches a location
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
            # Check next package
            nextPackage = truck.load.charter.peek()
            # Remove package from load and report as delivered
            truck.load.removePackage()
            dispatch.deliverPackage( nextPackage )

            # Select next destination
            # Time Complexity: O(n)
            # Check if another package exists in load
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




