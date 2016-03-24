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

class KeinMenschZahlt(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conllFile = os.path.join(TEST_DIR, 'kein_mensch_zahlt.conll')
        with open(conllFile) as f:
            cls.depGraph = nlp.DependencyGraph(f.read())
        assigner = montesniere.assign.SemRepAssigner.fromfile(RULES)
        assigner.assignToDependencyGraph(cls.depGraph)

    def testKein(self):
        assigned = KeinMenschZahlt.depGraph.get_by_address(1)['semrep']
        semRepPat = r'\P Q. ! exists x. (P(x) & Q(x))'
        semSig = {'P': '<e,t>', 'Q': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testMensch(self):
        assigned = KeinMenschZahlt.depGraph.get_by_address(2)['semrep']
        semRepPat = r'\x. mensch(x)'
        semSig = {'mensch': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testZahlt(self):
        assigned = KeinMenschZahlt.depGraph.get_by_address(3)['semrep']
        semRepPat = r'\y x. zahlen(x,y)'
        semSig = {'zahlen': '<e,<e,t>>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testEine(self):
        assigned = KeinMenschZahlt.depGraph.get_by_address(4)['semrep']
        semRepPat = r'\P R x. exists y. (P(y) & R(y)(x))'
        semSig = {'P': '<e,t>', 'R': '<e,<e,t>>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testRechnung(self):
        assigned = KeinMenschZahlt.depGraph.get_by_address(5)['semrep']
        semRepPat = r'\x. rechnung(x)'
        semSig = {'rechnung': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

class SchnelleJaegerin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conllFile = os.path.join(TEST_DIR, 'schnelle_jägerin.conll')
        with open(conllFile) as f:
            cls.depGraph = nlp.DependencyGraph(f.read())
        assigner = montesniere.assign.SemRepAssigner.fromfile(RULES)
        assigner.assignToDependencyGraph(cls.depGraph)

    def testEine(self):
        assigned = SchnelleJaegerin.depGraph.get_by_address(1)['semrep']
        semRepPat = r'\P Q. exists x. (P(x) & Q(x))'
        semSig = {'P': '<e,t>', 'Q': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testSchnelle(self):
        assigned = SchnelleJaegerin.depGraph.get_by_address(2)['semrep']
        semRepPat = r'\P x. (schnell(x) & P(x))'
        semSig = {'schnell': '<e,t>', 'P': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testJaegerin(self):
        assigned = SchnelleJaegerin.depGraph.get_by_address(3)['semrep']
        semRepPat = r'\x. jägerin(x)'
        semSig = {'jägerin': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testErzuernen(self):
        assigned = SchnelleJaegerin.depGraph.get_by_address(4)['semrep']
        semRepPat = r'\y x. erzürnen(x,y)'
        semSig = {'erzürnen': '<e,<e,t>>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testPlexippos(self):
        assigned = SchnelleJaegerin.depGraph.get_by_address(5)['semrep']
        semRepPat = r'plexippos'
        semSig = {'plexippos': 'e'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

class SchuppigeBeine(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conllFile = os.path.join(TEST_DIR, 'schuppige_beine.conll')
        with open(conllFile) as f:
            cls.depGraph = nlp.DependencyGraph(f.read())
        assigner = montesniere.assign.SemRepAssigner.fromfile(RULES)
        assigner.assignToDependencyGraph(cls.depGraph)

    def testSirenen(self):
        assigned = SchuppigeBeine.depGraph.get_by_address(1)['semrep']
        semRepPat = r'\P. all x. (sirene(x) -> P(x))'
        semSig = {'P': '<e,t>', 'sirene': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testHaben(self):
        assigned = SchuppigeBeine.depGraph.get_by_address(2)['semrep']
        semRepPat = r'\y x. (haben(x,y))'
        semSig = {'haben': '<e,<e,t>>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testSchuppige(self):
        assigned = SchuppigeBeine.depGraph.get_by_address(3)['semrep']
        semRepPat = r'\x. schuppig(x)'
        semSig = {'schuppig': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testBeine(self):
        assigned = SchuppigeBeine.depGraph.get_by_address(4)['semrep']
        semRepPat = r'\P R x. exists y. (P(y) & bein(y) & R(y)(x))'
        semSig = {'bein': '<e,t>', 'P': '<e,t>', 'R': '<e,<e,t>>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

class HausInRussland(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conllFile = os.path.join(TEST_DIR, 'haus_in_russland.conll')
        with open(conllFile) as f:
            cls.depGraph = nlp.DependencyGraph(f.read())
        assigner = montesniere.assign.SemRepAssigner.fromfile(RULES)
        assigner.assignToDependencyGraph(cls.depGraph)

    def testEin(self):
        assigned = HausInRussland.depGraph.get_by_address(1)['semrep']
        semRepPat = r'\P Q. exists x. (P(x) & Q(x))'
        semSig = {'P': '<e,t>', 'Q': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testHaus(self):
        assigned = HausInRussland.depGraph.get_by_address(2)['semrep']
        semRepPat = r'\x. haus(x)'
        semSig = {'haus': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testIn(self):
        assigned = HausInRussland.depGraph.get_by_address(3)['semrep']
        semRepPat = r'\y P x.(in(x,y) & P(x))'
        semSig = {'P': '<e,t>', 'in': '<e,<e,t>>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testRussland(self):
        assigned = HausInRussland.depGraph.get_by_address(4)['semrep']
        semRepPat = r'russland'
        semSig = {'russland': 'e'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testBrennt(self):
        assigned = HausInRussland.depGraph.get_by_address(5)['semrep']
        semRepPat = r'\x. brennen(x)'
        semSig = {'brennt': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

class WaldGurken(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conllFile = os.path.join(TEST_DIR, 'waldgurken.conll')
        with open(conllFile) as f:
            cls.depGraph = nlp.DependencyGraph(f.read())
        assigner = montesniere.assign.SemRepAssigner.fromfile(RULES)
        assigner.assignToDependencyGraph(cls.depGraph)

    def testAlle(self):
        assigned = WaldGurken.depGraph.get_by_address(1)['semrep']
        semRepPat = r'\P Q. all x. (P(x) -> Q(x))'
        semSig = {'P': '<e,t>', 'Q': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testGurken(self):
        assigned = WaldGurken.depGraph.get_by_address(2)['semrep']
        semRepPat = r'\x. gurke(x)'
        semSig = {'gurke': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testLeben(self):
        assigned = WaldGurken.depGraph.get_by_address(3)['semrep']
        semRepPat = r'\x. leben(x)'
        semSig = {'leben': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testIn(self):
        assigned = WaldGurken.depGraph.get_by_address(4)['semrep']
        semRepPat = r'\x V. in(V,x)'
        semSig = {'V': 't', 'in': '<t,<e,t>>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testEinem(self):
        assigned = WaldGurken.depGraph.get_by_address(5)['semrep']
        semRepPat = r'\P B V. exists x. (P(x) & B(x)(V))'
        semSig = {'P': '<e,t>', 'B': '<e,<t,t>>', 'V': 't'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testWald(self):
        assigned = WaldGurken.depGraph.get_by_address(6)['semrep']
        semRepPat = r'\x. wald(x)'
        semSig = {'wald': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

class FurieInKleid(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conllFile = os.path.join(TEST_DIR, 'furie_in_kleid.conll')
        with open(conllFile) as f:
            cls.depGraph = nlp.DependencyGraph(f.read())
        assigner = montesniere.assign.SemRepAssigner.fromfile(RULES)
        assigner.assignToDependencyGraph(cls.depGraph)

    def testEine(self):
        assigned = FurieInKleid.depGraph.get_by_address(1)['semrep']
        semRepPat = r'\P Q. exists x. (P(x) & Q(x))'
        semSig = {'P': '<e,t>', 'Q': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testFurie(self):
        assigned = FurieInKleid.depGraph.get_by_address(2)['semrep']
        semRepPat = r'\x. furie(x)'
        semSig = {'furie': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testIn(self):
        assigned = FurieInKleid.depGraph.get_by_address(3)['semrep']
        semRepPat = r'\y P x. (in(x,y) & P(x))'
        semSig = {'P': '<e,t>', 'in': '<e,<e,t>>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testEinem(self):
        assigned = FurieInKleid.depGraph.get_by_address(4)['semrep']
        semRepPat = r'\P U Q x. exists y. (P(y) & U(y)(Q)(x))'
        semSig = { 'P': '<e,t>', 'Q': '<e,t>', 'U': '<e,<<e,t>,<e,t>>>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testBlutigen(self):
        assigned = FurieInKleid.depGraph.get_by_address(5)['semrep']
        semRepPat = r'\P x. (blutig(x) & P(x))'
        semSig = {'blutig': '<e,t>', 'P': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testKleid(self):
        assigned = FurieInKleid.depGraph.get_by_address(6)['semrep']
        semRepPat = r'\x. kleid(x)'
        semSig = {'kleid': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testBewacht(self):
        assigned = FurieInKleid.depGraph.get_by_address(7)['semrep']
        semRepPat = r'\y x. bewachen(x,y)'
        semSig = {'bewachen': '<e,<e,t>>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testEinen(self):
        assigned = FurieInKleid.depGraph.get_by_address(8)['semrep']
        semRepPat = r'\P R x. exists y. (P(y) & R(y)(x))'
        semSig = { 'P': '<e,t>', 'R': '<e,<e,t>>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testSchlund(self):
        assigned = FurieInKleid.depGraph.get_by_address(9)['semrep']
        semRepPat = r'\x. schlund(x)'
        semSig = {'schlund': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

class TagInHaengematte(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conllFile = os.path.join(TEST_DIR, 'tag_in_hängematte.conll')
        with open(conllFile) as f:
            cls.depGraph = nlp.DependencyGraph(f.read())
        assigner = montesniere.assign.SemRepAssigner.fromfile(RULES)
        assigner.assignToDependencyGraph(cls.depGraph)

    def testDonald(self):
        assigned = TagInHaengematte.depGraph.get_by_address(1)['semrep']
        semRepPat = r'\P. P(donald)'
        semSig = {'donald': 'e', 'P': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testGeniesst(self):
        assigned = TagInHaengematte.depGraph.get_by_address(2)['semrep']
        semRepPat = r'\y x. genießen(x,y)'
        semSig = {'geniessen': '<e,<e,t>>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testEinen(self):
        assigned = TagInHaengematte.depGraph.get_by_address(3)['semrep']
        semRepPat = r'\P R x. exists y. (P(y) & R(y)(x))'
        semSig = {'P': '<e,t>', 'R': '<e,<e,t>>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testSchoenen(self):
        assigned = TagInHaengematte.depGraph.get_by_address(4)['semrep']
        semRepPat = r'\P x. (schön(x) & P(x))'
        semSig = { 'P': '<e,t>', 'schön': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testTag(self):
        assigned = TagInHaengematte.depGraph.get_by_address(5)['semrep']
        semRepPat = r'\x. tag(x)'
        semSig = {'tag': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testIn(self):
        assigned = TagInHaengematte.depGraph.get_by_address(6)['semrep']
        semRepPat = r'\y P x. (in(x,y) & P(x))'
        semSig = {'P': '<e,t>', 'in': '<e,<e,t>>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testEiner(self):
        assigned = TagInHaengematte.depGraph.get_by_address(7)['semrep']
        semRepPat = r'\P U Q x. exists y. (P(y) & U(y)(Q)(x))'
        semSig = { 'P': '<e,t>', 'Q': '<e,t>', 'U': '<e,<<e,t>,<e,t>>>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testWeichen(self):
        assigned = TagInHaengematte.depGraph.get_by_address(8)['semrep']
        semRepPat = r'\P x. (weich(x) & P(x))'
        semSig = { 'P': '<e,t>', 'weich': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testHaengematte(self):
        assigned = TagInHaengematte.depGraph.get_by_address(9)['semrep']
        semRepPat = r'\x. hängematte(x)'
        semSig = {'hängematte': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

class SingtUndTanzt(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conllFile = os.path.join(TEST_DIR, 'singt_und_tanzt.conll')
        with open(conllFile) as f:
            cls.depGraph = nlp.DependencyGraph(f.read())
        assigner = montesniere.assign.SemRepAssigner.fromfile(RULES)
        assigner.assignToDependencyGraph(cls.depGraph)

    def testMaria(self):
        assigned = SingtUndTanzt.depGraph.get_by_address(1)['semrep']
        semRepPat = r'\P. P(maria)'
        semSig = {'maria': 'e', 'P': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testSingt(self):
        assigned = SingtUndTanzt.depGraph.get_by_address(2)['semrep']
        semRepPat = r'\x. singen(x)'
        semSig = {'singen': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testUnd(self):
        assigned = SingtUndTanzt.depGraph.get_by_address(3)['semrep']
        semRepPat = r'\V W. (W & V)'
        semSig = {'V': 't', 'W': 't'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testPeter(self):
        assigned = SingtUndTanzt.depGraph.get_by_address(4)['semrep']
        semRepPat = r'\P. P(peter)'
        semSig = {'peter': 'e', 'P': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testTanzt(self):
        assigned = SingtUndTanzt.depGraph.get_by_address(5)['semrep']
        semRepPat = r'\x. tanzen(x)'
        semSig = {'tanzen': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

class HeuteBaden(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conllFile = os.path.join(TEST_DIR, 'heute_baden.conll')
        with open(conllFile) as f:
            cls.depGraph = nlp.DependencyGraph(f.read())
        assigner = montesniere.assign.SemRepAssigner.fromfile(RULES)
        assigner.assignToDependencyGraph(cls.depGraph)

    def testHeute(self):
        assigned = HeuteBaden.depGraph.get_by_address(1)['semrep']
        semRepPat = r'\V. heute(V)'
        semSig = {'V': 't', 'heute': '<t,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testBadet(self):
        assigned = HeuteBaden.depGraph.get_by_address(2)['semrep']
        semRepPat = r'\x. baden(x)'
        semSig = {'baden': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testEine(self):
        assigned = HeuteBaden.depGraph.get_by_address(3)['semrep']
        semRepPat = r'\P Q. exists x. (P(x) & Q(x))'
        semSig = {'P': '<e,t>', 'Q': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testTaube(self):
        assigned = HeuteBaden.depGraph.get_by_address(4)['semrep']
        semRepPat = r'\x. taube(x)'
        semSig = {'taube': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

class EinigeVoegel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conllFile = os.path.join(TEST_DIR, 'einige_vögel.conll')
        with open(conllFile) as f:
            cls.depGraph = nlp.DependencyGraph(f.read())
        assigner = montesniere.assign.SemRepAssigner.fromfile(RULES)
        assigner.assignToDependencyGraph(cls.depGraph)

    def testEinige(self):
        assigned = EinigeVoegel.depGraph.get_by_address(1)['semrep']
        semRepPat = r'\P Q. exists x. (P(x) & Q(x))'
        semSig = {'P': '<e,t>', 'Q': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testVoegel(self):
        assigned = EinigeVoegel.depGraph.get_by_address(2)['semrep']
        semRepPat = r'\x. vogel(x)'
        semSig = {'vogel': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testSind(self):
        assigned = EinigeVoegel.depGraph.get_by_address(3)['semrep']
        semRepPat = r'\P. P'
        semSig = {'P': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testSchwaene(self):
        assigned = EinigeVoegel.depGraph.get_by_address(4)['semrep']
        semRepPat = r'\x. schwan(x)'
        semSig = {'schwan': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

class KeineWanduhr(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conllFile = os.path.join(TEST_DIR, 'keine_wanduhr.conll')
        with open(conllFile) as f:
            cls.depGraph = nlp.DependencyGraph(f.read())
        assigner = montesniere.assign.SemRepAssigner.fromfile(RULES)
        assigner.assignToDependencyGraph(cls.depGraph)

    def testEine(self):
        assigned = KeineWanduhr.depGraph.get_by_address(1)['semrep']
        semRepPat = r'\P Q. exists x. (P(x) & Q(x))'
        semSig = {'P': '<e,t>', 'Q': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testUhr(self):
        assigned = KeineWanduhr.depGraph.get_by_address(2)['semrep']
        semRepPat = r'\x. uhr(x)'
        semSig = {'uhr': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testIst(self):
        assigned = KeineWanduhr.depGraph.get_by_address(3)['semrep']
        semRepPat = r'\P. P'
        semSig = {'P': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testKeine(self):
        assigned = KeineWanduhr.depGraph.get_by_address(4)['semrep']
        semRepPat = r'\P x. ! P(x)'
        semSig = {'P': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testWanduhr(self):
        assigned = KeineWanduhr.depGraph.get_by_address(5)['semrep']
        semRepPat = r'\x. wanduhr(x)'
        semSig = {'wanduhr': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

class NichtBeissen(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conllFile = os.path.join(TEST_DIR, 'nicht_beißen.conll')
        with open(conllFile) as f:
            cls.depGraph = nlp.DependencyGraph(f.read())
        assigner = montesniere.assign.SemRepAssigner.fromfile(RULES)
        assigner.assignToDependencyGraph(cls.depGraph)

    def testEin(self):
        assigned = NichtBeissen.depGraph.get_by_address(1)['semrep']
        semRepPat = r'\P Q. exists x. (P(x) & Q(x))'
        semSig = {'P': '<e,t>', 'Q': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testHund(self):
        assigned = NichtBeissen.depGraph.get_by_address(2)['semrep']
        semRepPat = r'\x. hund(x)'
        semSig = {'hund': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testBeisst(self):
        assigned = NichtBeissen.depGraph.get_by_address(3)['semrep']
        semRepPat = r'\y x. beißen(x,y)'
        semSig = {'beißen': '<e,<e,t>>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testPeter(self):
        assigned = NichtBeissen.depGraph.get_by_address(4)['semrep']
        semRepPat = r'peter'
        semSig = {'peter': 'e'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testNicht(self):
        assigned = NichtBeissen.depGraph.get_by_address(5)['semrep']
        semRepPat = r'\P x. ! P(x)'
        semSig = {'P': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

class NichtJederMensch(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conllFile = os.path.join(TEST_DIR, 'nicht_jeder_mensch.conll')
        with open(conllFile) as f:
            cls.depGraph = nlp.DependencyGraph(f.read())
        assigner = montesniere.assign.SemRepAssigner.fromfile(RULES)
        assigner.assignToDependencyGraph(cls.depGraph)

    def testNicht(self):
        assigned = NichtJederMensch.depGraph.get_by_address(1)['semrep']
        semRepPat = r'\E P Q. ! (E(P)(Q))'
        semSig = {'P': '<e,t>', 'Q': '<e,t>', 'E': '<<e,t>,<<e,t>,t>>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testJeder(self):
        assigned = NichtJederMensch.depGraph.get_by_address(2)['semrep']
        semRepPat = r'\P Q. all x. (P(x) -> Q(x))'
        semSig = {'P': '<e,t>', 'Q': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testMensch(self):
        assigned = NichtJederMensch.depGraph.get_by_address(3)['semrep']
        semRepPat = r'\x. mensch(x)'
        semSig = {'mensch': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testIst(self):
        assigned = NichtJederMensch.depGraph.get_by_address(4)['semrep']
        semRepPat = r'\P. P'
        semSig = {'P': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testEin(self):
        assigned = NichtJederMensch.depGraph.get_by_address(5)['semrep']
        semRepPat = r'\P. P'
        semSig = {'P': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testGrieche(self):
        assigned = NichtJederMensch.depGraph.get_by_address(6)['semrep']
        semRepPat = r'\x. grieche(x)'
        semSig = {'grieche': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

class NichtEinHund(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conllFile = os.path.join(TEST_DIR, 'nicht_ein_hund.conll')
        with open(conllFile) as f:
            cls.depGraph = nlp.DependencyGraph(f.read())
        assigner = montesniere.assign.SemRepAssigner.fromfile(RULES)
        assigner.assignToDependencyGraph(cls.depGraph)

    def testNicht(self):
        assigned = NichtEinHund.depGraph.get_by_address(1)['semrep']
        semRepPat = r'\E P Q. ! (E(P)(Q))'
        semSig = {'P': '<e,t>', 'Q': '<e,t>', 'E': '<<e,t>,<<e,t>,t>>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testEin(self):
        assigned = NichtEinHund.depGraph.get_by_address(2)['semrep']
        semRepPat = r'\P Q. exists x. (P(x) & Q(x))'
        semSig = {'P': '<e,t>', 'Q': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testHund(self):
        assigned = NichtEinHund.depGraph.get_by_address(3)['semrep']
        semRepPat = r'\x. hund(x)'
        semSig = {'hund': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testBeisst(self):
        assigned = NichtEinHund.depGraph.get_by_address(4)['semrep']
        semRepPat = r'\y x. beißen(x,y)'
        semSig = {'beißen': '<e,<e,t>>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testPeter(self):
        assigned = NichtEinHund.depGraph.get_by_address(5)['semrep']
        semRepPat = r'peter'
        semSig = {'peter': 'e'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

@unittest.skip('not implemented')
class GrueneAlteBaeume(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conllFile = os.path.join(TEST_DIR, 'grüne_alte_bäume.conll')
        with open(conllFile) as f:
            cls.depGraph = nlp.DependencyGraph(f.read())
        assigner = montesniere.assign.SemRepAssigner.fromfile(RULES)
        assigner.assignToDependencyGraph(cls.depGraph)

    def testGruene(self):
        assigned = GrueneAlteBaeume.depGraph.get_by_address(1)['semrep']
        semRepPat = r'\x. grün(x)'
        semSig = {'grün': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testEin(self):
        assigned = GrueneAlteBaeume.depGraph.get_by_address(2)['semrep']
        semRepPat = r'\P Q. all x. (P(x) -> Q(x))'
        semSig = {'P': '<e,t>', 'Q': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testHund(self):
        assigned = GrueneAlteBaeume.depGraph.get_by_address(3)['semrep']
        semRepPat = r'\x. hund(x)'
        semSig = {'hund': '<e,t>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testBeisst(self):
        assigned = GrueneAlteBaeume.depGraph.get_by_address(4)['semrep']
        semRepPat = r'\y x. beißen(x,y)'
        semSig = {'beißen': '<e,<e,t>>'}
        expected = tlp.parse(semRepPat, signature=semSig)
        self.assertEqual(assigned, expected)

    def testPeter(self):
        assigned = GrueneAlteBaeume.depGraph.get_by_address(5)['semrep']
        semRepPat = r'peter'
        semSig = {'peter': 'e'}
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
