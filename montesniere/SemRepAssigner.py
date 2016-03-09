#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#from nltk.grammar import DependencyGrammar
#import nltk.sem.logic as nll
#import nltk.parse as nlp

from Condition import *

class SemRepRule:

    def __init__(self, conditions, semRepPat):
        self.semRepPat = semRepPat
        self.conditions = []
        try:
            if isinstance(conditions[0], Condition):
                self.conditions = conditions
            elif isinstance(conditions[0], str):
                self.conditions = [
                        Condition(c) for c in conditions
                        ]
            else:
                raise TypeError(
                        'conditions is not a list of str or Condition objects')
        except KeyError as e:
            # The conditions set is empty. This is OK.
            pass

    @classmethod
    def fromstring(cls, s):
        """Read a SemRepRule from a string and return it."""
        pass

    def testConditions(self, node):
        """Apply a rule to a node and return True if all conditions are
        met, False otherwise.
        """
        for cond in self.conditions:
            if not cond(node):
                return False
        else:
            # All conditions are met.
            return True

    def __str__(self):
        s = '<SemRepRule: conditions={0.conditions}, semRepPat={0.semRepPat}>'
        return s.format(self)

class SemRepAssigner:

    def __init__(self, rules):
        self.rules = rules

    def assignToDependencyGraph(self, dg):
        """Assign semantic representations to the nodes in the
        DependencyGraph dg and return the updated DependencyGraph.
        """
        pass
    
    def assignToNode(self, node):
        """Assign semantic representations to the given node and
        return the updated node.
        """
        pass



def test():

    import nltk.parse as nlp
    rules = [
            SemRepRule(
                [
                    r'tag element {"NE"}',
                    r'rel element {"SB"}'
                ],
                r'\P. P({[lemma]})'
                ),
            SemRepRule(
                [
                    r'tag element {"NE"}',
                    r'rel not_element(NK) {"SB"}'
                ],
                r'{[lemma]}'
                ),
            SemRepRule(
                [
                    r'tag element {"NN"}'
                ],
                r'\x. {[lemma]}(x)'
                ),
            SemRepRule(
                [
                    r'tag element {"ART"}',
                    r'lemma element {"ein"}',
                    r'rel element(NK) {"SB"}'
                ],
                r'\PQ. exists x. (P(x) & Q(x))'
                ),
            SemRepRule(
                [
                    r'tag element {"VVFIN"}',
                    r'deps superset {"SB"}',
                    r'deps not_superset {"OA"}'
                ],
                r'\x. {[lemma]}(x)'
                ),
            SemRepRule(
                [
                    r'tag element {"VVFIN"}',
                    r'deps superset {"SB", "OA"}',
                    r'deps not_superset {"OD"}'
                ],
                r'\xy. {[lemma]}(y,x)'
                ),
            SemRepRule(
                [
                    r'tag element {"VVFIN"}',
                    r'deps superset {"SB", "OA", "OD"}'
                ],
                r'\x. {[lemma]}(x)'
                )
            ]

    sTaube = open('../test/beissende_taube.conll').read()
    dgTaube = nlp.DependencyGraph(sTaube)
    beissen = dgTaube.nodes[3]
    for rule in rules:
        print(rule)
        print(rule.testConditions(beissen))
        print("---")

if __name__ == '__main__':
    test()
