#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

import nltk.sem.logic as nll

from .Condition import Condition

tlp = nll.LogicParser(type_check=True)

class SemRepRule:
    """A rule assigning a semantic representation if conditions are met.

    A SemRepRule object consists of conditions that can be applied to
    the nodes in a nltk.parse.DependencyGraph object. For each node,
    each condition can be met (True) or not met (False) for each node.

    If the conditions are met, then the node should be assigned the
    semantic representation using the semRepPat.

    Attributes:
        conditions: A list of Condition objects.
        semRepPat: A string holding a template for a semantic
            representation. It can be formatted using the .format
            method with the correct node as an argument.
        semSig: A dictionary mapping expressions from the semRepPat to
            a string representation of their types.
    """

    def __init__(self, conditions, semRepPat, semSig):
        """Initialize SemRepRule with the given values.

        conditions can be a list of Condition objects that is then
        used as the attribute self.semRepPat or it can be a list of
        strings that can be used to construct Condition objects. It
        cannot be a mix of both.
        
        Args:
            conditions: A list of Condition objects or strings that can
                be used to initialize Condition objects.
            semRepPat: A string holding a template for a semantic
                representation.
            semSig: A dictionary mapping expressions from the semRepPat
                to a string representation of their types.

        Returns:
            The initialized SemRepRule.

        Raises:
            TypeError: conditions is not a list of str or Condition.
        """
        self.semRepPat = semRepPat
        self.semSig = semSig
        self.conditions = []
        if len(conditions) > 0:
            if isinstance(conditions[0], Condition):
                self.conditions = conditions
            elif isinstance(conditions[0], str):
                self.conditions = [
                        Condition.fromstring(c) for c in conditions
                        ]
            else:
                raise TypeError(
                        'conditions is not a list of str or Condition objects')

    @classmethod
    def fromstring(cls, s):
        """Read a SemRepRule from a string and return it."""
        # TODO: Implement this.
        pass

    def testConditions(self, depGraph, address):
        """Test if a node satisfies all conditions of this SemRepRule.

        Args:
            depGraph: An nltk.parse.DependencyGraph object.
            address: An integer denoting the address of a node in the
                depGraph
        Returns:
            True, if all conditions are satisfied.
            False, if one or more conditions are not satisfied.
        """
        for cond in self.conditions:
            if not cond(depGraph, address):
                # One condition is not satisfied.
                return False
        else:
            # All conditions are satisfied.
            return True

    def assignSemRep(self, node):
        """Assign the semantic representation of this rule to a node.

        Format this rule's semRepPat with the given node, do the same
        with the expressions in this rule's semSig. Then parse the
        formatted semRepPat into a logic expression using the formatted
        semSig as a signature. Add the resulting logic representation to
        the node's dictionary under the new key 'semrep'.

        Args:
            node: A node of an nltk.parse.DependencyGraph object.
        """
        expr = self.semRepPat.format(node)
        exprSig = {key.format(node): val for key, val in self.semSig.items()}
        node['semrep'] = tlp.parse(expr, signature=exprSig)

    def __str__(self):
        s = '<SemRepRule: conditions={0.conditions}, semRepPat={0.semRepPat}>'
        return s.format(self)

class SemRepAssigner:
    """An object assigning semantic representations to sentences.

    A SemRepAssigner can assign semantic representations to nodes of an
    nltk.parse.DependencyGraph object. Foundation for the decision on a
    representation is the list of rules.

    Attributes:
        rules: A list of SemRepRule objects.
    """

    def __init__(self, rules):
        """Initialize SemRepAssigner with the given rules.

        The rules should be a sorted iterable, e. g. a list.

        Args:
            rules: A list of SemRepRule objects.

        Returns:
            The initialized SemRepAssigner.
        """
        self.rules = rules

    @classmethod
    def fromfile(cls, filename):
        """Read a SemRepAssigner from a json file and return it.

        The json file has to hold an array of objects (the rules).
        The rules have to contain three keys: 'condition', 'semRepPat'
        and 'semSig'. The value of the 'conditions' key has to be an
        array of strings, each denoting one condition. The value of 
        'semRepPat' has to be a string holding a semRepPat meeting the
        requirements imposed by SemRepRule. The value of 'semSig' has to
        be an object (i. e. a python dict) meeting the requirements
        imposed by SemRepRule.
        
        Args:
            filename: The name of json file.

        Returns:
            A SemRepAssigner object with the rules from the json file.
        Raises:
            ValueError if filename does not denote a valid json file.
        """
        with open(filename) as f:
            try:
                json_rules = json.load(f)
            except ValueError:
                raise
        rules = [SemRepRule(r['conditions'], r['semRepPat'], r['semSig'])
                for r in json_rules]
        return cls(rules)

    def assignToDependencyGraph(self, depGraph):
        """Assign semantic representations to DependencyGraph nodes.

        The dictionaries corresponding to the nodes in the depGraph are
        extended with a 'semrep' key under which the representation is
        stored.

        Args:
            depGraph: An nltk.parse.DependencyGraph object.
        """
        for address in depGraph.nodes:
            self.assignToNode(depGraph, address)
    
    def assignToNode(self, depGraph, address):
        """Assign a semantic representation to a DependencyGraph node.

        Args:
            depGraph: An nltk.parse.DependencyGraph object.
            address: An integer denoting a node in the depGraph.
        """
        for r in self.rules:
            if r.testConditions(depGraph, address):
                r.assignSemRep(depGraph.get_by_address(address))
                break
        else:
            # No rule's conditions are satisfied.
            # Assign default semrep here.
            pass

def test():

    import nltk.parse as nlp
    rules = [
            SemRepRule(
                [
                    r'tag element {NE}',
                    r'rel element {SB}'
                ],
                r'\P. P({[lemma]})',
                {'P':'<e,t>', '{[lemma]}':'e'}
                ),
            SemRepRule(
                [
                    r'tag element {NE}',
                    r'rel notElement^{NK} {SB}'
                ],
                r'{[lemma]}',
                {'{[lemma]}':'e'}
                ),
            SemRepRule(
                [
                    r'tag element {NN}'
                ],
                r'\x. {[lemma]}(x)',
                {'{[lemma]}':'<e,t>'}
                ),
            SemRepRule(
                [
                    r'tag element {ART}',
                    r'lemma element {ein}',
                    r'rel element^{NK} {SB}'
                ],
                r'\P Q. exists x. (P(x) & Q(x))',
                {'P':'<e,t>', 'Q':'<e,t>'}
                ),
            SemRepRule(
                [
                    r'tag element {VVFIN}',
                    r'deps superset {SB}',
                    r'deps notSuperset {OA}'
                ],
                r'\x. {[lemma]}(x)',
                {'{[lemma]}':'<e,t>'}
                ),
            SemRepRule(
                [
                    r'tag element {VVFIN}',
                    r'deps superset {SB, OA}',
                    r'deps notSuperset {OD}'
                ],
                r'\x y. {[lemma]}(y,x)',
                {'{[lemma]}':'<e,<e,t>>'}
                ),
            SemRepRule(
                [
                    r'tag element {VVFIN}',
                    r'deps superset {SB, OA, OD}'
                ],
                r'\x y z. {[lemma]}(z,y,x)',
                {'{[lemma]}':'<e,<e,<e,t>>>'}
                )
            ]

    sTaube = open('../test/beissende_taube.conll').read()
    dgTaube = nlp.DependencyGraph(sTaube)
    beissen = dgTaube.nodes[3]
    #for rule in rules:
    #    print(rule)
    #    print(rule.testConditions(dgTaube, 1))
    #    print("---")
    print(dgTaube)
    ass = SemRepAssigner(rules)
    ass.assignToDependencyGraph(dgTaube)
    print(dgTaube)
    print(dgTaube.get_by_address(3)['semrep'].type)
    print(dgTaube.get_by_address(2)['semrep'].type)

if __name__ == '__main__':
    test()
