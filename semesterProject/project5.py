from project1_classes.lexer_fsm import LexerFSM
from project2_classes.my_parser import Parser
from project3_classes.Interpreter import Interpreter

#Return your program output here for grading (can treat this function as your "main")
def project5(input: str) -> str:
    lexer = LexerFSM()
    lexerOutput = lexer.run(input)

    parser = Parser()
    datalogProgram =  parser.run(lexerOutput)

    interpreter = Interpreter()
    return interpreter.run(datalogProgram)

def read_file_contents(filepath):
    with open(filepath, "r") as f:
        return f.read() 

#Use this to run and debug code within VS
if __name__ == "__main__":
    input_contents = read_file_contents("./project5-passoff/80/input6.txt")
    print(project5(input_contents))
