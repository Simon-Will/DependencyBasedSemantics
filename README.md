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


####montesniere_get_Semantics
We recommend using our bash script in order to avoid dependency errors. Start it on
the command line and run ./algorithm.sh test/conll/filename


####normalize.py

This module is only needed if you intend to add new data to or test directory.
Use normalize.py to normalize the input sentences in order to avoid unfortunate
coordination of phrases. 
This script takes one sentence in conll06-format as input parameter and returns the normalized
sentence. 

example:

our testsentence.morph.conll as input yields:

    >1	Ein	ein	DET	ART	_	2	NK	_	_
    >2	Kind	kind	NOUN	NN	_	3	SB	_	_
    >3	isst	issen	VERB	VVFIN	_	0	--	_	_
    >4	alle	aller	PRON	PIAT	_	5	NK	_	_
    >5	Kekse	keks	NOUN	NN	_	3	OA	_	_
    >6	und	und	CONJ	KON	_	3	CD	_	_
    >7	Ein	ein	DET	ART	_	8	NK	_	_
    >8	Kind	kind	NOUN	NN	_	9	SB	_	_
    >9	isst	issen	VERB	VVFIN	_	6	--	_	_
    >10	alle	aller	PRON	PIAT	_	11	NK	_	_
    >11	Brezeln	brezel	NOUN	NN	_	9	CJ	_	_
    >12	.	--	.	$.	_	3	--	_	_




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

an example: Sentence: "Eine Taube beißt Peter Müller"

    >import nltk.parse as nlp
    >ass = SemRepAssigner.fromfile('rules/heuristic_rules.json')
    >sTaube = open('test/conll/beissende_taube_und_Peter_Mueller.conll').read()
    >dgTaube = nlp.DependencyGraph(sTaube)
    >ass.assignToDependencyGraph(dgTaube)
    >print(dgTaube.get_by_address(3)['semrep'])
    >\y x.beissen(x,y)
    >print(dgTaube.get_by_address(3)['semrep'].type)
    ><e,<e,t>>

####merge.py

The algorithm merges all logical expressions into one representing the input sentence.
Consequently, you have to use a dependencygraph preprocessed by a SemRepAssigner object
to create a SemMerger object. Then call the getSemantics function of the SemMerger object
to receive the merged logical expression.

example, using the same sentence as before:

    >lamdaTaube = SemMerger(dgTaube)
    >lambdaTaube.getSemantics()
    >exists x.(Taube(x) & beissen(x, Peter_Mueller))



###testFracas.py
Both premises and hypotheses are stored in the testsuite. Call testFracas.py from the commandline,
use heuristic\_rules.json and testsuite\_text\_tags.xml as arguments. The number of failed and
succesful tests is shown on the commandline.


example:

    >./testFracas.py ../rules/heuristic_rules.json testsuite_text_tags.xml
    >33 out of 39 failed
    >IDs of failed tests: 1, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20,
    > 21, 22, 23, 24, 26, 27, 28, 29, 31, 32, 33, 34, 35, 36, 37, 38, 38

###Add new data
Follow these steps to add new data:

* Parse your sentences first. We recommend using a RBGParser model trained on the TIGER corpus
* Check your parsed data manuelly and correct wrong parses.
* Use normalize.py to normalize your sentences in order to avoid unfortunate coordinations of phrases
* Check your data for mistakes manually.
* Add it to our test data.
