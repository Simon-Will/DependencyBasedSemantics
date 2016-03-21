#!/usr/bin/env python3
# -*- coding: utf-8

import copy
import itertools

from nltk.grammar import DependencyGrammar
import nltk.parse as nlp
import nltk.sem.logic as nll

class SemMerger:
    ''' Combines the logical expressions of each node and returns
    al logical expression of the entire sentence.
    A SemMerger object consitst of a dependencygraph, that will be 
    updated continously.
    For each node, its own original logical expression is combined
    with those of its children and updated accordingly.
    Attributes:
        dg: a nltk.parse.dependencygraph.DependencyGraph 
            object with logical expression assigned to each node.
        dependencies: a list of nodes being currenlty processed
    '''
        
    def __init__(self, depGraph):
        '''Initializes SemMerger with given values. 
        dependencyGraph has to be an preprocessed DependencyGraph object
        with each node having a logical expression (semrep)
        An ordinary DependencyGraph will not lead to a sensible result.
        Args:
            depedencyGraph: a nltk.parse.dependencygraph.DependencyGraph 
                that has been preprocessed by a SemRepAssigner object
        Returns:
            the initialized SemMerger object
        Raises:
            TypeError: dg is not a DependencyGraph object
        '''
        self.dg = depGraph
        self.root = self.getRoot()
        self.dependencies = []
        # check type
        if isinstance(self.dg, nlp.dependencygraph.DependencyGraph):
            pass

        else:
            raise TypeError('argument must be a dependencygraph')
            

    def mergeWithChildren(self, node, force=False):
        """Merge the semrep of a node with the ones of its children.

        Args:
            node: A node of a dependencyGraph object.
            force: A bool denoting if a merge should be forced, even if node
                was merged already.
        """
        if self.isMerged(node) and not force:
            # The node was already merged and a new merge will not be forced.
            sys.stderr.write('The node was merged already')
            return None

        # Collect the children from self.dg.
        children = self.getChildren(node)

        if len(children) == 0:
            # If a node has no children, there is nothing to merge.
            try:
                node['mergedsemrep'] = node['semrep']
            except KeyError:
                pass

        else:
            # Merge the children with their children first.
            for c in children:
                if not self.isMerged(c):
                    self.mergeWithChildren(c, force)

            # Now actually merge the node with its children.
            mergeDict = {node['address']: node['semrep']}
            mergeDict.update(
                    {c['address']: c['mergedsemrep'] for c in children
                        if 'mergedsemrep' in c})

            if self.doubleNamed(node, c):
                node['mergedsemrep'] = self.doubleNamedEntity(node, c)
            else:    
                node['mergedsemrep'] = self._merge(mergeDict)

        # Mark node as merged and return.
        node['merged'] = True

    def _merge(self, mergeDict):
        """Merge the lambda expressions in mergeDict.
        
        Args:
            mergeDict: A dictionary mapping any keys to
                nltk.sem.logic.LambdaExpression objects.
        
        Returns:
            The Expression resulting from the merges.

        Raises:
            NoMergePossibleException if the types of the expressions
                do not allow a merge.
        """
        # Don't change values of original dict. (Emulation of pass by value)
        mergeDict = copy.deepcopy(mergeDict)

        if len(mergeDict) == 1:
            return list(mergeDict.values())[0]
        else:
            applicationTries = _generateApplicationTries(mergeDict.keys())
            for t in applicationTries:
                expr0, expr1 = mergeDict[t[0]], mergeDict[t[1]]
                if isApplicableTo(expr0, expr1):
                    firstMerge = expr0.applyto(expr1)
                    newMergeDict = {
                            k:v for k,v in mergeDict.items()
                            if k != t[0] and k != t[1]
                            }
                    newMergeDict[t] = firstMerge
                    try:
                        merged = self._merge(newMergeDict).simplify()
                    except NoMergePossibleException:
                        continue
                    return merged
            else:
                errMsg = "Could not merge the following types:"
                for v in mergeDict.values():
                    errMsg = "{0}\n{1}".format(errMsg, v)
                raise NoMergePossibleException(errMsg)

    def isMerged(self, node):
        """Check if a node's semrep has been merged with its children."""
        try:
            merged = True if node['merged'] is True else False
        except KeyError:
            # If the node has no key called 'merged', treat is as False.
            merged = False
        return merged
        
        
    def doubleNamed(self, node, child):
        return (node['tag'] == 'NE' and 
                (child['tag'] == 'NE' and child['rel'] == 'PNC'))

    def doubleNamedEntity(self, head_node, node):
        tlp = nll.LogicParser(type_check=True)
        '''Fuse representations of first and last name of one entity 
            into one
            
        Args:
            head_node   :   last name of NE
            node        :   first name of NE
        Returns:
            fused expression
        '''
        self.dependencies.append(head_node['address'])
        head_node['lemma'] = node['lemma'] + "_" + head_node['lemma']
        
        # new representation: subject
        if (head_node['rel'] == 'SB'):
            rule = r'\P. P({[lemma]})'
            sig = {'P':'<e,t>', 'lemma':'e'}
            
        # new representation: object
        else:
            rule = r'{[lemma]}'
            sig = {'{[lemma]}' : 'e'}
            
        new_expr = rule.format(head_node)
        exprSig = {key.format(head_node): val for key, val in sig.items()}
        return tlp.parse(new_expr, signature=exprSig)
    
    def getSemantics(self):
        ''' returns logical expression of the entire sentence '''
        #self.getDependencies()
        #return self.getSemRepresentation()
        self.mergeWithChildren(self.root)
        return self.root['mergedsemrep']

    def getChildren(self, node):
        """Get the child nodes of a node.

        The addresses of the children are found under the 'deps' key in the
        dict of the dependencyGraph self.dg.

        Args:
            node: A dict corresponding to a node in self.dg.

        Returns:
            A list of dicts corresponding to the child nodes.
        """
        deps = node['deps']
        children = []
        for child_list in deps.values():
            children.extend([self.dg.nodes[c] for c in child_list])
        return children

    def getRoot(self):
        '''Get the root node of the dependencyGraph.
        
        Returns:
            The root node of the dependencyGraph self.dg.

        Raises:
            ValueError if self.dg has less than or more than one root node.
        '''
        roots = self.getChildren(self.dg.nodes[0])

        if len(roots) == 1:
            return roots[0]
        elif len(roots) > 1:
            errMsg = 'The dependencyGraph has more than one root.'
            raise ValueError(errMsg)
        else:
            errMsg = 'The dependencyGraph has no root.'
            raise ValueError(errMsg)

def _generateApplicationTries(iterable):
    for i in itertools.combinations(iterable, 2):
        yield i
        yield tuple(reversed(i))

class NoMergePossibleException(Exception):
    pass

def isApplicableTo(expr1, expr2, strict=False):
    '''Test whether expr1 can be applied to expr2.

    Args:
        expr1: An nltk.sem.logic.Expression object with resolved type.
        expr2: An nltk.sem.logic.Expression object with resolved type.

    Returns:
        True if expr1 can be applied to expr2; False otherwise.
    '''
    if not isinstance(expr1.type, nll.ComplexType):
        return False

    elif expr1.type.first == expr2.type:
        return True
    
    elif (not strict) and expr1.type.first.matches(expr2.type):
        print("Warning: Type is not definite, application may be incorrect!")
        return True
    
    return False


def applyCorrectly(expr1, expr2):
    '''Try to correctly apply one expression to the other.

    Args:
        expr1: An nltk.sem.logic.Expression object with resolved type.
        expr2: An nltk.sem.logic.Expression object with resolved type.

    Returns:
        An nltk.sem.logic.Expression object resulting from the
            application of one expression to the other.

    Raises:
        nltk.sem.logic.TypeResolutionException if none of the
            expressions can be applied to the other.
    ''' 
    if isApplicableTo(expr1, expr2):
        return expr1.applyto(expr2).simplify()
    elif isApplicableTo(expr2, expr1):
        return expr2.applyto(expr1).simplify()
    else:
        # either deps are wrong or types are not accurate
        errMsg = 'The types {0} and {1} are incompatible.'
        raise nll.TypeException(errMsg.format(expr1, expr2))
    
def testUsualCase():
    import nltk.sem.logic as nll
    tlp = nll.LogicParser()
    read_expr = tlp.parse
    treebank_data = open('../test/conll/beissende_taube.conll').read()
    dg = nlp.DependencyGraph(treebank_data)
    #this will soon be replaced by an automatic representation
    dg.nodes[1]['semrep'] = read_expr(r'\P\Q. exists x.(P(x) & Q(x))')
    dg.nodes[2]['semrep'] = read_expr(r'\x. taube(x)')
    dg.nodes[3]['semrep'] = read_expr(r'\y\x. beissen(x, y)')
    dg.nodes[4]['semrep'] = read_expr(r'peter')
   # dg.nodes[5]['semrep'] = read_expr(r'mueller')
    semantics = SemMerger(dg)
    return semantics.getSemantics()
    
def test():
    return testUsualCase()
    
if __name__ == '__main__':
    print(test())
