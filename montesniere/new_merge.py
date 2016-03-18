#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nltk.grammar import DependencyGrammar
import nltk.parse as nlp
import nltk.sem.logic as nll

class SemMerger:
    '''Combines logical expressions of each node and returns logical 
    expression of entire sentence.
    
    A SemMerger object consists of dependencygraph, which is updated 
    continously.
    Each node's logical expression is combined with the logical 
    expression of its headnode and stored in its headnode semrep 
    attribute.
    Attributes:
        dg: a nltk.parse.dependencygraph.DependencyGraph 
            object with logical expression assigned to each node.
        dependencies: list of nodes marked down for processing.
    '''
    
    def __init__(self, dependencyGraph):
        '''Initialize SemMerger object with given values.
        dependencyGraph has to be a preprocessed (assign.py) 
        nlp.dependencygraph.DependencyGraph object
        Args:
            depedencyGraph: a nltk.parse.dependencygraph.DependencyGraph 
                    that has been preprocessed by a SemRepAssigner object
        Returns:
            the initialized SemMerger object
        Raises:
            TypeError: dg is not a DependencyGraph object
        '''
        self.dg = dependencyGraph
        self.dependencies = []
        
        # checks type of dependencyGraph
        if not isinstance(self.dg, nlp.dependencygraph.DependencyGraph):
            raise TypeError('argument must be a DependencyGraph object')
            
        
    def getDependencies(self):
        '''find bottom of depedencytree and store those nodes in 
        self.dependencies
        '''
        for node in self.dg.nodes:
            
            # finds bottom of dependency tree
            if self.dg.nodes[node]['deps'] == {}:
                self.dependencies.append(node)
                
        # begin right-hand side
        self.dependencies = list(reversed(self.dependencies))

    def getSemRepresentation(self):
        ''' return logical expression of the entire sentence'''
        # returns complete sentence only
        while len(self.dependencies) != 0:
       
            for node in self.dependencies:
                self.sortSemantics(node)
    
        # returns complete logical expression
        root = ourGetRoot(self.dg)
        return root['semrep']

    def sortSemantics(self, node):
        '''gives node's head node combined logical expression'''
        # avoids repitition
        self.dependencies.remove(node)
        
        # abort if top-node is given
        if self.dg.nodes[node]['address'] == 0:
            return
            
        head = self.dg.nodes[node]['head']
        
        # check for first and last name
        if (self.dg.nodes[node]['rel'] == 'PNC' 
            and self.dg.nodes[node]['ctag'] == 'NOUN'):
            return self.mergeNamedEntities(self.dg.nodes[head], 
                                            self.dg.nodes[node])

         # subject-verb has to be last
        elif(
            self.dg.nodes[node]['rel'] == 'SB'
            and len(self.dependencies) > 0
            ):
                self.dependencies.append(self.dg.nodes[node]['address'])
                return
                
        # merges expressions
        self.dg.nodes[head]['semrep'] = self.mergeSemantics(
                                            self.dg.nodes[head],
                                            self.dg.nodes[node]
                                            )
        # checks modification
        if(self.checkModifier(node)):
            return
        
     
        self.checkAdress(head)
        
        # start recursion
        self.getSemRepresentation()
        
        
    def checkAdress(self, head):
        """checks new dependency"""
        if self.dg.nodes[head]['address'] != None:
            self.dependencies.append(self.dg.nodes[head]['address'])
        
    def checkModifier(self, node):
        """checks if node modifies a nomen """
        if (self.dg.nodes[node]['rel'] == 'NK' ):
            self.dependencies.insert(0, self.dg.nodes[node]['head'])
            return True
        
        return False
        
                
    def mergeNamedEntities(self, head_node, node_node):
        '''Fuse representations of first and last name of one entity 
            into one
            
        Args:
            head_node   :   last name of NE
            node        :   first name of NE
        Returns:
            fused expression
        '''
        tlp = nll.LogicParser(type_check=True)
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
        head_node['semrep'] = tlp.parse(new_expr, signature=exprSig)
        return
        
    def mergeSemantics(self, semhead, semdep):
        '''merges logical expressions'''
        # store final logical expression in Top-Node
        if semhead['address'] == 0:
            return semdep['semrep']
            
        try:
            return self.applyCorrectly(semhead['semrep'], semdep['semrep'])
        
        except KeyError:
            #in case of no logical representation
            return semhead['semrep']

    
    def isApplicableTo(self, expr1, expr2):
        '''Test whether expr1 can be applied to expr2.
    
        Args:
            expr1: An nltk.sem.logic.Expression object with resolved type.
            expr2: An nltk.sem.logic.Expression object with resolved type.

        Returns:
            True if expr1 can be applied to expr2; False otherwise.
        '''
        if expr1.type.first == expr2.type:
            return True
        
        elif expr1.type.first.matches(expr2.type):
            print("Warning: Type is not definite, application may be incorrect!")
            return True
        
        return False
        
    def applyCorrectly(self, expr1, expr2):
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
        
        if self.isApplicableTo(expr1, expr2):
            return expr1.applyto(expr2).simplify()
        
        elif self.isApplicableTo(expr2, expr1):
            return expr2.applyto(expr1).simplify()
        
        else:
            # either deps are wrong or types are not accurate
            errMsg = 'The types {0} and {1} are incompatible.'
            raise nll.TypeException(errMsg.format(expr1, expr2))
    
    def getSemantics(self):
        ''' returns logical expression of the entire sentence '''
        self.getDependencies()
        return self.getSemRepresentation()

def ourGetRoot(dependencyGraph):
    '''Get the root node of a dependencyGraph.
    
    Args:
        dependencyGraph: A nltk.parse.DependencyGraph object.
    Returns:
        The root node of the dependencyGraph.
    Raises:
        ValueError if the dependencyGraph has less than or more than
            root node.
    '''
    root_dict = dependencyGraph.nodes[0]['deps']
    roots = []
    for root_list in root_dict.values():
        roots.extend([r for r in root_list])

    if len(roots) == 1:
        return dependencyGraph.nodes[roots[0]]
    elif len(roots) > 1:
        errMsg = 'The dependencyGraph has more than one root.'
        raise ValueError(errMsg)
    else:
        errMsg = 'The dependencyGraph has no root.'
        raise ValueError(errMsg)

def testUsualCase():
    import nltk.sem.logic as nll
    tlk = nll.LogicParser()
    read_expr = tlk.parse
    treebank_data = open('../test/conll/beissende_taube.conll').read()
    dg = nlp.DependencyGraph(treebank_data)
    #this will soon be replaced by an automatic representation
    dg.nodes[1]['semrep'] = read_expr(r'\P\Q. exists x.(P(x) & Q(x))')
    dg.nodes[2]['semrep'] = read_expr(r'\x. taube(x)')
    dg.nodes[3]['semrep'] = read_expr(r'\y\x. beissen(x, y)')
    dg.nodes[4]['semrep'] = read_expr(r'peter')
    semantics = SemMerger(dg)
    return semantics.getSemantics()
    
def test():
    return testUsualCase()
    
if __name__ == '__main__':
    print(test())
