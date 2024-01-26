class RulesOutput():
    def __init__(self, rules) -> None:
        self.rules = rules
    
    def toString(self):
        output = f'Rules({len(self.rules)}):'

        for rule in self.rules:
            output += f'\n  {rule[0].toString()} :- '
            for predicate in rule[1]:
                output += f'{predicate.toString()},'
            output = output[:-1]
            output = output + '.'
    
        return output