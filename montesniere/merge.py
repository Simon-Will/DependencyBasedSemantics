#!/usr/bin/env python3
# -*- coding: utf-8

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
        
    def __init__(self, dependencyGraph):
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
        self.dg = dependencyGraph
        self.dependencies = []
        # check type
        if isinstance(self.dg, nlp.dependencygraph.DependencyGraph):
            pass

        else:
            raise TypeError('argument must be a dependencygraph')
            
        
    def getDependencies(self):
        '''find bottom of depedencytree and store those nodes in 
        self.dependencies
        '''
        for node in self.dg.nodes:
            
            if self.dg.nodes[node]['deps'] == {}:
                self.dependencies.append(node)
                
        # solve object-verb dependencies first
        self.dependencies = list(reversed(self.dependencies))
        
    def getSemRepresentation(self):
        ''' return logical expression of the entire sentence'''
        # ensure that entire sentence is resolved
        while len(self.dependencies) != 0:
       
            for node in self.dependencies:
                self.sortSemantics(node)
       
        return self.dg.root['semrep']
            
            
    def sortSemantics(self, node):
        '''gives each node the correct logical expression'''
        self.dependencies.remove(node)
        head = self.dg.nodes[node]['head']
        
        # stops the loop once the top of the tree has been reached
        if self.dg.nodes[node]['address'] == 0:
            return
        
        # fuses two representations of one entity (NE: first and last name)
        elif (self.dg.nodes[node]['rel'] == 'PNC' 
            and self.dg.nodes[node]['ctag'] == 'NOUN'):
            return self.doubleNamedEntity(self.dg.nodes[head], 
                                            self.dg.nodes[node])
                                            
    
        
        # subject-verb has to be last
        elif(
            self.dg.nodes[node]['rel'] == 'SB'
            and len(self.dependencies) > 0
            ):
                self.dependencies.append(self.dg.nodes[node]['address'])
                return
        
        # merge logical expressions
        self.dg.nodes[head]['semrep'] = self.mergeSemantics(
                                            self.dg.nodes[head],
                                            self.dg.nodes[node]
                                            )
                                            
        if self.dg.nodes[head]['address'] != None:
            self.dependencies.append(self.dg.nodes[head]['address'])
        
        # starts (not quite) a loop
        self.getSemRepresentation()
    
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
        head_node['semrep'] = tlp.parse(new_expr, signature=exprSig)
    
    
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
            raise nll.TypeException(expr1, expr2, "are not compatible,\
                                    wrong types?")


    
    def getSemantics(self):
        ''' returns logical expression of the entire sentence '''
        self.getDependencies()
        return self.getSemRepresentation()

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
