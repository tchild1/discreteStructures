from typing import Callable

class FSA:
    def __init__(self, name):
        self.fsa_name = name          # name of your state machine
        self.start_state = self.S0  # start state always named s0 in this implementation
        self.accept_states = set()  # set of accept states must be specified in derived class
        self.input_string = ""      # input string and
        self.num_chars_read = 0     # current input character
    
    def S0(self) -> Callable:
        raise NotImplementedError()
    
    def run(self, input_string: str) -> bool:
        self.input_string = input_string
        current_state = self.start_state
        while self.num_chars_read < len(self.input_string):
            current_state = current_state()
        if current_state in self.accept_states:
            return True
        else:
            return False

    def reset(self) -> None:
        self.num_chars_read = 0
        self.input_string = ""

    def get_name(self) -> str: 
        return self.fsa_name

    def set_name(self, FSA_name) -> None:
        self.fsa_name = FSA_name

    def __get_current_input(self) -> str:  # The double underscore makes the method private
        current_input = self.input_string[self.num_chars_read]
        self.num_chars_read += 1
        return current_input