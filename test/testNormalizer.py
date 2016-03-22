#!/usr/bin/env python3
# -*- coding: utf-8

import unittest
import sys
import os
import inspect

from context import montesniere

class TanzendeGurken(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        conllFile = os.path.join(TEST_DIR, 'tanzende_gurken.conll')
        with open(conllFile) as f:
            cls.normalized = montesniere.normalize.Normalizer(f.read())
        
    def testgetNormalizedSentence(self):
        normalized = TanzendeGurken.normalized.getSentence()
        resultsFile= os.path.join(
                            TEST_DIR, 
                            'normalizedTanzendeGurken.conll'
                            )
        expected = open(os.path.join(resultsFile)).read()
        self.assertEqual(normalized, expected)
  
class TanzendeGurkenPronomen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        conllFile = os.path.join(TEST_DIR, 'tanzende_gurken2.conll')
        with open(conllFile) as f:
            cls.normalized = montesniere.normalize.Normalizer(f.read())
        
    def testgetNormalizedSentence(self):
        normalized = TanzendeGurkenPronomen.normalized.getSentence()
        resultsFile= os.path.join(
                            TEST_DIR, 
                            'normalizedTanzendeGurken2.conll'
                            )
        expected = open(os.path.join(resultsFile)).read()
        self.assertEqual(normalized, expected)
        
class SchenkenderHase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        conllFile = os.path.join(TEST_DIR, 'schenkender_hasen.conll')
        with open(conllFile) as f:
            cls.normalized = montesniere.normalize.Normalizer(f.read())
            
    def testNormalized(self):
        normalized = SchenkenderHase.normalized.getSentence()
        results = os.path.join(TEST_DIR, 'normalizedSchenkenderHase.conll')
        expected = open(os.path.join(results)).read()
        self.assertEqual(expected, normalized)

# fail, coordination in PP
class Presidents(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        conllFile = os.path.join(TEST_DIR, 'presidents.conll')
        with open(conllFile) as f:
            cls.normalized = montesniere.normalize.Normalizer(f.read())
            
    def testNormalized(self):
        normalized = Presidents.normalized.getSentence()
        results = os.path.join(TEST_DIR, 'normalizedPresidents.conll')
        expected = open(os.path.join(results)).read()
        self.assertEqual(expected, normalized) 

class NurPronomen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        conllFile = os.path.join(TEST_DIR, 'nur_pronomen.conll')
        with open(conllFile) as f:
            cls.normalized = montesniere.normalize.Normalizer(f.read())
            
    def testNormalized(self):
        normalized = NurPronomen.normalized.getSentence()
        results = os.path.join(TEST_DIR, 'normalizedNurPronomen.conll')
        expected = open(os.path.join(results)).read()
        self.assertEqual(expected, normalized) 

if __name__ == '__main__':
    global TEST_DIR
    pathToHere = inspect.getfile(inspect.currentframe())
    pathToTop = os.path.dirname(os.path.dirname(pathToHere))
    TEST_DIR = os.path.join(pathToTop, 'test/conll/')

    unittest.main()
