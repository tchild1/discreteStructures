from project1_classes.lexer_fsm import LexerFSM
from project2_classes.my_parser import Parser

#Return your program output here for grading (can treat this function as your "main")
def project2(input: str) -> str:
    lexer = LexerFSM()
    lexerOutput = lexer.run(input)

    parser = Parser()
    return parser.run(lexerOutput)

def read_file_contents(filepath):
    with open(filepath, "r") as f:
        return f.read() 

#Use this to run and debug code within VS
if __name__ == "__main__":
    input_contents = read_file_contents("./project2-passoff/80/input0.txt")
    print(project2(input_contents))
