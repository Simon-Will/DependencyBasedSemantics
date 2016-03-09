#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def makeElementFixedObj(obj):
    def elementFixedObj(subj):
        return subj in obj
    return elementFixedObj

def makeSubsetFixedObj(obj):
    def subsetFixedObj(subj):
        return subj.issubset(obj)
    return subsetFixedObj

def makeSupersetFixedObj(obj):
    def supersetFixedObj(subj):
        return subj.issuperset(obj)
    return supersetFixedObj

def makeNotElementFixedObj(obj):
    def notElementFixedObj(subj):
        return subj in obj
    return notElementNotedObj

def makeNotSubsetFixedObj(obj):
    def notSubsetFixedObj(subj):
        return subj.issubset(obj)
    return notSubsetFixedObj

def makeNotSupersetFixedObj(obj):
    def notSupersetFixedObj(subj):
        return subj.issuperset(obj)
    return notSupersetFixedObj

RELATION_DICT = {
        'element': makeElementFixedObj,
        'subset': makeSubsetFixedObj,
        'superset': makeSupersetFixedObj,
        'not_element': makeNotElementFixedObj,
        'not_subset': makeNotSubsetFixedObj,
        'not_superset': makeNotSupersetFixedObj,
        }

class Condition():

    def __init__(self, conditionString):
        self.subj, self.pred, self.obj = Condition.splitConditionString(
                conditionString)
        self.relation = RELATION_DICT[self.pred]
        self.relationFixedObj = self.relation(self.obj)

    def __str__(self):
        return '{0.subj} {0.pred} {0.obj}'.format(self)
    
    @staticmethod
    def splitConditionString(conditionString):
        subj, pred, obj = conditionString.split(maxsplit=2)
        obj = eval(obj)
        return subj, pred, obj
    
    def __call__(self, node):
        subj = node[self.subj]
        if isinstance(subj, dict):
            return self.relationFixedObj(set(subj.keys()))
        else:
            return self.relationFixedObj(subj)

def test():
    alphabet = {chr(n) for n in range(0x61, 0x61 + 26)}
    abc = {'a', 'b', 'c'}
    inAlphabet = makeSubsetFixedObj(alphabet)
    print(inAlphabet)
    print(inAlphabet(abc))
    print(inAlphabet({'%'}))

if __name__ == '__main__':
    test()
