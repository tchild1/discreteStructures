from .fsa import FSA
from typing import Callable

class PeriodFSA(FSA):
    def __init__(self):
        FSA.__init__(self, "PeriodFSA")
        self.accept_states.add(self.S1)
    
    def S0(self) -> Callable:
        next_state = None
        if self.input_string[self.num_chars_read] != '.':
            next_state = self.s_err
        else:
            next_state = self.S1
        self.num_chars_read += 1
        return next_state
    
    def S1(self):
        next_state = self.S1
        self.num_chars_read += 1
        return next_state
    
    def s_err(self):
        next_state = self.s_err
        self.num_chars_read +=1
        return next_state
    
    