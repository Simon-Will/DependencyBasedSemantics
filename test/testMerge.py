#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This is more of an integration test than a unit test.
# It relies on montesniere.assign working correctly.

import unittest
import sys
import os
import inspect

import nltk.parse as nlp
import nltk.sem.logic as nll

from context import montesniere

tlp = nll.LogicParser(type_check=True)

def getMergedRepresentation(conllFile, rules):
    with open(conllFile) as f:
        depGraph = nlp.DependencyGraph(f.read())
    assigner = montesniere.assign.SemRepAssigner.fromfile(rules, ascii=True)
    assigner.assignToDependencyGraph(depGraph)
    merger = montesniere.merge.SemMerger(depGraph)
    return merger.getSemantics()

def assertEquivalent(self, expr1, expr2):
    self.assertTrue(expr1.equiv(expr2))

class BeissendeTaube(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conllFile = os.path.join(TEST_DIR, 'beissende_taube.conll')
        cls.merged = getMergedRepresentation(conllFile, RULES)

    def testBeissendeTaube(self):
        assigned = BeissendeTaube.merged
        semRep = r'exists x. (Taube(x) & beissen(x,Peter))'
        semSig = {'Peter': 'e', 'Taube': '<e,t>', 'beissen': '<e,<e,t>>'}
        expected = tlp.parse(semRep, signature=semSig)
        self.assertEquivalent(assigned, expected)

class SchenkenderHase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conllFile = os.path.join(TEST_DIR, 'schenkender_hase.conll')
        cls.merged = getMergedRepresentation(conllFile, RULES)

    def testSchenkenderHase(self):
        assigned = SchenkenderHase.merged
        semRep = r'exists x. (hase(x) & exists y. (igel(y) & exists z. (blume(z) & schenken(x,y,z))))'
        semSig = {'hase': '<e,t>', 'igel': '<e,t>', 'blume': '<e,t>', 'schenken': '<e,<e,<e,t>>>'}
        expected = tlp.parse(semRep, signature=semSig)
        self.assertEquivalent(assigned, expected)

class LehrenderLehrer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conllFile = os.path.join(TEST_DIR, 'lehrender_lehrer.conll')
        cls.merged = getMergedRepresentation(conllFile, RULES)

    def testSchenkenderHase(self):
        assigned = SchenkenderHase.merged
        semRep = r'exists x. (lehrer(x) & exists z. (musikstueck(z) & lehren(x,maria,z))))'
        semSig = {'maria': 'e', 'lehrer': '<e,t>', 'musikstueck': '<e,t>', 'lehren': '<e,<e,<e,t>>>'}
        expected = tlp.parse(semRep, signature=semSig)
        self.assertEquivalent(assigned, expected)

if __name__ == '__main__':
    unittest.TestCase.assertEquivalent = assertEquivalent
    global RULES
    global TEST_DIR
    pathToHere = inspect.getfile(inspect.currentframe())
    pathToTop = os.path.dirname(os.path.dirname(pathToHere))
    RULES = os.path.join(pathToTop, 'rules/heuristic_rules.json')
    TEST_DIR = os.path.join(pathToTop, 'test/conll/')

    unittest.main()
