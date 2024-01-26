from .fsa_classes.fsa import FSA
from .fsa_classes.colon_dash_fsa import ColonDashFSA
from .fsa_classes.colon_fsa import ColonFSA
from .fsa_classes.left_paren_fsa import LeftParenFSA
from .fsa_classes.comma_fsa import CommaFSA
from .fsa_classes.period_fsa import PeriodFSA
from .fsa_classes.q_mark_fsa import QMarkFSA
from .fsa_classes.right_paren_fsa import RightParenFSA
from .fsa_classes.comment_fsa import CommentFSA
from .fsa_classes.id_fsa import IdFSA
from .fsa_classes.schemes_fsa import SchemesFSA
from .fsa_classes.queries_fsa import QueriesFSA
from .fsa_classes.rules_fsa import RulesFSA
from .fsa_classes.facts_fsa import FactsFSA
from .fsa_classes.string_fsa import StringFSA
from .token import Token

class LexerFSM:
    def __init__(self):
        self.comma_fsa = CommaFSA()
        self.period_fsa = PeriodFSA()
        self.q_mark_fsa = QMarkFSA()
        self.left_paren_fsa = LeftParenFSA()
        self.right_paren_fsa = RightParenFSA()
        self.colon_fsa = ColonFSA()
        self.colon_dash_fsa = ColonDashFSA()
        self.comment_fsa = CommentFSA()
        self.id_fsa = IdFSA()
        self.schemes_fsa = SchemesFSA()
        self.queries_fsa = QueriesFSA()
        self.rules_fsa = RulesFSA()
        self.facts_fsa = FactsFSA()
        self.string_fsa = StringFSA()

        self.tokens: list[function] = [self.comma_fsa, 
                                       self.period_fsa, 
                                       self.q_mark_fsa, 
                                       self.left_paren_fsa, 
                                       self.right_paren_fsa, 
                                       self.colon_fsa, 
                                       self.colon_dash_fsa,
                                       self.comment_fsa,
                                       self.id_fsa,
                                       self.schemes_fsa,
                                       self.queries_fsa,
                                       self.rules_fsa,
                                       self.facts_fsa,
                                       self.string_fsa]
        self.fsa_dict: dict[function, bool] = dict.fromkeys(self.tokens, False)

    def nextNotIdChar(self, input):
        for char in input:
            ordchar = ord(char)
            if (not((65 <= ordchar <= 90) or (97 <= ordchar <= 122) or (48 <= ordchar <= 57))):
                return input.find(char)
                
    def run(self, input: str) -> str:
        lexedAnswer = []
        number_of_tokens = 1
        line = 1
        while len(input) > 0:
            if input[:1] != ' ' and input[:1] != '\n' and input[:1] != '\t':
                output = self.lex(input)
                if output == "UNDEFINED":
                    lexedAnswer.append(Token(output,f"{input[:1]}",line))
                    return lexedAnswer
                else:
                    if output == "COLON_DASH":
                        input = input[1:]
                        lexedAnswer.append(Token(output,':-',line))
                    elif output == "COMMENT":
                        lexedAnswer.append(Token(output,input.split('\n')[0],line))
                        input = input[len(input.split('\n')[0]):]
                    elif output == "ID":
                        lexedAnswer.append(Token(output,input[:self.nextNotIdChar(input)],line))
                        input = input[self.nextNotIdChar(input)-1:]
                    elif output == "SCHEMES":
                        lexedAnswer.append(Token(output,input[:7],line))
                        input = input[6:]
                    elif output == "FACTS":
                        lexedAnswer.append(Token(output,input[:5],line))
                        input = input[4:]
                    elif output == "RULES":
                        lexedAnswer.append(Token(output,input[:5],line))
                        input = input[4:]
                    elif output == "QUERIES":
                        lexedAnswer.append(Token(output,input[:7],line))
                        input = input[6:]
                    elif output == "STRING":
                        input = input[1:]
                        string = "'"
                        lexedAnswer.append(Token(output,f"'{input[:input.find(string)]}'",line))
                        input = input[input.find("'"):]
                    else:
                        lexedAnswer.append(Token(output,f"{input[:1]}",line))
                    number_of_tokens += 1

            if input[:1] == '\n':
                line += 1

            input = input[1:]
        lexedAnswer.append(Token('EOF','',line))

        return lexedAnswer
    
    def lex(self, input_string: str) -> Token:
        for FSA in self.fsa_dict.keys():
            self.fsa_dict[FSA] = FSA.run(input_string)
            FSA.reset()


        return self.__manager_fsm__()

    def __manager_fsm__(self) -> Token:
        output_token = "UNDEFINED"

        output_list = [value for value in self.fsa_dict.values()]
        if output_list == [True, False, False, False, False, False, False, False, False, False, False, False, False, False]: output_token = "COMMA"
        elif output_list == [False, True, False, False, False, False, False, False, False, False, False, False, False, False]: output_token = "PERIOD"
        elif output_list == [False, False, True, False, False, False, False, False, False, False, False, False, False, False]: output_token = "Q_MARK"
        elif output_list == [False, False, False, True, False, False, False, False, False, False, False, False, False, False]: output_token = "LEFT_PAREN"
        elif output_list == [False, False, False, False, True, False, False, False, False, False, False, False, False, False]: output_token = "RIGHT_PAREN"
        elif output_list == [False, False, False, False, False, True, False, False, False, False, False, False, False, False]: output_token = "COLON"
        elif output_list == [False, False, False, False, False, True, True, False, False, False, False, False, False, False]: output_token = "COLON_DASH"
        elif output_list == [False, False, False, False, False, False, False, True, False, False, False, False, False, False]: output_token = "COMMENT"
        if output_list[:9] == [False, False, False, False, False, False, False, False, True]: output_token = "ID"
        if output_list == [False, False, False, False, False, False, False, False, True, True, False, False, False, False]: output_token = "SCHEMES"
        if output_list == [False, False, False, False, False, False, False, False, True, False, True, False, False, False]: output_token = "QUERIES"
        if output_list == [False, False, False, False, False, False, False, False, True, False, False, True, False, False]: output_token = "RULES"
        if output_list == [False, False, False, False, False, False, False, False, True, False, False, False, True, False]: output_token = "FACTS"
        if output_list == [False, False, False, False, False, False, False, False, False, False, False, False, False, True]: output_token = "STRING"

        return output_token        

    def reset(self) -> None:
        for FSA in self.fsa_dict.keys():
            FSA.reset()