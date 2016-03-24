#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from collections import defaultdict
from functools import reduce

import xml.etree.ElementTree as ET
import nltk.parse as nlp
import nltk

from context import montesniere

class Sentence:

    def __init__(self, sentence, idx, conll=None, expr=None):
        self.sentence = sentence
        self.idx = idx
        self.conll = conll
        self.expr = expr
        self.dg = None
        if self.conll:
            self.dg = nlp.DependencyGraph(self.conll)

    def getExpr(self, assigner):
        try:
            assigner.assignToDependencyGraph(self.dg)
        except nltk.sem.logic.InconsistentTypeHierarchyException:
            self.expr = None
            return

        merger = montesniere.merge.SemMerger(self.dg)
        try:
            self.expr = merger.getSemantics()
        except montesniere.merge.NoMergePossibleException:
            self.expr = None

    def __str__(self):
        return self.sentence

    def __repr__(self):
        return str(self)

def getPremises(prob):
    premises = [Sentence(p.text.strip(), p.get('idx')) for p in prob.iter('p')]

    for conll in prob.iter('p_conll'):
        for p in premises:
            if p.idx == conll.get('idx'):
                p.conll = conll.text.strip()
                p.dg = nlp.DependencyGraph(p.conll)

    return premises

def getHypothesis(prob):
    h = prob.find('h')
    hypothesis = Sentence(h.text.strip(),
            h.get('idx'),
            prob.find('h_conll').text.strip())
    return hypothesis

def formatPremises(premises):
    if len(premises) == 1:
        return '"{}"'.format(premises[0])
    else:
        return reduce(
                lambda p1,p2:'"{}", "{}"'.format(p1, p2),
                premises)

def main():
    # Configure argparse.
    d = 'Test problems in fraces testsuite.'
    parser = argparse.ArgumentParser(description=d)

    parser.add_argument('rulesFile',
            help='''The json file containing the rules for the montesniere
            SemRepAssigner''')

    parser.add_argument('fracasFile',
            help='The xml file containing the fracas problems.')

    parser.add_argument('-v', '--verbose',
            action='store_true', default=False,
            help='Print result for every fracas problem.')

    args = parser.parse_args()

    assigner = montesniere.assign.SemRepAssigner.fromfile(
            args.rulesFile, ascii=True)
    prover = nltk.Prover9()
    fracas = ET.fromstring(open(args.fracasFile).read())

    results = []
    answerDict = defaultdict(lambda: False, {'yes': True, 'no': False})

    # Test each problem
    for prob in fracas.iter('problem'):
        # Get premises, hypothesis, fracas answer and problem id.
        id = prob.get('id')
        answer = prob.get('fracas_answer')
        premises = getPremises(prob)
        hypothesis = getHypothesis(prob)

        # Assign semantic expressions.
        for p in premises:
            p.getExpr(assigner)
        hypothesis.getExpr(assigner)

        # Check if hypothesis follows from premises.
        if None in [p.expr for p in premises]:
            result = None
            failReasonPat1 = 'For one or more premise of problem {}, no '
            failReasonPat2 = 'semantic representation could be constructed.'
            failReason = (failReasonPat1 + failReasonPat2).format(id)
        elif hypothesis.expr is None:
            result = None
            failReason1 = 'For the hypothesis of problem {}, no semantic '
            failReason2 = 'representation could be constructed.'
            failReason = (failReason1 + failReason2).format(id)
        else:
            try:
                result = prover.prove(
                        hypothesis.expr,
                        [p.expr for p in premises])
            except nltk.inference.prover9.Prover9FatalException as e:
                result = None
                failReasonPat1 = 'Prover9 failed at problem {0} with the '
                failReasonPat2 = 'message:{1}\n'
                failReason = (failReasonPat1 + failReasonPat2).format(id, e)

        if result is None:
            successful = False
        else:
            successful = answerDict[answer] == result
        results.append((id, successful))

        # Print verbose info.
        if args.verbose:

            if result:
                resultString = 'is said to follow' if result\
                        else 'is said not to follow'

                hypothesisString = '"{}"'.format(hypothesis.sentence)
                premisesString = formatPremises(premises)

                msgPat = 'The hypothesis {0} {1} from the premises {2}.'
                msg = msgPat.format(
                    hypothesisString,
                    resultString,
                    premisesString)
            else:
                msg = failReason

            successfulString = 'OK' if successful else 'FAILED'
            print(msg)
            print(successfulString)
            print()

    # Print summary.
    unsuccessful = [r[0] for r in results if not r[1]]
    summaryPat = '{0} out of {1} failed.\nIDs of failed tests: {2}'
    print(summaryPat.format(
        len(unsuccessful),
        len(results),
        reduce(lambda i,j: '{}, {}'.format(i,j), unsuccessful)))

if __name__ == '__main__':
    main()
