class DomainsOutput():
    def __init__(self, facts) -> None:
        self.facts = facts
        self.domain = []

        for fact in facts:
            self.domain += fact.parameters
        self.domain = list(set(self.domain))
        self.domain.sort()
    
    def toString(self):
        output = f'Domain({len(self.domain)}):'

        for domain in self.domain:
            output += f'\n  {domain}'
    
        return output