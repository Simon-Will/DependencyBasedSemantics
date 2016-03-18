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

    def testLehrenderLehrer(self):
        assigned = LehrenderLehrer.merged
        semRep = r'exists x. (lehrer(x) & exists z. (musikstueck(z) & lehren(x,maria,z)))'
        semSig = {'maria': 'e', 'lehrer': '<e,t>', 'musikstueck': '<e,t>', 'lehren': '<e,<e,<e,t>>>'}
        expected = tlp.parse(semRep, signature=semSig)
        self.assertEquivalent(assigned, expected)

class LehrlingSein(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conllFile = os.path.join(TEST_DIR, 'lehrling_sein.conll')
        cls.merged = getMergedRepresentation(conllFile, RULES)

    def testLehrlingSein(self):
        assigned = LehrlingSein.merged
        semRep = r'all x. (stift(x) -> lehrling(x))'
        semSig = {'stift': '<e,t>', 'lehrling': '<e,t>'}
        expected = tlp.parse(semRep, signature=semSig)
        self.assertEquivalent(assigned, expected)

class KeinMenschZahlt(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conllFile = os.path.join(TEST_DIR, 'kein_mensch_zahlt.conll')
        cls.merged = getMergedRepresentation(conllFile, RULES)

    def testKeinMenschZahlt(self):
        assigned = KeinMenschZahlt.merged
        semRep = r'! exists x. (mensch(x) & exists y. (rechnung(y) & zahlen(x,y)))'
        semSig = {'mensch': '<e,t>', 'rechnung': '<e,t>'}
        expected = tlp.parse(semRep, signature=semSig)
        self.assertEquivalent(assigned, expected)

class SchuppigesBein(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conllFile = os.path.join(TEST_DIR, 'schuppiges_bein.conll')
        cls.merged = getMergedRepresentation(conllFile, RULES)

    def testSchuppigeBeine(self):
        assigned = SchuppigesBein.merged
        semRep = r'all x. (sirene(x) -> exists y. (haben(x,y) & bein(x) & schuppig(x))'
        semSig = {'sirene': '<e,t>', 'bein': '<e,t>', 'schuppig': '<e,t>', 'haben': '<e,<e,t>>'}
        expected = tlp.parse(semRep, signature=semSig)
        self.assertEquivalent(assigned, expected)

# This test can not succeed because the rules can not yet handle plural nouns
# except in subject position
class SchuppigeBeine(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conllFile = os.path.join(TEST_DIR, 'schuppige_beine.conll')
        cls.merged = getMergedRepresentation(conllFile, RULES)

    def testSchuppigeBeine(self):
        assigned = SchuppigeBeine.merged
        semRep = r'all x. (sirene(x) -> exists y. (haben(x,y) & bein(x) & schuppig(x))'
        semSig = {'sirene': '<e,t>', 'bein': '<e,t>', 'schuppig': '<e,t>', 'haben': '<e,<e,t>>'}
        expected = tlp.parse(semRep, signature=semSig)
        self.assertEquivalent(assigned, expected)

# This test seems to create an infinite loop. Comment this test to run the rest.
# Or, better yet: Fix SemMerger to cover this test.
class SchnelleJaegerin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conllFile = os.path.join(TEST_DIR, 'schnelle_jägerin.conll')
        cls.merged = getMergedRepresentation(conllFile, RULES)

    def testSchnelleJaegerin(self):
        assigned = SchnelleJaegerin.merged
        semRep = r'exists x. (schnell(x) & jaegerin(x) & erzuernen(x,plexippos))'
        semSig = {'schnell': '<e,t>', 'jaegerin': '<e,t>', 'erzuernen': '<e,<e,t>>', 'plexippos': 'e'}
        expected = tlp.parse(semRep, signature=semSig)
        self.assertEquivalent(assigned, expected)

# This test can not succeed because adverbs are not yet handled correctly by
# the SemRepAssigner.
class Waldgurken(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conllFile = os.path.join(TEST_DIR, 'waldgurken.conll')
        cls.merged = getMergedRepresentation(conllFile, RULES)

    def testWaldgurken(self):
        assigned = Waldgurken.merged
        semRep = r'exists x. (wald(x) & in(all y. (gurke(y) -> leben(y))),x)'
        semSig = {'gurke': '<e,t>', 'leben': '<e,t>'}
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
