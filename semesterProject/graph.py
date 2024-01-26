
class Graph:
    def __init__(self) -> None:
        self.allNodes = []

    def addNode(self, node):
        self.allNodes.append(node)

    def getNode(self, nodeName):
        for node in self.allNodes:
            if node.name == nodeName:
                return node

    def getAdjacencyList(self):
        adjacencyList = dict()

        for node in self.allNodes:
            adjacencyList[node.name] = node.pointsTo

        return adjacencyList
    
    def getReverseAdjacencyList(self):
        reverseAdjacencyList = dict()

        for node in self.allNodes:
            reverseAdjacencyList[node.name] = node.pointedAtBy

        return reverseAdjacencyList
    
    def printDependencyGraph(self):
        string = ''
        for node in self.allNodes:
            sepChar = ''
            string += node.name + ':'
            pointsToList = list(node.pointsTo)
            pointsToList.sort(key=lambda x: x.name[1:])
            for nodetwo in pointsToList:
                string += sepChar + nodetwo.name
                sepChar = ','
            string += '\n'
        
        return string
