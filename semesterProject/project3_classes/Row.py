# this is sometimes called tuple, I am renaming it to help be specific
class Row:
    def __init__(self, values: list[str]) -> None:
        self.values = values
    
    def __eq__(self, other: 'Row') -> bool:
        return self.values == other.values
    
    def __hash__(self) -> int:
        return hash(tuple(self.values))
    
    def __lt__(self, other: 'Row') -> bool:
        return self.values < other.values