#!/usr/bin/env python3
# -*- coding: utf-8

from nltk.grammar import DependencyGrammar
import nltk.parse as nlp
import nltk.sem.logic as nll

class SemMerger:
    """ Combines the logical expressions of each node and returns
        al logical expression of the entire sentence.
        A SemMerger object consitst of a dependencygraph, that will be 
        updated continously.
        For each node, its own original logical expression is combined
        with those of its children and updated accordingly.
        Attributes:
            dg: a nltk.parse.dependencygraph.DependencyGraph 
                object with logical expression assigned to each node.
            dependencies: a list of nodes being currenlty processed
        """
        
    def __init__(self, dependencyGraph):
        """Initializes SemMerger with given values. 
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
        """
        self.dg = dependencyGraph
        self.dependencies = []
        # check type
        if isinstance(self.dg, nlp.dependencygraph.DependencyGraph):
            pass

        else:
            raise TypeError('argument must be a dependencygraph')
            
        
    def getDependencies(self):
        """
        find bottom of depedencytree and store those nodes in 
        self.dependencies
        """
        for node in self.dg.nodes:
            
            if self.dg.nodes[node]['deps'] == {}:
                self.dependencies.append(node)
        
    def getSemRepresentation(self):
        """ return logical expression of the entire sentence"""
        for node in self.dependencies:
            self.sortSemantics(node)
        return self.dg.nodes[self.dg.nodes[0]['deps']['ROOT'][0]]['semrep']
            
            
    def sortSemantics(self, node):
        """gives each node the correct logical expression"""
        self.dependencies.remove(node)
        head = self.dg.nodes[node]['head']
        
        # stops the loop once the top of the tree has been reached
        if self.dg.nodes[node]['address'] == 0:
            return
        
        self.dg.nodes[head]['semrep'] = self.mergeSemantics(
                                            self.dg.nodes[head],
                                            self.dg.nodes[node]
                                            )
                                            
        if self.dg.nodes[head]['address'] != None:
            self.dependencies.append(self.dg.nodes[head]['address'])
        
        # starts not quite a loop
        self.getSemRepresentation()
    
    def mergeSemantics(self, semhead, semdep):
        """merges logical expressions"""
        # store final logical expression in Top-Node
        if semhead['address'] == 0:
            return semdep['semrep']
            
        # better solution woulb be truly appreciated!
        # FIXME: This needs to pay attention to types.
        try:
            if semdep['rel'] == 'SB' or semdep['rel'] == 'NK':
                return semdep['semrep'].applyto(semhead['semrep']).simplify()
        
            else:
                return semhead['semrep'].applyto(semdep['semrep']).simplify()
        # Proposed 'better solution':
        #    applyCorrectly(semhead['semrep'], semdep['semrep'])
        
        except KeyError:
            #in case of no logical representation
            return semhead['semrep']
    
    def getSemantics(self):
        """ returns logical expression of the entire sentence """
        self.getDependencies()
        return self.getSemRepresentation()
    
def isApplicableTo(expr1, expr2):
    """Test whether expr1 can be applied to expr2.
    
    Args:
        expr1: An nltk.sem.logic.Expression object with resolved type.
        expr2: An nltk.sem.logic.Expression object with resolved type.

    Returns:
        True if expr1 can be applied to expr2; False otherwise.
    """
    return expr1.type.first == expr2.type

def applyCorrectly(expr1, expr2):
    """Try to correctly apply one expression to the other.

    Args:
        expr1: An nltk.sem.logic.Expression object with resolved type.
        expr2: An nltk.sem.logic.Expression object with resolved type.

    Returns:
        An nltk.sem.logic.Expression object resulting from the
            application of one expression to the other.

    Raises:
        nltk.sem.logic.TypeResolutionException if none of the
            expressions can be applied to the other.
    """
    if isApplicableTo(expr1, expr2):
        return expr1.applyto(expr2).simplify()
    elif isApplicableTo(expr2, expr1):
        return expr2.applyto(expr1).simplify()
    else:
        # Raising TypeResolutionException may not be the correct choice,
        # because we're trying to apply both ways, not only expr1 to expr2.
        # Maybe a generic nltk.sem.logic.TypeException with a descriptive error
        # message should be raised.
        raise nll.TypeResolutionException(expr1, expr2)

def testUsualCase():
    import nltk.sem.logic as nll
    tlk = nll.LogicParser()
    read_expr = tlk.parse

    treebank_data = open('../test/beissende_taube.conll').read()
    dg = nlp.DependencyGraph(treebank_data)
    # this will soon be replaced by an automatic representation
    dg.nodes[1]['semrep'] = read_expr(r'\P\Q. exists x. (P(x) & Q(x))')
    dg.nodes[2]['semrep'] = read_expr(r'\x. taube(x)')
    dg.nodes[3]['semrep'] = read_expr(r'\y\x. beissen(x, y)')
    dg.nodes[4]['semrep'] = read_expr(r'peter')
    semantics = SemMerger(dg)
    return semantics.getSemantics()
    
if __name__ == '__main__':
    print(testUsualCase())
