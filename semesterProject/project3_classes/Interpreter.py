from .Relation import Relation
from .Row import Row
from .Header import Header
from typing import Dict
from graph import Graph
from graphNode import GraphNode
from forest import Forest

class Interpreter:
    def __init__(self) -> None:
        self.output_str: str = ""
        self.database: Dict[str, Relation] = {}
        pass
    
    def run(self, datalog_program) -> str:
        self.datalog_program = datalog_program
        self.interpret_schemes()
        self.interpret_facts()
        self.interpret_rules()
        self.output_str += '\nQuery Evaluation\n' + self.interpret_queries()
        return self.output_str
    
    def interpret_schemes(self) -> None:
        # Start with an empty Database. 
        self.database: Dict[str, Relation] = {}
        schemesList = self.getSchemesFromDatalog()
        # For each scheme in the Datalog program, 
        #   add an empty Relation to the Database. 
        #   Use the scheme name as the name of the relation 
        #   and the attribute list from the scheme as the header of the relation.
        for scheme in schemesList:
            self.database[self.getName(scheme)] = Relation(self.getName(scheme), Header(self.getAttributeList(scheme)), set())
        pass

    def getName(self, scheme):
        startIndex = 0
        endIndex = scheme.find('(')
        return scheme[startIndex:endIndex]
    
    def getAttributeList(self, scheme):
        startIndex = scheme.find('(') + 1
        endIndex = scheme.find(')')
        return scheme[startIndex:endIndex].split(',')

    def getSchemesFromDatalog(self):
        startIndex = self.datalog_program.find('Schemes(') + 13
        endIndex = self.datalog_program.find('Facts(')
        datalogSchemes = self.datalog_program[startIndex:endIndex]
        while '\n' in datalogSchemes:
            datalogSchemes = datalogSchemes.replace('\n', '', 1)
        schemesList = datalogSchemes.split('  ')
        for i in range(len(schemesList)):
            schemesList[i] = schemesList[i].replace(' ', '', 1)
        return schemesList
    
    def interpret_facts(self) -> None:
        factList = self.getFactsFromDatalog()

        for fact in factList:
            that = self.database[self.getName(fact)]
            that.add_row(Row(self.getAttributeList(fact)))
        pass

    def getFactsFromDatalog(self):
        startIndex = self.datalog_program.find('Facts(') + 11
        endIndex = self.datalog_program.find('Rules(')
        datalogFacts = self.datalog_program[startIndex:endIndex]
        datalogFacts = datalogFacts.strip()
        while '\n' in datalogFacts:
            datalogFacts = datalogFacts.replace('\n', '', 1)
        datalogFacts = datalogFacts.split('  ')
        for i in range(len(datalogFacts)):
            datalogFacts[i] = datalogFacts[i].strip()
        return datalogFacts
    
    def interpret_queries(self) -> None:
        outputString = ""
        queriesList = self.getQueriesFromDatalog()

        for query in queriesList:
            resultingRelation = self.evaluate_predicate(self.getName(query), self.getAttributeList(query))
            outputString += f'{query} '
            # resultingRelation = self.evaluate_predicate(query)
            if len(resultingRelation.rows) > 0:
                outputString += f'Yes({len(resultingRelation.rows)})\n'
            else:
                outputString += f'No\n'
            
            if self.doesQueryHaveVariables(query):
                outputString += f'{str(resultingRelation)}'

        return outputString

    def doesQueryHaveVariables(self, query):
        queryParameters = self.getAttributeList(query)
        for i in queryParameters:
            if self.isParameterAConstant(i) == False:
                return True
        return False


    def getQueriesFromDatalog(self):
        startIndex = self.datalog_program.find('Queries(') + 13
        endIndex = self.datalog_program.find('Domain(')
        datalogQueries = self.datalog_program[startIndex:endIndex]
        while '\n' in datalogQueries:
            datalogQueries = datalogQueries.replace('\n', '', 1)
        datalogQueries = datalogQueries.strip()
        datalogQueries = datalogQueries.split('  ')
        for i in range(len(datalogQueries)):
            datalogQueries[i] = datalogQueries[i].strip()
        return datalogQueries
    
    def evaluate_predicate(self, predicate, queryParameters) -> Relation:
        tableRelation = self.getDBTable(predicate)

        relationsOfAllQueries = self.getRelationsOfAllQueries(queryParameters, tableRelation)
        variableColumns = relationsOfAllQueries[1]
        relationsOfAllQueries = relationsOfAllQueries[0]

        returnRelation = self.getRelationWithMatchingRows(relationsOfAllQueries, tableRelation)
        
        if len(variableColumns) > 0:
            returnRelation = returnRelation.project(self.getVariableColumns(variableColumns), queryParameters)

        returnRelation.rename(returnRelation.header)
        
        return returnRelation
    
    def getVariableColumns(self, variableColumns):
        allColumns = []
        for key in variableColumns:
            allColumns += variableColumns[key]
        return allColumns
    
    def getRelationWithMatchingRows(self, relationsOfAllQueries, tableRelation):
        for queryRelation in relationsOfAllQueries:
            tableRelation = tableRelation.reduceToOnlyMatchingRows(queryRelation)
        return tableRelation

    def getDBTable(self, predicate):
        return self.database[predicate]
    
    def getRelationsOfAllQueries(self, queryParameters, relation):
        allResultingRelations = []
        variables = {}
        column = 0
        for parameter in queryParameters:
            if self.isParameterAConstant(parameter):
                resultingRelation = relation.select1(parameter, column)
                if resultingRelation != None:
                    allResultingRelations.append(resultingRelation)
                else:
                    relation = Relation('EmptyRelation', relation.header, set())
                    return relation
            else:
                if parameter in variables:
                    variables[parameter].append(column)
                    resultingRelation = relation.selectWithVariable(variables, parameter)
                else:
                    variables[parameter] = [column]
                    resultingRelation = relation.selectWithVariable(variables, parameter)
                if resultingRelation != None:
                    allResultingRelations.append(resultingRelation)
                else:
                    relation = Relation('EmptyRelation', relation.header, set())
                    return relation
            column += 1

        return [allResultingRelations, variables]
    
    def selectParametersFromRelation(self, relation, queryParameters):
        variables = {}
        matches = Relation('Result', )
        # for every param
        for index in range(len(queryParameters)):
            # initialize a list in the matches dictionary with the index as the key
            # get gurrent parameter
            parameter = queryParameters[index]
            if self.isParameterAConstant(parameter):
                # if parameter is a constant
                # for every row of this relation
                for row in relation.rows:
                    # if the parameter is in the relation's row at the correct position
                    if parameter == row[index]:
                        # add it to the matches
                        matches.rows.add(row)
            
            else:
                # if the parameter is a variable
                for row in relation.rows:
                    if parameter in variables:
                        # if the variable already exists
                        # if the variable has been used, the variable needs to be the same as the one already used
                        if variables[parameter] == row[index]:
                            # if its a match, add it to matches
                            matches.rows.add(row)

                    else:
                        # if the variable has not been used, add it to the variables
                        variables[parameter] = {'value': row.values[index], 'index': index}
                        # add it to matches
                        matches.rows.add(row)
        return matches


    def isParameterAConstant(self, parameter):
        return parameter.startswith("'") and parameter.endswith("'")

    def getRulesFromDatalog(self):
        startIndex = self.datalog_program.find('Rules(') + 11
        endIndex = self.datalog_program.find('Queries(')
        datalogRules = self.datalog_program[startIndex:endIndex]
        datalogRules = datalogRules.strip()
        while '\n' in datalogRules:
            datalogRules = datalogRules.replace('\n', '', 1)
        datalogRules = datalogRules.split('  ')
        for i in range(len(datalogRules)):
            datalogRules[i] = datalogRules[i].strip()
        return datalogRules
    
    def interpret_rules(self) -> None:
        self.output_str += 'Dependency Graph\n'
        # fixed point algorithm to evaluate rules goes here:
        rulesList = self.getRulesFromDatalog()

        graph = self.createGraph(rulesList)
        self.output_str += graph.printDependencyGraph() + '\n'

        postOrder = self.dfsPostOrderOnReverseGraph(graph)
        postOrder.reverse()
        forest = self.dfsForForest(postOrder, graph)
        SCCs = self.forestToSCC(forest)

        self.output_str += 'Rule Evaluation\n'
        numOfPasses = 0
        for SCC in SCCs:
            numOfPasses = 0
            addedTuples = True
            self.printSCCName(SCC)
            sccList = list(SCC)

            while addedTuples:
                if (len(SCC) == 1) and self.doesNodePointToSelf(sccList[0]):
                    # trivial
                    self.evaluate_rule(sccList[0].rule)
                    numOfPasses += 1
                    addedTuples = False
                else:
                    addedTuples = False
                    for rule in sorted(SCC, key=lambda x: int(x.name[1:])):
                        if self.evaluate_rule(rule.rule) != 0:
                            addedTuples = True
                    numOfPasses += 1

                        

                        
            self.output_str += str(numOfPasses) + ' passes: '
            self.printSCCNameWithoutSCC(SCC)

    def doesNodePointToSelf(self, rule):
        for r in rule.pointsTo:
            if r.name == rule.name:
                return False
        
        return True

    def printSCCNameWithoutSCC(self, SCC):
        SCC = list(SCC)
        SCC.sort(key=lambda x: x.name[1:])
        sepChar = ''
        for component in SCC:
            self.output_str += sepChar + component.name
            sepChar=','
        
        self.output_str += '\n'

    def printSCCName(self, SCC):
        SCC = list(SCC)
        SCC.sort(key=lambda x: x.name[1:])
        sepChar = ''
        self.output_str += 'SCC: '
        for component in SCC:
            self.output_str += sepChar + component.name
            sepChar=','
        
        self.output_str += '\n'

            

        # numOfPasses = 0
        # noChange = False
        # while not noChange:
        #     noChange = True
        #     numOfPasses += 1
        #     for rule in rulesList:
        #         if self.evaluate_rule(rule) != 0:
        #             noChange = False

        # self.output_str += '\nSchemes populated after ' + str(numOfPasses) + ' passes through the Rules.\n\nQuery Evaluation\n'

    def forestToSCC(self, forest):
        SCCs = []
        for node in forest:
            SCCs.append(self.nodeToSCC(node))

        return SCCs
            
    def nodeToSCC(self, node):
        SCC = set()
        SCC.add(node)
        for node in node.SCCPointsTo:
            test = self.nodeToSCC(node)
            SCC.update(test)
        return SCC


    def dfsForForest(self, postOrder, graph):
        if len(postOrder) == 0:
            return graph.allNodes
        visited = set()
        stack = []
        forest = []
        adjacencyList = graph.getAdjacencyList()

        currNode = postOrder.pop(0)
        stack.append(currNode)
        visited.add(stack[-1])
        forest.append(stack[-1])

        while len(graph.allNodes) > len(visited):
            nextNode = self.getLowestNotVisitedNode(adjacencyList[currNode.name], graph, visited)
            if nextNode == 0:
                stack.pop()
                if len(stack) == 0:
                    currNode = postOrder.pop(0)
                    stack.append(currNode)
                    visited.add(stack[-1])
                    forest.append(stack[-1])
                else:
                    currNode = stack[-1]
            else:
                currNode.addSCCPointsTo(nextNode)
                stack.append(nextNode)
                visited.add(stack[-1])
                currNode = stack[-1]

        return forest

    def dfsPostOrderOnReverseGraph(self, graph):
        visited = set()
        postOrder = []
        stack = []
        forest = []
        reverseAdjacencyList = graph.getReverseAdjacencyList()

        currNode = graph.getNode('R0')
        stack.append(currNode)
        visited.add(stack[-1])
        forest.append(stack[-1])

        while len(stack) > 0:
            nextNode = self.getLowestNotVisitedNode(reverseAdjacencyList[currNode.name], graph, visited)
            if nextNode == 0:
                postOrder.append(stack.pop())
                if len(stack) == 0:
                    nextLowestNodeInGraph = self.getLowestNotVisitedNodeInGraph(graph, visited)
                    if nextLowestNodeInGraph == 0:
                        return postOrder
                    else:
                        stack.append(nextLowestNodeInGraph)
                        visited.add(stack[-1])
                        forest.append(stack[-1])
                else:
                    currNode = stack[-1]
            else:
                currNode.addReverseForestPointsTo(nextNode)
                stack.append(nextNode)
                visited.add(stack[-1])
                currNode = stack[-1]
        
        return postOrder

    def getLowestNotVisitedNodeInGraph(self, graph, visited):
        notVisitedNodes = []

        for node in graph.allNodes:
            if node not in visited:
                notVisitedNodes.append(node)
        
        if len(notVisitedNodes) == 0:
            return 0

        lowNum = float('inf')

        for node in notVisitedNodes:
            if int(node.name[1:]) < lowNum:
                lowNum = int(node.name[1:])

        return graph.getNode('R' + str(lowNum))




    def getLowestNotVisitedNode(self, setOfNodes, graph, visited):
        lowNum = float('inf')

        for node in setOfNodes:
            if int(node.name[1:]) < lowNum:
                if graph.getNode('R' + str(node.name[1:])) not in visited:
                    lowNum = int(node.name[1:])

        if lowNum == float('inf'):
            return 0
        else:
            return graph.getNode('R' + str(lowNum))
            
    def createGraph(self, rulesList):
        ruleNum = 0
        graph = Graph()

        for rule in rulesList:
            ruleParts = self.splitRule(rule)
            graph.addNode(GraphNode('R' + str(ruleNum), rule, ruleParts['leftSide'], ruleParts['rightSide']))
            ruleNum+=1

        for node in graph.allNodes:
            for name in node.getRightSidePredicates():
                for nodeTwo in graph.allNodes:
                    if nodeTwo.getLeftSideName() == name:
                        node.addForwardArrow(nodeTwo)

        return graph

            


    def splitRule(self, rule):
        rule = rule[0:len(rule)-1]
        arrow = rule.find(':-')
        rule = {
            'leftSide': rule[0:arrow].strip(),
            'rightSide': rule[arrow+2:].strip()
        }

        rule['rightSide'] = rule['rightSide'].split('),')

        for item in range(len(rule['rightSide'])-1):
            rule['rightSide'][item] = rule['rightSide'][item] + ')'
        
        return rule
    
    # this function should return the number of unique tuples added to the database
    def evaluate_rule(self, rule) -> int:
        self.output_str += rule
        # Step 1:
        
        # Evaluate the predicates on the right-hand side of the rule (the body predicates):
        rule = self.splitRule(rule)

        # For each predicate on the right-hand side of a rule, 
        #   evaluate the predicate in the same way you evaluated the queries in the last project (using select, project, and rename operations). 
        #   Each predicate should produce a single relation as an intermediate result. 
        #   If there are n predicates on the right-hand side of a rule, 
        #   there should be n intermediate results.
        intermediateRelations = []
        for predicate in rule['rightSide']:
            intermediateRelations.append(self.evaluate_predicate(self.getName(predicate), self.getAttributeList(predicate)))       
        # HINT: 
        #   if you used the EvaluatePredicate function as suggested in lab 3
        #   you should only need to call that function once per 
        #   body predicate and store the result
   
        # Example:
        # for body_predicate in rule.body:
        # result = self.evaluate_predicate(body_predicate))

        # Step 2:
        # Join the relations that result:

        # If there are two or more predicates on the right-hand side of a rule, 
        #   join the intermediate results to form the single result for Step 2. 
        #   Thus, if p1, p2, and p3 are the intermediate results from Step 1, join them 
        #   (p1 |x| p2 |x| p3) into a single relation.

        # If there is a single predicate on the right hand side of the rule, 
        # use the single intermediate result from Step 1 as the result for Step 2.
        
        if len(intermediateRelations) > 1:
            resultingRelation = intermediateRelations[0]
            for relation in range(1, len(intermediateRelations)):
                resultingRelation = resultingRelation.natural_join(intermediateRelations[relation]) 
        else:
            resultingRelation = intermediateRelations[0]

        # Step 3:
        # Project the columns that appear in the head predicate:

        # The predicates in the body of a rule may have variables 
        #   that are not used in the head of the rule. 
        #   The variables in the head may also appear in a different order 
        #   than those in the body. Use a project operation on the result from 
        #   Step 2 to remove the columns that don't appear in the head of the 
        #   rule and to reorder the columns to match the order in the head.
        projectedRelation = self.projectRules(rule['leftSide'], resultingRelation)

        # Step 4:
        # Rename the relation to make it union-compatible:
        
        # Rename the relation that results from Step 3 to 
        #   make it union compatible with the relation that 
        #   matches the head of the rule. Rename each attribute 
        #   in the result from Step 3 to the attribute name found 
        #   in the corresponding position in the relation 
        #   that matches the head of the rule.
        valuesOfDBTable = self.database[self.getTableName(rule['leftSide'])].header.values
        projectedRelation.header.values = valuesOfDBTable

        # Step 5:
        # Union with the relation in the database:

        # Save the size of the database relation before calling union
        size_before = len(self.database[self.getTableName(rule['leftSide'])].rows)
        
        # Union the result from Step 4 with the relation 
        # in the database whose name matches the name of the head of the rule.
        printRows = []

        for row in projectedRelation.rows:
            s1 = len(self.database[self.getTableName(rule['leftSide'])].rows)
            self.database[self.getTableName(rule['leftSide'])].add_row(row)
            s2 = len(self.database[self.getTableName(rule['leftSide'])].rows)
            if s2 > s1:
                printRows.append(row)
        
        # Save the size of the database relation after calling union
        size_after = len(self.database[self.getTableName(rule['leftSide'])].rows)
        
        if (size_after - size_before) != 0:
            newRelation = Relation('copy', Header(projectedRelation.header.values), set())
            for row in projectedRelation.rows:
                if row in printRows:
                    newRelation.add_row(row)
            self.output_str += '\n' + str(newRelation)
        else:
            self.output_str += '\n'

        return size_after - size_before
    
    def getTableName(self, headRule):
        leftParen = headRule.find('(')
        return headRule[:leftParen]

    
    def projectRules(self, headPredicate, intermediateRelationsResult):
        headPredicateColNames = self.getHeadPredicateCols(headPredicate)
        interRelationColNames = intermediateRelationsResult.header.values

        sharedColumns = []
        for header in headPredicateColNames:
            if header in interRelationColNames:
                sharedColumns.append(interRelationColNames.index(header))

        # for header in interRelationColNames:
        #     if header in headPredicateColNames:
        #         sharedColumns.append(interRelationColNames.index(header))

        returnRelation = Relation('projectedRelation', Header(headPredicateColNames), set())

        for row in intermediateRelationsResult.rows:
            rowValues = []
            for sharedCol in sharedColumns:
                rowValues.append(row.values[sharedCol])
            returnRelation.add_row(Row(rowValues))
            
        return returnRelation


    def getHeadPredicateCols(self, headPredicate):
        leftParen = headPredicate.find('(')
        rightParen = headPredicate.find(')')

        columnNames =  headPredicate[leftParen+1:rightParen].split(',')

        return columnNames