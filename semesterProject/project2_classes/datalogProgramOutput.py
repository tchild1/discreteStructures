class DatalogProgramOutput():
    def __init__(self, schemes, facts, rules, queries, domains) -> None:
        self.schemes = schemes
        self.facts = facts
        self.rules = rules
        self.queries = queries
        self.domains = domains
    
    def toString(self):
        return f'''Success!
{self.schemes.toString()}
{self.facts.toString()}
{self.rules.toString()}
{self.queries.toString()}
{self.domains.toString()}
'''