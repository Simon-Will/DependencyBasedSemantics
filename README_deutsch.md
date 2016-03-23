##Dependency-based semantics construction with lambda calculus



Lukas Mülleder

Simon Will

Rebekka Hubert

{mülleder, will, hubert}@cl.uni-heidelberg.de

Institut der Computerlinguistik

Ruprecht-Karls-Universität Heidelberg


###Überblick

Durch Verwendung dieses Moduls können Sätzen logische Ausdrücke zugewiesen und 
bei anschließender Verwendung der Testsuit auch einzelnen Sätzen ein 
Wahrheitswert zugewiesen werden. Dabei wird jedem Wort ein Lambda-Ausdruck
zugewiesen und diese durch funktionale Applikation zusammgefügt.
Der Fokus liegt dabei auf dem korrekten Zuweisen der logischen Ausdrücke.


###Voraussetzungen

Python 3.4

NLTK 3.0

tiger\_release\_aug07.corrected.16012013.conll06

* RGBParser

TIGER-Korpus und RBGParser werden nur zum erstellen neuer Daten benötigt,
im Algorithmus selbst finden sie keine Verwendung

####normalize.py

Dieses Skript kann benutzt werden, um Sätze in eine vereinfachte Form zu bringen,
mit welcher der Algorihmus besser umgehen kann. Dadurch können Fehler in der weiteren
Verarbeitung vermieden werden. Die Verwendung dieses Skript empfiehlt sich lediglich,
wenn neue Sätze zu den bereits vorhandenen conll-Datein hinzugefügt werden sollen.
Hinweis: Das Ausführen dieses Programms ist keine Garantie für ein erfolgreiches 
Ablaufen des Algorithmus.
Für einen Programmaufruf muss der zu normalisierende Satz erst aus einer Datei 
ausgelesen, dann beim Erstellen eines Normalizerobjektes als Argument übergeben
werden. Man erhält den normalisierten durch den Aufruf der Methode getSentence()
des Normalizerobjekts.

Beispiel:

testsentence.morph.conll aus test/conll als Eingabe führt zu folgendem Resultat:

    >1	Ein	ein	DET	ART	_	2	NK	_	_
    >2	Kind	kind	NOUN	NN	_	3	SB	_	_
    >3	isst	issen	VERB	VVFIN	_	0	--	_	_
    >4	alle	aller	PRON	PIAT	_	2	NK	_	_
    >5	Kekse	keks	NOUN	NN	_	3	OA	_	_
    >6	und	und	CONJ	KON	_	5	CD	_	_
    >7	Ein	ein	DET	ART	_	8	NK	_	_
    >8	Kind	kind	NOUN	NN	_	9	SB	_	_
    >9	isst	issen	VERB	VVFIN	_	6	--	_	_
    >10	alle	aller	PRON	PIAT	_	8	NK	_	_
    >11	Brezeln	brezel	NOUN	NN	_	9	CJ	_	_
    >12	.	--	.	$.	_	3	--	_	_




####assign.py

Mit Hilfe eines SemRepAssignerobjekts kann ein Satz eingelesen und 
der dazugehörige Dependenzgraph zurückgegeben werden. Dabei wird jedem
Knoten des Baums ein passender logischer bzw. ein Lamda-Ausdruck 
zugewiesen.
Um ein Assignerobjekt zu erstellen, wird das condition module benötigt.
assign.py und condition.py befinden sich im selben Ordner.
Zur Erstellung eines SemRepAssignerobjekts muss die Datei heuristic_rules.json
der Methode fromSring übergeben werden. Dann einen conll06 formatierten Satz 
beim Aufruf von nltk.parse.DependencyGraph als Argument ergeben.
Das so erstellte Objekt als Argument der SemRepAssigner Methode 
assignToDependencyGraph übergeben.
Durch den Aufruf der Methode get\_by\_address kann jeder Knoten abgefragt 
werden.

Beispiel:

    >import nltk.parse as nlp
    >ass = SemRepAssigner.fromfile('rules/heuristic_rules.json')
    >sKind = open('test/conll/testsentence.conll').read()
    >dgKind = nlp.DependencyGraph(sKind)
    >ass.assignToDependencyGraph(dgKind)
    >print(dgKind.get\_by\_address(3)['semrep'].type)

> 

####merge.py

Die Anwendung dieses Skripts ermöglicht es, die zuvor dem Dependenzgraph in assign.py zugewiesenen
logischen Ausdrücke durch funktionale Applikationen zusammenzufügen.
Bei der Erstellung eines SemMergerobjekts den durch die Anwendung von assign.py erhaltenen
Dependenzgraph als Argument übergeben. Der logische Ausdruck des Satzes kann über die
SemMerger-Methode getSemantics() abgefragt werden.

example:

    >lamdaKind = SemMerger(dgKind)
    >lambdaKind.getSemantics()
    >exists x.(kind(x) & (all y.(Keks(y) -> essen(x,y)))) & exists z.(kind(z) & (all u.(Brezel(u) -> essen(z,u))))


###Testsuite
In dieser Testsuite sind mehrere Prämissen-Hypothesen-Paare im xml-Format im FraCas ähnlichen
Format abgespeichert, wobei der Wahrheitsgehalt der Hypothesen abgefragt werden kann.



###Hinzufügen neuer Daten

Sollen weitere Daten hinzugefügt werden, sind folgende Schritte zu befolgen:

* parsen der hinzuzufügenden Daten, diese sollten als Sätze abgespeichert sein,
  vorzugsweise in einem txt-File

** Dafür wird das Bash-Skript process\_with\_spmrl.sh verwendet. Dabei wird
   das Datenfile als Kommandozeilenargument übergeben. Soll anstelle des 
   Default-RBGParser ein anderer RBGParser verwendet werden, ist dieser 
   als zweites Kommandozeilenargument zu übergeben
   Bsp.:

>Ein Kind isst alle Kekse und alle Brezeln.
>Inhalt der Datei testsentence.conll:
>
    >1       Ein     ein     DET     ART     _       2       NK      _       _
    >2       Kind    kind    NOUN    NN      _       3       SB      _       _
    >3       isst    issen   VERB    VVFIN   _       0       --      _       _
    >4       alle    aller   PRON    PIAT    _       5       NK      _       _
    >5       Kekse   keks    NOUN    NN      _       3       OA      _       _
    >6       und     und     CONJ    KON     _       5       CD      _       _
    >7       alle    aller   PRON    PIAT    _       8       NK      _       _
    >8       Brezeln brezel  NOUN    NN      _       6       CJ      _       _
    >9       .       --      .       $.      _       3       --      _       _

* Wir empfehlen die geparsten Daten manuell zu überpfüfen und ggf. Korrekturen
  vorzunehmen

* Auch können die Daten mit dem Skript normalize.py ggf. angepasst,
  um mögliche spätere Komplikationen zu vermeiden. Dies ist aber nicht Pflicht.

  An unserem Beispiel führt dies zu folgender Änderung:
    >1	Ein	ein	DET	ART	_	2	NK	_	_
    >2	Kind	kind	NOUN	NN	_	3	SB	_	_
    >3	isst	issen	VERB	VVFIN	_	0	--	_	_
    >4	alle	aller	PRON	PIAT	_	5	NK	_	_
    >5	Kekse	keks	NOUN	NN	_	3	OA	_	_
    >6	und	und	CONJ	KON	_	3	CD	_	_
    >7	Ein	ein	DET	ART	_	8	NK	_	_
    >8	Kind	kind	NOUN	NN	_	9	SB	_	_
    >9	isst	issen	VERB	VVFIN	_	6	--	_	_
    >10 alle	aller	PRON	PIAT	_	11	NK	_	_
    >11 Brezeln	brezel	NOUN	NN	_	9	CJ	_	_
    >12	.	--	.	$.	_	3	--	_	_

