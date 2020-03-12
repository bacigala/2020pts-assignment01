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

    #finds index of element
    def indexOf(self, x):
        if (x in self.values):
            return self.values.index(x)
        else:
            return -1
    
    #returns empty Relation with united values with self
    def unitedValuesRelation(self, otherRelation):
        newValues = pvector()
        for x in self.values:
            newValues = newValues.append(x)
        for x in otherRelation.values:
            if not (x in newValues):
                newValues = newValues.append(x)
        return Relation(newValues)


    #1 returns true if x and y are in relation
    def has(self, x, y):
        if (x in self.values) and (y in self.values):
            indexX = self.values.index(x)
            indexY = self.values.index(y)
            return self.relations[indexX][indexY]
        else:
            return False

    #2 adds element (x,y) to relation
    def add(self, x, y):
        indexX = self.indexOf(x)
        indexY = self.indexOf(y)
        if (indexX > -1) and (indexY > -1):
            newSubRelations = self.relations[indexX].set(indexY, True)
            return Relation(self.values, self.relations.set(indexX, newSubRelations))
        else:
            return self

    #3 removes element (x,y) form relation
    def remove(self, x, y):
        if self.has(x,y):
            indexX = self.indexOf(x)
            indexY = self.indexOf(y)
            newSubRelations = self.relations[indexX].set(indexY, False)
            return Relation(self.values, self.relations.set(indexX, newSubRelations))

    #4 returns union of two relations
    def union(self, otherRelation):
        newRelation = self.unitedValuesRelation(otherRelation)
        for x in self.values:
            for y in self.values:
                if self.has(x,y):
                    newRelation = newRelation.add(x,y)
        for x in otherRelation.values:
            for y in otherRelation.values:
                if otherRelation.has(x,y):
                    newRelation = newRelation.add(x,y)
        return newRelation
