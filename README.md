#Dependency-based semantics construction with lambda calculus


##Authors


Lukas Mülleder         

Simon Will              

Rebekka Hubert          

{mülleder, will, hubert}@cl.uni-heidelberg.de

Institute of Computational Linguistics

Heidelberg University, Germany


##Outline



Our goal was to create an algorithm that takes sentences, extracts their meaning
and is both capable of judging statements to be true or false and answer
questions based on the extracted knowledge.
In order to achieve this goal first a RPG-model is trained on the TIGER-corpus
and then used to annotate any sentence given by the user of the algorithm.
This annotated sentence is then further processed in various steps to extract
its meaning and store it as a lambda expression.
Then this meaning can be assest and used to answer a question related to that
knowledge.



##Requirements

Python 3.4

NLTK

tiger\_release\_aug07.corrected.16012013.conll06




##Strucure and Usage of the Single Program Parts

###normalize.py

Start by using normalize.py to normalize the input sentences in order to avoid unfortunate
coordination of phrases. During this step all coordinated phrases are changed from
rather difficult constructions to far simpler phrases.
This script takes one  sentence as input parameter and returns the normalized
sentence.

example:

our testsentence.morph.conll as input yields:

1	Ein	ein	DET	ART	_	2	NK	_	_

2	Kind	kind	NOUN	NN	_	3	SB	_	_

3	isst	issen	VERB	VVFIN	_	0	--	_	_

4	alle	aller	PRON	PIAT	_	2	NK	_	_

5	Kekse	keks	NOUN	NN	_	3	OA	_	_

6	und	und	CONJ	KON	_	5	CD	_	_

7	Ein	ein	DET	ART	_	8	NK	_	_

8	Kind	kind	NOUN	NN	_	9	SB	_	_

9	isst	issen	VERB	VVFIN	_	6	--	_	_

10	alle	aller	PRON	PIAT	_	8	NK	_	_

11	Brezeln	brezel	NOUN	NN	_	9	CJ	_	_

12	.	--	.	$.	_	3	--	_	_



At this point, the first problem of the algorithm is evident: 
There is an immensse difference between our original sentence and the normalized one:
This sentence speaks of one child eating all cookies and of one child,
who eats all pretzel. There is no reason to believe both subjects refer to the
same child.
In other words, the semantic of the sentence has been changed.



###assign.py

This normalized sentence is then used as a parameter of the SemRepAssigner class
in  assign.py to give each word in the sentence a logical expression.
This is done by creating a dependencygraph using nltk.
During the algorithm each node is given a logical expression representing its
word. The script returns the modified dependencygraph.



###merge.py

The output of assing.py is given to merge.py as input parameter. The algorithm
merges all logical expression into one representing the input sentence.
This expression is then returned.

example:
exists x.(kind(x) & (all y.(Keks(y) -> essen(x,y)))) & exists z.(kind(z) & (all u.(Brezel(u) -> essen(z,u))))


##Testsuite
Both semantic premises and hypotheses are stored in the testsuite. An input sentence is processed and the
suit assigns a truth value and returns it.
example:
#TODO



##Results


