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
Wahrheitswert zugewiesen werden. Dabei wird aus dem eingespeisten
Satz ein Dependenzgraph aus dem eingegebenen Satz erschaffen. 
Jedem Knoten des Graphen wird ein eigener Lambda-Ausdruck zugewiesen, der dessen
Bedeutung repräsentiert. Diese Ausdrücke werden dann zusammengesetzt und 
der logische Ausdruck für den gesamten Satz zurückgegeben. 
Dieser kann benutzt werden, um einem anderen Satz auf der Basis des extrahierten
Wissens einen Wahrheitswert zuzuweisen. Unsere Testsuit repräsentiert diese 
Funktion.
Der Fokus des Moduls liegt auf dem korrekten Zuweisen der logischen Ausdrücke.

###Voraussetzungen

Python 3.4

NLTK 3.0


###Module

####normalize.py
Die Verwendung dieses Skript empfiehlt sich lediglich vor dem Hinzufügen
von neuen Daten im '"test" Ordner.
Es verändert die Struktur eines Satzes, indem er problematische Koordinationen
von Phrasen umschreibt. Dadurch werden Fehler in der weiteren
Verarbeitung vermieden.
Hinweis: Das Ausführen dieses Programms ist keine Garantie für ein erfolgreiches 
Ablaufen des Algorithmus.
Für einen Programmaufruf muss der zu normalisierende Satz im conll06-Format 
als Argument übergeben werden. Durch Aufruf der Methode getSentence() wird
der normalisierte Satz zurückgegeben.


Beispiel:

testsentence.morph.conll aus test/conll als Eingabe führt zu folgendem Resultat:

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

Um ein Assignerobjekt zu erstellen, wird das condition module benötigt.
Dieses muss importiert werden.
Zur Erstellung eines SemRepAssignerobjekts muss die Datei heuristic_rules.json
der Methode fromSring übergeben werden. Dann muss man einen conll06 formatierten Satz 
beim Aufruf von nltk.parse.DependencyGraph als Argument übergeben.
Danach ruft man die Methode assignToDependencyGraph des erstellten SemRepAssigner 
mit dem DependencyGraphobjekt als Argument auf.
Durch den Aufruf der Methode get\_by\_address kann jeder Knoten abgefragt 
werden.

Beispiel:

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

Dieses Modul kombiniert die zuvor dem Dependenzgraph in assign.py zugewiesenen
logischen Ausdrücke.
Man übergibt bei der Erstellung eines SemMergerobjekt den durch die Anwendung von
assign.py erhaltenen Dependenzgraph als Argument.
Der logische Ausdruck des Satzes wird über die
SemMerger-Methode getSemantics() abgefragt.

Beispiel:

    >lamdaTaube = SemMerger(dgTaube)
    >lambdaTaube.getSemantics()
    >exists x.(Taube(x) & beissen(x, Peter_Mueller)))))


###Testsuite
In dieser Testsuite sind mehrere Prämissen-Hypothesen-Paare im xml-Format im FraCas ähnlichen
Format abgespeichert, wobei der Wahrheitsgehalt der Hypothesen abgefragt werden kann.



###Hinzufügen neuer Daten

Sollen weitere Daten hinzugefügt werden, sind folgende Schritte zu befolgen:

* parsen der hinzuzufügenden Daten, vorzugsweise mit einem RBGParser, der auf dem
  TIGER-Korpus trainiert wurde

* Wir empfehlen die geparsten Daten manuell zu überpfüfen und ggf. Korrekturen
  vorzunehmen

* Nun wird Normalize.py verwendet, um problematische Phrasenkoordination zu vermeiden

* Wir empfehlen die verarbeiteten Daten manuell zu überprüfn und ggf. zu korrigieren

* Nun die Daten den Testdaten hinzufügen
