# hermes
A logistics simulation app for the WGU Computer Science program

## Dependencies
Python 3.x

## Installation
- OSX, Windows, Linux - Navigate to the installation directory and type `python3 main.py`

## Notes
This app is intended to combine both prescriptive and generalized solutions for
a logistics simulation. The following algorithms are applied to the problem:
1. Nearest-NeighborCalculation
• Loads are sorted according to the distance between each package's address and the previously visited package with the group. This creates a predictable routing pattern which allows redundant crossings while preventing the most substantial cases of unnecessary travel.
• The Nearest-Neighbor algorithm is also easy to adjust because it identifies an initial origin point manually. For the purposes of this application this is very convenient for purposes of prioritizing urgent packages to the front of the algorithm selecion
2. MinimumandMaximumLoadSizes
• The load will be limited to a maximum number of packages before the next package is loaded in to a truck. Minimum load sizes minimize the need for trucks to return to the hub. Maximum load sizes ensure that packages are delivered on-time.
3. WeightedGraphNearestNeighbor
• Addresses are nodes and distances between address are edges. There is no consideration of 'more difficult' paths.
4. LoadOptimization
• Heuristics are provided for the special instructions and package deadlines provided
 
by some packages. This process ensures priority packages are loaded first
The defining feature of the algorithm used is that routing is determined in one step when a load is constructed by the dispatch.

