#!/usr/bin/env python3
class FuzzySetsDict(dict):

    def printFuzzySetsDict(self):
        for elem in self:
            print("setid:     ", elem)
            self[elem].printSet()


class FuzzySet:
    var = ""  # variable of the fuzzy set (ex.: Age)
    label = ""  # label of the specific fuzzy set (ex.: Young)
    x = []  # list of abscissas, from xmin to xmax, 1 by 1
    y = []  # list of ordinates (float)

    def calculateMembershipDegree(self, value):
        if value < min(self.x) or value > max(self.x):
            return 0  # El valor está fuera del rango del conjunto difuso
        for i in range(len(self.x) - 1):
            if value >= self.x[i] and value <= self.x[i + 1]:
                # Calcular el grado de pertenencia interpolando linealmente entre dos puntos
                slope = (self.y[i + 1] - self.y[i]) / (self.x[i + 1] - self.x[i])
                return self.y[i] + slope * (value - self.x[i])
        return 0  # En caso de que no se encuentre un valor coincidente
    def printSet(self):
        print("var:       ", self.var)
        print("label:     ", self.label)
        # print("x coord:   ", self.x)
        # print("y coord:   ", self.y)
        print("memDegree: ", self.memDegree)
        print()


class RuleList(list):
    def printRuleList(self):
        for elem in self:
            elem.printRule()


class Rule:
    ruleName = ""  # name of the rule (str)
    antecedent = []  # list of setids
    consequent = ""  # just one setid
    strength = 0  # float
    consequentX = []  # output fuzzySet, abscissas
    consequentY = []  # output fuzzySet, ordinates

    def printRule(self):
        print("ruleName: ", self.ruleName)
        print("IF        ", self.antecedent)
        print("THEN      ", self.consequent)
        print("strength: ", self.strength)
        print()


class Application:
    appId = ""  # application identifier (str)
    data = []  # list of ValVarPair

    def printApplication(self):
        print("App ID: ", self.appId)
        for elem in self.data:
            print(elem[0], " is ", elem[1])
        print()
