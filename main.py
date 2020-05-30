# WGUPS Routing Application
# Kevin Fredericks 2020

from logistics import Truck
from dispatcher import DispatchService

# Initialize time variables
SECONDS_PER_HOUR = 3600
startTime = 8 * SECONDS_PER_HOUR
currentTime = startTime

# Create dispatcher to control routing
dispatch = DispatchService()

# Create two new trucks at the WGU address
HUB = dispatch.locations.get(0)
truck = Truck( 1, 1200, HUB )

# Load trucks with minimal load
load = dispatch.getLoad(10)
truck.assignLoad( load )

# Main Loop
while( True and currentTime < 16 * SECONDS_PER_HOUR):
    # Move truck toward location of next package if not at location
    destination = truck.load.charter.peek().address
    graph = dispatch.graph
    currentTime += 1
    if( truck.location.address is not destination ):

        print( "Traveling to destination" )
    else:





