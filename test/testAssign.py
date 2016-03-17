#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys
import os
import inspect

import nltk.parse as nlp
import nltk.sem.logic as nll

from context import montesniere

tlp = nll.LogicParser(type_check=True)

class BeissendeTaube(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conllFile = os.path.join(TEST_DIR, 'beissende_taube.conll')
        with open(conllFile) as f:
            cls.depGraph = nlp.DependencyGraph(f.read())
        assigner = montesniere.assign.SemRepAssigner.fromfile(RULES)
        assigner.assignToDependencyGraph(cls.depGraph)

    def testEine(self):
        assigned = BeissendeTaube.depGraph.get_by_address(1)['semrep']
        semRepPat = r'\P Q. exists x. (P(x) & Q(x))'
        semSig = {'P': '<e,t>', 'Q': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testTaube(self):
        assigned = BeissendeTaube.depGraph.get_by_address(2)['semrep']
        semRepPat = r'\x. Taube(x)'
        semSig = {'Taube': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testBeisst(self):
        assigned = BeissendeTaube.depGraph.get_by_address(3)['semrep']
        semRepPat = r'\y x. beißen(x,y)'
        semSig = {'beißen': '<e,<e,t>>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testPeter(self):
        assigned = BeissendeTaube.depGraph.get_by_address(4)['semrep']
        semRepPat = r'Peter'
        semSig = {'Peter': 'e'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

class SchenkenderHase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conllFile = os.path.join(TEST_DIR, 'schenkender_hase.conll')
        with open(conllFile) as f:
            cls.depGraph = nlp.DependencyGraph(f.read())
        assigner = montesniere.assign.SemRepAssigner.fromfile(RULES)
        assigner.assignToDependencyGraph(cls.depGraph)

    def testEin(self):
        assigned = SchenkenderHase.depGraph.get_by_address(1)['semrep']
        semRepPat = r'\P Q. exists x. (P(x) & Q(x))'
        semSig = {'P': '<e,t>', 'Q': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testHase(self):
        assigned = SchenkenderHase.depGraph.get_by_address(2)['semrep']
        semRepPat = r'\x. hase(x)'
        semSig = {'hase': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testSchenkt(self):
        assigned = SchenkenderHase.depGraph.get_by_address(3)['semrep']
        semRepPat = r'\z y x. schenken(x,y,z)'
        semSig = {'schenken': '<e,<e,<e,t>>>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testEinem(self):
        assigned = SchenkenderHase.depGraph.get_by_address(4)['semrep']
        semRepPat = r'\P R x. exists y. (P(y) & R(y)(x))'
        semSig = {'P': '<e,t>', 'R': '<e,<e,t>>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testIgel(self):
        assigned = SchenkenderHase.depGraph.get_by_address(5)['semrep']
        semRepPat = r'\x. igel(x)'
        semSig = {'igel': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testEine(self):
        assigned = SchenkenderHase.depGraph.get_by_address(6)['semrep']
        semRepPat = r'\P T y x. exists z. (P(z) & T(z)(y)(x))'
        semSig = {'P': '<e,t>', 'T': '<e,<e,<e,t>>>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testBlume(self):
        assigned = SchenkenderHase.depGraph.get_by_address(7)['semrep']
        semRepPat = r'\x. blume(x)'
        semSig = {'blume': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

class LehrenderLehrer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conllFile = os.path.join(TEST_DIR, 'lehrender_lehrer.conll')
        with open(conllFile) as f:
            cls.depGraph = nlp.DependencyGraph(f.read())
        assigner = montesniere.assign.SemRepAssigner.fromfile(RULES)
        assigner.assignToDependencyGraph(cls.depGraph)

    def testEin(self):
        assigned = LehrenderLehrer.depGraph.get_by_address(1)['semrep']
        semRepPat = r'\P Q. exists x. (P(x) & Q(x))'
        semSig = {'P': '<e,t>', 'Q': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testLehrer(self):
        assigned = LehrenderLehrer.depGraph.get_by_address(2)['semrep']
        semRepPat = r'\x. lehrer(x)'
        semSig = {'lehrer': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testLehrt(self):
        assigned = LehrenderLehrer.depGraph.get_by_address(3)['semrep']
        semRepPat = r'\z y x. lehren(x,y,z)'
        semSig = {'lehren': '<e,<e,<e,t>>>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testMaria(self):
        assigned = LehrenderLehrer.depGraph.get_by_address(4)['semrep']
        semRepPat = r'maria'
        semSig = {'maria': 'e'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testEin2(self):
        assigned = LehrenderLehrer.depGraph.get_by_address(5)['semrep']
        semRepPat = r'\P T y x. exists z. (P(z) & T(z)(y)(x))'
        semSig = {'P': '<e,t>', 'T': '<e,<e,<e,t>>>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testMusikstueck(self):
        assigned = LehrenderLehrer.depGraph.get_by_address(6)['semrep']
        semRepPat = r'\x. musikstück(x)'
        semSig = {'musikstück': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

class LehrlingSein(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conllFile = os.path.join(TEST_DIR, 'lehrling_sein.conll')
        with open(conllFile) as f:
            cls.depGraph = nlp.DependencyGraph(f.read())
        assigner = montesniere.assign.SemRepAssigner.fromfile(RULES)
        assigner.assignToDependencyGraph(cls.depGraph)

    def testJeder(self):
        assigned = LehrlingSein.depGraph.get_by_address(1)['semrep']
        semRepPat = r'\P Q. all x. (P(x) -> Q(x))'
        semSig = {'P': '<e,t>', 'Q': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testStift(self):
        assigned = LehrlingSein.depGraph.get_by_address(2)['semrep']
        semRepPat = r'\x. stift(x)'
        semSig = {'stift': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testIst(self):
        assigned = LehrlingSein.depGraph.get_by_address(3)['semrep']
        semRepPat = r'\P. P'
        semSig = {'P': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testEin(self):
        assigned = LehrlingSein.depGraph.get_by_address(4)['semrep']
        semRepPat = r'\P. P'
        semSig = {'P': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testLehrling(self):
        assigned = LehrlingSein.depGraph.get_by_address(5)['semrep']
        semRepPat = r'\x. lehrling(x)'
        semSig = {'lehrling': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

if __name__ == '__main__':
    global RULES
    global TEST_DIR
    pathToHere = inspect.getfile(inspect.currentframe())
    pathToTop = os.path.dirname(os.path.dirname(pathToHere))
    RULES = os.path.join(pathToTop, 'rules/heuristic_rules.json')
    TEST_DIR = os.path.join(pathToTop, 'test/conll/')

    unittest.main()
