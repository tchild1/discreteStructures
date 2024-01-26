from .Header import Header
from .Row import Row

class Relation:
    def __init__(self, name: str, header: Header, rows: set = set()) -> None:
        self.name = name
        self.header = header
        self.rows = rows
    
    def __str__(self) -> str:
        outputString = ""
        for row in sorted(self.rows):
            if len(row.values) == 0:
                continue
            sep = '  '

            uniqueHeaders = []
            index = 0
            indexes = []
            for header in list(self.header.values):
                if header not in uniqueHeaders:
                    uniqueHeaders.append(header)
                    indexes.append(index)
                index += 1

            for i in range(len(indexes)):
                outputString += sep
                outputString += f'{self.header.values[indexes[i]]}'
                outputString += '='
                outputString += row.values[indexes[i]]
                sep = ', '

            outputString += '\n'
        return outputString
        
    def add_row(self, row: Row) -> None:
        if len(row.values) != len(self.header.values):
            raise ValueError("Row was not the same length as Header")
        self.rows.add(row)
    
    def select1(self, value: str, colIndex: int) -> 'Relation':
        returnRelation = Relation('ResultRelation', self.header, set())
        newRows = self.rows
        for row in newRows:
            if row.values[colIndex] == value:
                returnRelation.add_row(row)
        return returnRelation
    
    def selectWithVariable(self, variables, parameter):
        returnRelation = Relation('ResultRelation', self.header, set())
        newRows = self.rows
        for row in newRows:
            successCount = 0
            for var in variables:
                indexesWithThisVariable = variables[var]
                for varindex in range(0, len(indexesWithThisVariable)):
                    firstValueWithVariable = row.values[indexesWithThisVariable[0]]
                    for index in range(0, len(indexesWithThisVariable)):
                        if row.values[indexesWithThisVariable[varindex]] != firstValueWithVariable:
                            break
                        elif ((row.values[indexesWithThisVariable[varindex]] == firstValueWithVariable)
                        and (index == len(indexesWithThisVariable)-1)):
                            successCount += 1
                            if successCount == self.getNumOfVarIndexes(variables):
                                returnRelation.add_row(row)

        return returnRelation
    
    def getNumOfVarIndexes(self, variables):
        allList = []
        for key in variables:
            allList += variables[key]

        return len(allList)

    
    def select2(self, index1: int, index2: int) -> 'Relation':
        ...
    
    
    def rename(self, new_header: Header) -> 'Relation':
        self.header = new_header

    def project(self, col_indexes: list[int], queryParameters) -> 'Relation':
        newRows = []
        col_indexes.sort()
        for row in self.rows:
            newRow = Row(row.values)
            newRows.append(newRow)
        for row in newRows:
            newList = []
            for column in col_indexes:
                newList.append(row.values[column])
            row.values = newList

        newHeaders = []
        for column in col_indexes:
            newHeaders.append(queryParameters[column])

        newRelation = Relation('ProjectedRelation', Header(newHeaders), newRows)
        return newRelation

    def reduceToOnlyMatchingRows(self, otherRelation: 'Relation'):
        returnRelation = Relation('RelationOfAllQueries', self.header, set())
        newRows = set()
        for row in self.rows:
            for otherRow in otherRelation.rows:
                if row == otherRow:
                    newRows.add(row)
        returnRelation.rows = newRows
        
        return returnRelation

    def natural_join(self, other: 'Relation') -> 'Relation':
        r1: Relation = self
        r2: Relation = other
        
        overlap: list[tuple(int,int)] = []
        unique_cols_2: list[int] = []
        
        for x in range(len(r2.header.values)):
            is_unique = True
            for y in range(len(r1.header.values)):
                if r2.header.values[x] == r1.header.values[y]:
                    overlap.append(tuple([x,y]))
                    is_unique = False
            if is_unique:
                unique_cols_2.append(x)
                    
        h: Header = self.join_headers(r1.header, r2.header, unique_cols_2)

        result: Relation = Relation(r1.name + "|x|" + r2.name, h, set())
        for t1 in r1.rows:
            for t2 in r2.rows:
                if self.can_join_rows(t1, t2, overlap):
                    result_row = self.join_rows(t1, t2, unique_cols_2)
                    result.add_row(result_row)
        
        return result
    
    def join_headers(self, header1: Header, header2: Header, unique_cols_2: list[int]) -> Header:
        new_header_values = []
        new_header_values.extend(header1.values)
        for x in unique_cols_2:
            new_header_values.append(header2.values[x])

        return Header(new_header_values)
    
    def can_join_rows(self, row1: Row, row2: Row, overlap: list[tuple[int,int]]) -> bool:
        for x,y in overlap:
            if row2.values[x] != row1.values[y]:
                return False

        return True
    
    def join_rows(self, row1: Row, row2: Row, unique_cols_2: list[int]) -> Row:
        new_row_values = []
        new_row_values.extend(row1.values)

        for x in unique_cols_2:
            new_row_values.append(row2.values[x])

        return Row(new_row_values)