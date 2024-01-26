from .fsa import FSA
from typing import Callable

class StringFSA(FSA):
    def __init__(self):
        FSA.__init__(self, "String")
        self.accept_states.add(self.S2)
    
    def S0(self) -> Callable:
        next_state = None
        if self.input_string[self.num_chars_read] != "'":
            next_state = self.s_err
        else:
            next_state = self.S1
        self.num_chars_read += 1
        return next_state
    
    def S1(self):
        next_state = None
        if self.input_string[self.num_chars_read] != "'":
            next_state = self.S1
        else:
            next_state = self.S2
        self.num_chars_read += 1
        return next_state
    
    def S2(self):
        next_state = self.S2
        self.num_chars_read += 1
        return next_state
    
    def s_err(self):
        next_state = self.s_err
        self.num_chars_read +=1
        return next_state
    
    