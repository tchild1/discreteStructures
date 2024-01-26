class QueriesOutput():
    def __init__(self, queries) -> None:
        self.queries = queries
    
    def toString(self):
        output = f'Queries({len(self.queries)}):'

        for query in self.queries:
            output += f'\n  {query.toString()}?'
    
        return output