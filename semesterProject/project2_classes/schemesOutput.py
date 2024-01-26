class SchemesOutput():
    def __init__(self, schemes) -> None:
        self.schemes = schemes
    
    def toString(self):
        output = f'Schemes({len(self.schemes)}):'

        for scheme in self.schemes:
            output += f'\n  {scheme.toString()}'
    
        return output