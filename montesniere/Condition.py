#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Functionality for conditions applicable to DependencyGraph nodes."""

import re

def makeElementFixedObj(obj):
    """
    >>> alphabet = {chr(n) for n in range(0x61, 0x61 + 26)}
    >>> inAlphabet = makeElementFixedObj(alphabet)
    >>> inAlphabet('s')
    True
    >>> inAlphabet('%')
    False
    """
    def elementFixedObj(subj):
        return subj in obj
    return elementFixedObj

def makeSubsetFixedObj(obj):
    """
    >>> alphabet = {chr(n) for n in range(0x61, 0x61 + 26)}
    >>> abc = {'a', 'b', 'c'}
    >>> subAlphabet = makeSubsetFixedObj(alphabet)
    >>> subAlphabet(abc)
    True
    >>> subAlphabet({'%'})
    False
    """
    def subsetFixedObj(subj):
        return subj.issubset(obj)
    return subsetFixedObj

def makeSupersetFixedObj(obj):
    """
    >>> alphabet = {chr(n) for n in range(0x61, 0x61 + 26)}
    >>> abc = {'a', 'b', 'c'}
    >>> lowerAlphanumeric = alphabet.union({str(i) for i in range(0,10)})
    >>> superAlphabet = makeSupersetFixedObj(alphabet)
    >>> superAlphabet(lowerAlphanumeric)
    True
    >>> superAlphabet(abc)
    False
    """
    def supersetFixedObj(subj):
        return subj.issuperset(obj)
    return supersetFixedObj

def makeNotElementFixedObj(obj):
    def notElementFixedObj(subj):
        return subj not in obj
    return notElementFixedObj

def makeNotSubsetFixedObj(obj):
    def notSubsetFixedObj(subj):
        return not subj.issubset(obj)
    return notSubsetFixedObj

def makeNotSupersetFixedObj(obj):
    def notSupersetFixedObj(subj):
        return not subj.issuperset(obj)
    return notSupersetFixedObj

class Condition():
    """A condition for nodes of an nltk.parse.DependencyGraph.

    A Condition object represents a condition that can be satisfied or
    not satisfied for each node in an nltk.parse.DependencyGraph object.

    Each condition at least consists of a subject, a relation and an
    object. The subject is a key in the dictionary of each node in the
    DependencyGraph. Typical examples are 'tag', 'deps' or 'lemma'.
    The object is a set of strings. The relation is 

    Attributes:
        subj: A string that is a key in a dictionary corresponding to a
            node of a DependencyGraph. 
        rel: A string that is a key in Condition.relationDict.
        obj: A set of strings that can occur as values in a dictionary
            corresponding to a node of a DependencyGraph.
        transeunda: A set of strings that can occur as values of a
            dictionary corresponding to a node of a DependencyGraph when
            accessed at the 'rel' key. Typically {'NK'} or other
            dependency tags.
        relationFixedObj: A unary function that already incorporates the
            attribute obj. Applied to a subject, it evaluates to True or
            False, depending on the function and the fixed object.
    """
    # TODO: Describe better what transeunda are used for.

    # Regular expression for the condition
    conditionPat = re.compile(r"""
            \s*                         # leading whitespace
            (?:                         # optional part for negation
                (?P<neg>!)              # negation string (exclamation mark)
                \s+                     # separating whitespace
            )?                          # end of optional part
            (?P<subj>\S+)               # subject string
            \s+                         # separating whitespace
            (?P<rel>[^^]+)              # relation string
            (?:                         # optional part for transeunda
                \^                      # separating circumflex
                (?P<transeunda>{[^}]+}) # transeunda string
            )?                          # end of optional part
            \s+                         # separating whitespace
            (?P<obj>{[^}]+})            # object string
            \s*                         # trailing whitespace
            """, re.VERBOSE)

    # This dictionary maps the relation specified in the string representation
    # of a condition (conditionString) to the factory functions producing a
    # version of the relation with a fixed object.
    relationDict = {
            'element': makeElementFixedObj,
            'notElement': makeNotElementFixedObj,
            'subset': makeSubsetFixedObj,
            'notSubset': makeNotSubsetFixedObj,
            'superset': makeSupersetFixedObj,
            'notSuperset': makeNotSupersetFixedObj,
            }

    def __init__(self, subj, rel, obj, transeunda=frozenset(), negated=False):
        """Initialize Condition with the given values.

        Args:
            subj: A string that is a key in a dictionary corresponding
                to a node of a DependencyGraph. 
            rel: A string that is a key in Condition.relationDict.
            obj: A set of strings that can occur as values in a
                dictionary corresponding to a node of a DependencyGraph.
            transeunda: A set of strings that can occur as values of a
                dictionary corresponding to a node of a DependencyGraph
                when accessed at the 'rel' key. Typically {'NK'} or
                other dependency tags.

        Returns:
            The initialized SemRepRule.
        """
        self.subj = subj
        self.rel = rel
        self.obj = obj
        self.transeunda = transeunda
        self.negated = negated
        objFixer = Condition.relationDict[self.rel]
        self.relationFixedObj = objFixer(self.obj)

    @classmethod
    def fromstring(cls, conditionString):
        """Initialize Condition from a string.

        Args:
            conditionString: A string representing a condition.

        Returns:
            The initialized SemRepRule.
        """
        negated, subj, rel, transeunda, obj = Condition.readConditionString(
                conditionString)
        return cls(subj, rel, obj, transeunda, negated)

    def __str__(self):
        return '{0.subj} {0.rel}^{0.transeunda} {0.obj}'.format(self)
    
    def __call__(self, depGraph, address):
        """Test if a node of a DependencyGraph satisfies this condition.

        Args:
            depGraph: An nltk.parse.DependencyGraph object.
            address: An integer denoting the address of a node in the
                depGraph
        Returns:
            True, if the condition is satisfied; False otherwise.
        """
        # XXX: The logic of this function is a little obscure. Maybe it should
        # be rewritten.
        node = depGraph.get_by_address(address)
        subj = node[self.subj]
        satisfied = self._testSubj(subj)
        while node['rel'] in self.transeunda:
            node = depGraph.get_by_address(node['head'])
            subj = node[self.subj]
            satisfied = satisfied or self._testSubj(subj)
            if not satisfied:
                return False
        if self.negated:
            return not satisfied
        else:
            return satisfied
            
    def _testSubj(self, subj):
        """Test if a set satisfies the condition.

        Args:
            subj: A set of strings or a dict whose keys are strings.

        Returns:
            True if the condition is satisfied; False otherwise.
        """
        if isinstance(subj, dict):
            return self.relationFixedObj(set(subj.keys()))
        else:
            return self.relationFixedObj(subj)

    @staticmethod
    def readConditionString(conditionString):
        """Construct Condition attributes from a string.

        Args:
            conditionString: A string representing a condition.

        Returns:
            A quadruple containing subj (str), rel (str),
                transeunda (set of str) and obj (set of str).
            
        Raises:
            ValueError if the conditionString is invalid.

        >>> cs = 'deps superset {SB}'
        >>> Condition.readConditionString(cs)
        (False, 'deps', 'superset', set(), {'SB'})
        >>> cs2 = 'rel element^{NK} {SB, OA}'
        >>> Condition.readConditionString(cs2)[0:-1]
        (False, 'rel', 'element', {'NK'})
        >>> sorted(Condition.readConditionString(cs2)[-1])
        ['OA', 'SB']
        >>> cs3 = '! deps subset {DA}'
        >>> Condition.readConditionString(cs3)
        (True, 'deps', 'subset', set(), {'DA'})
        """
        negated, subj, rel, transeunda, obj = (False, '', '', set(), set())
        match = Condition.conditionPat.match(conditionString)
        if match:
            subj = match.group('subj')
            obj = buildSet(match.group('obj'))
            rel = match.group('rel')
            if match.group('transeunda'):
                transeunda = buildSet(match.group('transeunda'))
            if match.group('neg') == '!':
                negated = True
        else:
            errMsg = '{} is not a valid conditionString.'
            raise ValueError(errMsg.format(conditionString))
        return negated, subj, rel, transeunda, obj

def buildSet(setString):
    """Build a set of strings from a string representation of a set.

    Args:
        setString: A string representing a set. The members of the set
            should not be surrounded by quotes.

    Returns:
        A set of strings.

    >>> sorted(buildSet('{foo, bar, baz}'))
    ['bar', 'baz', 'foo']
    >>> buildSet('{}')
    set()
    >>> buildSet('[not, a, set]')
    Traceback (most recent call last):
        ...
    ValueError: setString '[not, a, set]' does not represent a set.
    """
    setString = setString.strip()
    s = {}
    if setString.startswith('{') and setString.endswith('}'):
        setString = setString[1:-1].strip()
        if setString:
            s = set(re.split(r'\s*,\s*', setString))
        else:
            return set()
    else:
        errMsg = "setString '{}' does not represent a set."
        raise ValueError(errMsg.format(setString))
    return s
    
def test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    test()
