import csv

class DistanceGraph:
    def __init__(self):
        self.csvLocation = ''
        self.graph = self._createGraph()

    def getGraph(self):
        #Convert available data
        csvTable = open( self.csvLocation )
        distances = self._csvToList( csvTable )

        #Graph is a dictionary of dictionaries
        entry = { 'Zed': { 'a': 1, 'b': 2, 'c': 3 } }
        self.graph.update( entry )
        for row in distances:
            #Index 1 provides a concise address
            currentAddress = row[1]
            entry = { currentAddress: 'null' }
            self.graph.update( entry )

    def setLocation(self, csvLocation):
        self.csvLocation = csvLocation

    def _csvToList(self, csvObject):
        # Convert data to list structure
        with csvObject as file:
            reader = csv.reader(file, delimiter=',')
            result = list(reader)

        return result

newTable = distanceTable()
newTable.setLocation('data/WGUPS Distance Table.csv')
newTable.getGraph()

graph = newTable.graph

for item in graph:
    print( item + '\n')