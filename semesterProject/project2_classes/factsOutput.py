class FactsOutput():
    def __init__(self, facts) -> None:
        self.facts = facts
    
    def toString(self):
        output = f'Facts({len(self.facts)}):'

        for fact in self.facts:
            output += f'\n  {fact.toString()}.'
    
        return output