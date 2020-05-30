# WGUPS Routing Application
# Kevin Fredericks 2020
# Student ID: 001227342

from logistics import Truck
from dispatcher import DispatchService

# Initialize time variables
SECONDS_PER_HOUR = 3600
startTime = 8 * SECONDS_PER_HOUR
currentTime = startTime

# Create dispatcher to control routing
dispatch = DispatchService()
graph = dispatch.graph

# Create two new trucks at the WGU address
HUB = dispatch.locations.get(0)
truck = Truck( 1, HUB )

# Load trucks with minimal load
load = dispatch.getLoad(10)
truck.assignLoad( load )
truck.setDestination( load.charter.peek() )

# Main Loop
while( True and currentTime < 16 * SECONDS_PER_HOUR):
    # Tick time forward by one second
    currentTime += 1

    # Register when a truck reaches a location
    if( truck.distanceToNextStop < 0.1 ):
        truck.setLocation( truck.destination )

    # Deliver package when at location and choose next destination
    if not( truck.location.id == truck.destination.id ):
        print( "Traveling to: " + str( truck.destination.address ) )
        truck.distanceToNextStop -= truck.velocity
    else:
        print( "Arrived at location: " + str( truck.location.name ) )
        # Deliver package at location
        # Direct truck to node of next package in load
        # Time Complexity: O(1)
        if( truck.load.getCount() > 0 ):
            truck.load.removePackage()

            nextPackage = truck.load.charter.peek()
            if( nextPackage ):
                # Next destination is the next package address
                nextAddress = nextPackage.address
                nextNode = graph.getNodeByAddress( nextAddress )
                nextLocation = nextNode.location
            else:
                # Destination changes to hub
                nextLocation = dispatch.locations.get( 0 )

            # Find distance to next package location
            truck.distanceToNextStop = graph.getDistanceBetween(
                truck.location,
                nextLocation
            )




