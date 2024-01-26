from project1_classes.token import Token
from project2_classes.predicate import Predicate
from project2_classes.datalogProgramOutput import DatalogProgramOutput
from project2_classes.schemesOutput import SchemesOutput
from project2_classes.factsOutput import FactsOutput
from project2_classes.rulesOutput import RulesOutput
from project2_classes.queriesOutput import QueriesOutput
from project2_classes.domainsOutput import DomainsOutput

class Parser():
    def __init__(self):
        pass


    def throw_error(self):
        raise ValueError(self.getCurrToken().to_string())

    def getCurrToken(self) -> Token:
        if (self.index >= len(self.tokens)):
            self.index = len(self.tokens) -1
            self.throw_error()
        return self.tokens[self.index]
        
    def advance(self):
        self.index += 1

    def match(self, expected_type: str):
        if (self.getCurrToken().token_type == expected_type):
            self.advance()
        else:
            self.throw_error()

    def getPreviousTokenValue(self):
        return self.tokens[self.index-1].value

    def run(self, tokens: list[Token]) -> str:
        self.index: int = 0
        self.tokens: list[Token] = tokens

        self.tokens = self.removeComments(tokens)

        try:
            datalogProgram = self.parseDatalogProgram()
            return datalogProgram.toString()
        except ValueError as ve:
            return f"Failure!\n  {ve}"
        
    def removeComments(self, tokens):
        tokensWithoutComments = []

        for token in tokens:
            if token.token_type != "COMMENT":
                tokensWithoutComments.append(token)
        
        return tokensWithoutComments

    # datalogProgram	->	SCHEMES COLON scheme schemeList FACTS COLON factList RULES COLON ruleList QUERIES COLON query queryList EOF
    def parseDatalogProgram(self):
        allSchemes = []
        allFacts = []
        allRules = []
        allQueries = []

        self.match("SCHEMES")
        self.match("COLON")
        allSchemes.append(self.parseScheme())
        allSchemes += self.parseSchemeList()
        self.match("FACTS")
        self.match("COLON")
        allFacts += self.parseFactList()
        self.match("RULES")
        self.match("COLON")
        allRules += self.parseRuleList()
        self.match("QUERIES")
        self.match("COLON")
        allQueries.append(self.parseQuery())
        allQueries += self.parseQueryList()
        self.match("EOF")

        return DatalogProgramOutput(SchemesOutput(allSchemes), FactsOutput(allFacts), RulesOutput(allRules), QueriesOutput(allQueries), DomainsOutput(allFacts))
    
    # schemeList	->	scheme schemeList | lambda
    def parseSchemeList(self):
        allSchemesList = []
        if self.getCurrToken().token_type == "ID":
            currScheme = self.parseScheme()
            allSchemesList += self.parseSchemeList()
            allSchemesList.insert(0, currScheme)
            return allSchemesList
        else:
            return []
        
    # factList	->	fact factList | lambda
    def parseFactList(self):
        allFactsList = []
        if self.getCurrToken().token_type == "ID":
            currFact = self.parseFact()
            allFactsList += self.parseFactList()
            allFactsList.insert(0, currFact)
            return allFactsList
        else:
            return []
    
    # fact    	->	ID LEFT_PAREN STRING stringList RIGHT_PAREN PERIOD
    def parseFact(self):
        name = ""
        parameters = []

        self.match("ID")
        name = self.getPreviousTokenValue()
        self.match("LEFT_PAREN")
        self.match("STRING")
        parameters.append(self.getPreviousTokenValue())
        parameters += self.parseStringList()
        self.match("RIGHT_PAREN")
        self.match("PERIOD")
        return Predicate(name, parameters)
    
    # stringList	-> 	COMMA STRING stringList | lambda
    def parseStringList(self):
        if self.getCurrToken().token_type == "COMMA":
            self.match("COMMA")
            self.match("STRING")
            currString = [self.getPreviousTokenValue()]
            restStrings = self.parseStringList()
            return currString + restStrings
        else:
            return []

    # ruleList	->	rule ruleList | lambda
    def parseRuleList(self):
        allRulesList = []
        if self.getCurrToken().token_type == "ID":
            currRule = self.parseRule()
            allRulesList += self.parseRuleList()
            allRulesList.insert(0, currRule)
            return allRulesList
        else:
            return []
        
    # rule    	->	headPredicate COLON_DASH predicate predicateList PERIOD
    def parseRule(self):
        predicateList = []

        headPredicate = self.parseHeadPredicate()
        self.match("COLON_DASH")
        predicateList.append(self.parsePredicate())
        predicateList += self.parsePredicateList()
        self.match("PERIOD")
        return (headPredicate, predicateList)
    
    # predicateList	->	COMMA predicate predicateList | lambda
    def parsePredicateList(self):
        predicateList = []

        if self.getCurrToken().token_type == "COMMA":
            self.match("COMMA")
            predicateList.append(self.parsePredicate())
            predicateList += self.parsePredicateList()
            return predicateList
        else:
            return []
    
    # predicate	->	ID LEFT_PAREN parameter parameterList RIGHT_PAREN
    def parsePredicate(self):
        name = ""
        parameters = []

        self.match("ID")
        name = self.getPreviousTokenValue()
        self.match("LEFT_PAREN")
        self.parseParameter()
        parameters.append(self.getPreviousTokenValue())
        parameters += self.parseParameterList()
        self.match("RIGHT_PAREN")
        return Predicate(name, parameters)
        
    # parameter	->	STRING | ID
    def parseParameter(self):
        if self.getCurrToken().token_type == "STRING":
            self.match("STRING")
        else:
            self.match("ID")
        
    # parameterList	-> 	COMMA parameter parameterList | lambda
    def parseParameterList(self):
        if self.getCurrToken().token_type == "COMMA":
            self.match("COMMA")
            self.parseParameter()
            currParameter = [self.getPreviousTokenValue()]
            restParameters = self.parseParameterList()
            return currParameter + restParameters
        else:
            return []
        
    # headPredicate	->	ID LEFT_PAREN ID idList RIGHT_PAREN
    def parseHeadPredicate(self):
        name = ""
        parameters = []

        self.match("ID")
        name = self.getPreviousTokenValue()
        self.match("LEFT_PAREN")
        self.match("ID")
        parameters.append(self.getPreviousTokenValue())
        parameters += self.parseIdList()
        self.match("RIGHT_PAREN")
        return Predicate(name, parameters)


    # query	        ->      predicate Q_MARK
    def parseQuery(self):
        if self.getCurrToken().token_type == "ID":
            currQuery = self.parsePredicate()
            self.match("Q_MARK")
            return currQuery
        else:
            return []
        
    # queryList	->	query queryList | lambda
    def parseQueryList(self):
        allQueriesList = []
        if self.getCurrToken().token_type == "ID":
            currQuery = self.parseQuery()
            allQueriesList += self.parseQueryList()
            allQueriesList.insert(0, currQuery)
            return allQueriesList
        else:
            return []

    # scheme   	-> 	ID LEFT_PAREN ID idList RIGHT_PAREN
    def parseScheme(self):
        name = ""
        parameters = []

        self.match("ID")
        name = self.getPreviousTokenValue()
        self.match("LEFT_PAREN")
        self.match("ID")
        parameters.append(self.getPreviousTokenValue())
        parameters += self.parseIdList()
        self.match("RIGHT_PAREN")
        return Predicate(name, parameters)

    
    # idList  	-> 	COMMA ID idList | lambda
    def parseIdList(self):
        if self.getCurrToken().token_type == "COMMA":
            self.match("COMMA")
            self.match("ID")
            currID = [self.getPreviousTokenValue()]
            restIDs = self.parseIdList()
            return currID + restIDs
        else:
            return []

    