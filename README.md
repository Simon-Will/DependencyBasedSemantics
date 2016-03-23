##Dependency-based semantics construction with lambda calculus


###Authors


Lukas Mülleder

Simon Will

Rebekka Hubert

{mülleder, will, hubert}@cl.uni-heidelberg.de

Institute of Computational Linguistics

Heidelberg University, Germany


###Outline



The algorithm presented in this module takes already parsed sentences, extracts their meaning
and returns a logical expression representing the given sentence. During this process, 
a depedencygraph is created out of the given sentence and each node is assigned a unique 
lambda expression representing its meaning. Then these expression are merged using functional
application and returned to the user.
This complete expression can be accessed and later used to assign a truth value to an other sentence
related to that extracted knowledge. This function is represented by our testsuit.


###Requirements

Python 3.4

NLTK 3.0

####normalize.py

Start by using normalize.py to normalize the input sentences in order to avoid unfortunate
coordination of phrases. 
This script takes one sentence in conll06-format as input parameter and returns the normalized
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




####assign.py

The SemRepAssigner relies on the Condition module to work properly, 
therefore you have to import it first.
Use the heuristic rules in the rules directory as a parameter to create a
SemRepAssigner object. Then read a conll06-formated sentence from a file
and use nltk's parse module to create a DependencyGraph object.
Now call the function assignToDependencyGraph of the SemRepAssigner object
to assign a logical lambda expression to every relevent word in the parsed
sentence. By calling the get\_by\_address function you can access every node
and all its attributes.

example:

>import nltk.parse as nlp

>ass = SemRepAssigner.fromfile('rules/heuristic_rules.json')

>sKind = open('test/conll/testsentence.conll').read()

>dgKind = nlp.DependencyGraph(sKind)

>ass.assignToDependencyGraph(dgKind)
 
>print(dgKind.get\_by\_address(3)['semrep'].type)

> 

####merge.py

The algorithm merges all logical expressions into one representing the input sentence.
Consequently, you have to use a dependencygraph preprocessed by a SemRepAssigner object
to create a SemMerger object. Then call the getSemantics function of the SemMerger object
to receive the merged logical expression.

example:

>lamdaKind = SemMerger(dgKind)

>lambdaKind.getSemantics()

exists x.(kind(x) & (all y.(Keks(y) -> essen(x,y)))) & exists z.(kind(z) & (all u.(Brezel(u) -> essen(z,u))))


###Testsuite
Both semantic premises and hypotheses are stored in the testsuite. An input sentence is processed and the
suit assigns a truth value and returns it.

example:
#TODO



###Results


