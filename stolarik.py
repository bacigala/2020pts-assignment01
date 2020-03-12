from pyrsistent import pvector

class Relation:
    #immutable pvector of values
    values = pvector()
    #pvector of pvectors of booleans = represents relations
    relations = pvector()

    def __init__(self, inputSet, relations = False):
        #fill values set -> immutable pvector
        for x in inputSet:
            self.values = self.values.append(x)
        #create 2D immutable matrix for relations
        if not relations:
            for x in range(len(self.values)):
                subRelations = pvector()
                for y in range(len(self.values)):
                    subRelations = subRelations.append(False)
                self.relations = self.relations.append(subRelations)
        else:
            self.relations = relations

    #1 returns true if x and y are in relation
    def has(self, x, y):
        if (x in self.values) and (y in self.values):
            indexX = self.values.index(x)
            indexY = self.values.index(y)
            return self.relations[indexX][indexY]
        else:
            return False
