
class GraphNode:
    def __init__(self, name, rule, leftSide, rightSide) -> None:
        self.name = name
        self.rule = rule
        self.leftSide = leftSide
        self.rightSide = rightSide
        self.pointsTo = set()
        self.pointedAtBy = set()
        self.reverseForestPointsTo = set()
        self.reverseForestpointedAtBy = set()
        self.SCCPointsTo = set()
        self.SCCPointedAtBy = set()

    def addSCCPointsTo(self, toNode):
        toNode.SCCPointedAtBy.add(self)
        self.SCCPointsTo.add(toNode)

    def addReverseForestPointsTo(self, toNode):
        toNode.reverseForestpointedAtBy.add(self)
        self.reverseForestPointsTo.add(toNode)

    def addForwardArrow(self, toNode):
        toNode.pointedAtBy.add(self)
        self.pointsTo.add(toNode)

    def addBackwardArrow(self, fromNode):
        fromNode.pointsTo.add(self)
        self.pointedAtBy.add(fromNode)

    def getRightSidePredicates(self):
        listOfPredicateNames = []
        for predicate in self.rightSide:
            listOfPredicateNames.append(predicate[0:predicate.find('(')])
        
        return listOfPredicateNames
    
    def getLeftSideName(self):
        return self.leftSide[0:self.leftSide.find('(')]
