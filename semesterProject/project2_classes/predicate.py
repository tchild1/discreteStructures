class Predicate():
    def __init__(self, name: str, parameters: list[str]) -> None:
        self.name = name
        self.parameters = parameters
    
    def toString(self):
        param_str: str = ""
        param_str = ','.join(self.parameters)
        return (f'{self.name}({param_str})')