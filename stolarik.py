from pyrsistent import pvector

def get_relation_class(inputSet):

    #immutable pvector of __values
    values = pvector()
    #pvector of pvectors of booleans = represents relations
    initRelations = pvector()
    
    #fill __values set -> immutable pvector
    for x in inputSet:
        values = values.append(x)
    #create 2D immutable matrix for relations
    for x in range(len(values)):
        subRelations = pvector()
        for y in range(len(values)):
            subRelations = subRelations.append(False)
        initRelations = initRelations.append(subRelations)
    
    class Relation:
        #immutable pvector of __values
        __values = values
        #pvector of pvectors of booleans = represents relations
        __relations = initRelations

        def __init__(self, inputSet = values, inputRelations = False):
            #fill __values set -> immutable pvector
            self.__values = pvector()
            for x in inputSet:
                self.__values = self.__values.append(x)
            #create 2D immutable matrix for relations
            if not inputRelations:
                self.__relations = pvector()
                for x in range(len(self.__values)):
                    subRelations = pvector()
                    for y in range(len(self.__values)):
                        subRelations = subRelations.append(False)
                    self.__relations = self.__relations.append(subRelations)
            else:
                self.__relations = inputRelations
    
        #returns immutable pvector of values
        def getValues(self):
            return self.__values

        #finds index of element
        def indexOf(self, x):
            if (x in self.__values):
                return self.__values.index(x)
            else:
                return -1
    
        #returns empty Relation with united __values with self
        def unitedValuesRelation(self, otherRelation):
            newValues = pvector()
            for x in self.__values:
                newValues = newValues.append(x)
            otherRelationValues = otherRelation.getValues()
            for x in otherRelationValues:
                if not (x in newValues):
                    newValues = newValues.append(x)
            return Relation(newValues)
    

        #1 returns true if x and y are in relation
        def has(self, x, y):
            if (x in self.__values) and (y in self.__values):
                indexX = self.__values.index(x)
                indexY = self.__values.index(y)
                return self.__relations[indexX][indexY]
            else:
                return False

        #2 adds element (x,y) to relation
        def add(self, x, y):
            indexX = self.indexOf(x)
            indexY = self.indexOf(y)
            if (indexX > -1) and (indexY > -1):
                newSubRelations = self.__relations[indexX].set(indexY, True)
                return Relation(self.__values, self.__relations.set(indexX, newSubRelations))
            else:
                return self
    
        #3 removes element (x,y) form relation
        def remove(self, x, y):
            if self.has(x,y):
                indexX = self.indexOf(x)
                indexY = self.indexOf(y)
                newSubRelations = self.__relations[indexX].set(indexY, False)
                return Relation(self.__values, self.__relations.set(indexX, newSubRelations))
    
        #4 returns union of two relations
        def union(self, otherRelation):
            newRelation = self.unitedValuesRelation(otherRelation)
            otherRelationValues = otherRelation.getValues()
            for x in self.__values:
                for y in self.__values:
                    if self.has(x,y):
                        newRelation = newRelation.add(x,y)
            for x in otherRelationValues:
                for y in otherRelationValues:
                    if otherRelation.has(x,y):
                        newRelation = newRelation.add(x,y)
            return newRelation
    
        #5 returns intrersection of two relations
        def intersection(self, otherRelation):
            newRelation = self.unitedValuesRelation(otherRelation)
            for x in self.__values:
                for y in self.__values:
                    if self.has(x,y) and otherRelation.has(x,y):
                        newRelation = newRelation.add(x,y)
            return newRelation

        #6 returns subtraction of two relations
        def subtract(self, otherRelation):
            newRelation = self.unitedValuesRelation(otherRelation)
            for x in self.__values:
                for y in self.__values:
                    if self.has(x,y) and not(otherRelation.has(x,y)):
                        newRelation = newRelation.add(x,y)
            return newRelation

        #7 returns inverse relation
        def inverse(self):
            newRelation = self.unitedValuesRelation(self)
            for x in self.__values:
                for y in self.__values:
                    if not(self.has(x,y)):
                        newRelation = newRelation.add(x,y)
            return newRelation

        #8 returns composition of 2 relations
        def compose(self, otherRelation):
            otherRelationValues = otherRelation.getValues()
            newRelation = self.unitedValuesRelation(otherRelation)
            for x in self.__values:
                for y in self.__values:
                    if self.has(x,y):
                        for y2 in otherRelationValues:
                            if otherRelation.has(y,y2):
                                newRelation = newRelation.add(x,y2)
            return newRelation

        #9 returns true if relation is reflexve
        def isReflexive(self):
            for x in self.__values:
                if not(self.has(x,x)):
                        return False
            return True
    
        #10 returns true if relation is symetric
        def isSymertic(self):
            for x in self.__values:
                for y in self.__values:
                    if self.has(x,y):
                        if not(self.has(y,x)):
                            return False
            return True

        #11 returns true if relation is transitive
        def isTransitive(self):
            for x in self.__values:
                for y in self.__values:
                    if self.has(x,y):
                        for y1 in self.__values:
                            if self.has(y,y1):
                                if not(self.has(x,y1)):
                                    return False
            return True

        #12 returns reflexive-transitive closure
        def getClosure(self):
            newRelation = self
            #add all (x,x) elements = make relation reflexive
            for x in self.__values:
                newRelation = newRelation.add(x,x)
            #make newRelation transitive
            newElement = True
            while newElement:
                newElement = False
                for x in self.__values:    
                    for y in self.__values:
                        if newRelation.has(x,y):
                            for y1 in self.__values:
                                if newRelation.has(y,y1):
                                    if not(newRelation.has(x,y1)):
                                        newRelation = newRelation.add(x,y1)
                                        newElement = True
            return newRelation

    return Relation
