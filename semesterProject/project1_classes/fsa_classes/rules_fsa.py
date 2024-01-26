from .fsa import FSA
from typing import Callable

class RulesFSA(FSA):
    def __init__(self):
        FSA.__init__(self, "Rules")
        self.accept_states.add(self.S6)
    
    def S0(self) -> Callable:
        next_state = None
        if self.input_string[self.num_chars_read] != 'R':
            next_state = self.s_err
        else:
            next_state = self.S1
        self.num_chars_read += 1
        return next_state
    
    def S1(self):
        next_state = None
        if self.input_string[self.num_chars_read] != 'u':
            next_state = self.s_err
        else:
            next_state = self.S2
        self.num_chars_read += 1
        return next_state
    
    def S2(self):
        next_state = None
        if self.input_string[self.num_chars_read] != 'l':
            next_state = self.s_err
        else:
            next_state = self.S3
        self.num_chars_read += 1
        return next_state
    
    def S3(self):
        next_state = None
        if self.input_string[self.num_chars_read] != 'e':
            next_state = self.s_err
        else:
            next_state = self.S4
        self.num_chars_read += 1
        return next_state
    
    def S4(self):
        next_state = None
        if self.input_string[self.num_chars_read] != 's':
            next_state = self.s_err
        else:
            next_state = self.S5
        self.num_chars_read += 1
        return next_state
    
    def S5(self):
        next_state = None
        if (self.input_string[self.num_chars_read] != ':' and self.input_string[self.num_chars_read:self.num_chars_read+1] != '\n'):
            next_state = self.s_err
        else:
            next_state = self.S6
        self.num_chars_read += 1
        return next_state
    
    def S6(self):
        next_state = self.S6
        self.num_chars_read += 1
        return next_state
    
    def s_err(self):
        next_state = self.s_err
        self.num_chars_read +=1
        return next_state
    
    