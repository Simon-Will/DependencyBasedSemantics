#!/usr/bin/env python3
# -*- coding: utf-8

from nltk.grammar import DependencyGrammar
import nltk.sem.logic as nll
import nltk.parse as nlp
tlk = nll.LogicParser()
read_expr = tlk.parse

class SemMerger:

    def __init__(self, dependencyGraph):
        self.dg = dependencyGraph
        self.relations = []
        # check type
        if isinstance(self.dg, nlp.dependencygraph.DependencyGraph):
            pass

        else:
            raise TypeError('argument must be a dependencygraph')
            
        
    def getDependencies(self):
        """
        Reads head, rel, dep triples from the given DependencyGraph and 
        reverses their order
        """
        for (head, rel, dep) in self.dg.triples():
            self.relations.append((head, rel, dep))
        self.relations = list(reversed(self.relations))
        
    def getSemRepresentation(self):
        """ Sort semantic representations to each triple """
        # apply each node to a triple
        for triple in self.relations:
            self.sortSemantics(triple)
        sentence = self.dg.nodes[self.dg.nodes[0]['deps']['ROOT'][0]]
        return sentence['semrep']    
            
            
    def sortSemantics(self, triple):
        """gives each node the correct logical expression"""
        # store each represenation
        semRep = {}
        semRep['dep'] = None
        semRep['head'] = None
        for node in self.dg.nodes:
            word = self.dg.nodes[node]['word']
                
            if word == triple[0][0]:
                semRep['head'] = self.dg.nodes[node]['semrep']
                processedNode = node
                    
            elif word == triple[2][0]:
                semRep['dep'] = self.dg.nodes[node]['semrep']
                
            if (semRep['head'] != None and semRep['dep'] != None):
                # relation is needed in order to apply correctly
                self.dg.nodes[processedNode]['semrep'] = self.mergeSemantics(
                                                            semRep['dep'], 
                                                            triple[1], 
                                                            semRep['head']
                                                            )
                break
    
    
    def mergeSemantics(self, semdep, relation, semhead):
        """merges logical expressions"""
        # better solution woulb be truly appreciated!
        try:
            if (relation == 'NK' or relation == 'SB') and \
                (type(semdep) != nll.ConstantExpression):
                return semdep.applyto(semhead).simplify()
        
            else:
                return semhead.applyto(semdep).simplify()
        
        except AssertionError:
            return "semantic representation must be a logical expression!"
    
    def getSemantics(self):
        """ returns logical expression of the entire sentence """
        self.getDependencies()
        return self.getSemRepresentation()
    
    
    
    
    
    
def testUsualCase():
    treebank_data = open('../test/beissende_taube.conll').read()
    dg = nlp.DependencyGraph(treebank_data)
    # this will soon be replaced by an automatic representation
    dg.nodes[1]['semrep'] = read_expr(r'\P\Q. exists x. (P(x) & Q(x))')
    dg.nodes[2]['semrep'] = read_expr(r'\x. taube(x)')
    dg.nodes[3]['semrep'] = read_expr(r'\y\x. beissen(x, y)')
    dg.nodes[4]['semrep'] = read_expr(r'peter')
    dg.nodes[5]['semrep'] = None
    semantics = SemMerger(dg)
    return semantics.getSemantics()
    
if __name__ == '__main__':
    print(testUsualCase())
