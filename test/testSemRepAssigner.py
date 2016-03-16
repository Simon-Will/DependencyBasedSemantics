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
        cls.depGraph = nlp.DependencyGraph(open(conllFile).read())
        assigner = montesniere.SemRepAssigner.fromfile(RULES)
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
        semRepPat = r'\x y. beißen(y,x)'
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
        cls.depGraph = nlp.DependencyGraph(open(conllFile).read())
        assigner = montesniere.SemRepAssigner.fromfile(RULES)
        assigner.assignToDependencyGraph(cls.depGraph)

    def testEin(self):
        assigned = SchenkenderHase.depGraph.get_by_address(1)['semrep']
        semRepPat = r'\P Q. exists x. (P(x) & Q(x))'
        semSig = {'P': '<e,t>', 'Q': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testHase(self):
        assigned = SchenkenderHase.depGraph.get_by_address(2)['semrep']
        semRepPat = r'\x. Taube(x)'
        semSig = {'hase': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testSchenkt(self):
        assigned = SchenkenderHase.depGraph.get_by_address(3)['semrep']
        semRepPat = r'\x y z. beißen(z,y,x)'
        semSig = {'schenken': '<e,<e,<e,t>>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testEinem(self):
        assigned = SchenkenderHase.depGraph.get_by_address(4)['semrep']
        semRepPat = r'\P R x. exists y. (P(y) & R(x,y))'
        semSig = {'P': '<e,t>', 'R': '<e<e,t>>'}
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
        semRepPat = r'\P T y x. exists z. (P(z) & T(x,y,z))'
        semSig = {'P': '<e,t>', 'T': '<e,<e,<e,t>>>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testBlume(self):
        assigned = SchenkenderHase.depGraph.get_by_address(7)['semrep']
        semRepPat = r'\x. blume(x)'
        semSig = {'blume': '<e,t>'}
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
