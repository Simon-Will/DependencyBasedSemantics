#!/usr/bin/env python3
# -*- codung: utf-8 -*-

import montesniere
import sys
import nltk.parse as nlp

def getExpression(conllFile):
    """runs entire algorithm and returns logical expression"""
    with open(conllFile) as f:
        depGraph = nlp.DependencyGraph(f.read())
    assigner = montesniere.assign.SemRepAssigner.fromfile("rules/heuristic_rules.json")
    assigner.assignToDependencyGraph(depGraph)
    merger = montesniere.merge.SemMerger(depGraph)
    return merger.getSemantics()


if __name__ == '__main__':
    print(getExpression(sys.argv[1]))
