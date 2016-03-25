## Dependency-based semantics construction with lambda calculus


### Authors

Lukas Mülleder

Rebekka Hubert

Simon Will

{mülleder, will, hubert}@cl.uni-heidelberg.de

Institut für Computerlinguistik

Ruprecht-Karls-Universität Heidelberg


### Überblick

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


### Voraussetzungen

Python 3.4

NLTK 3.0


### Module

#### `montesniere_get_Semantics.sh`
Wir empfehlen dieses Skript über die Kommandozeile aufzurufen. Die zu 
verarbeitende Datei wird als Kommamdozeilenparameter angegeben. 
Der komplette Algorithmus wird ausgeführt, anschließend wird der vollständie 
logische Ausdruck auf der Kommandozeile ausgegeben.

#### `normalize.py`
Die Verwendung dieses Skript empfiehlt sich lediglich vor dem Hinzufügen
von neuen Daten im Ordner `test/`.
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

    1	Ein	ein	DET	ART	_	2	NK	_	_
    2	Kind	kind	NOUN	NN	_	3	SB	_	_
    3	isst	issen	VERB	VVFIN	_	0	--	_	_
    4	alle	aller	PRON	PIAT	_	5	NK	_	_
    5	Kekse	keks	NOUN	NN	_	3	OA	_	_
    6	und	und	CONJ	KON	_	3	CD	_	_
    7	Ein	ein	DET	ART	_	8	NK	_	_
    8	Kind	kind	NOUN	NN	_	9	SB	_	_
    9	isst	issen	VERB	VVFIN	_	6	--	_	_
    10	alle	aller	PRON	PIAT	_	11	NK	_	_
    11	Brezeln	brezel	NOUN	NN	_	9	CJ	_	_
    12	.	--	.	$.	_	3	--	_	_


#### assign.py

Um ein Assignerobjekt zu erstellen, wird das condition module benötigt.
Zur Erstellung eines SemRepAssignerobjekts muss die Datei `heuristic_rules.json`
der Methode fromSring übergeben werden. Dann muss man einen conll06 formatierten Satz 
beim Aufruf von nltk.parse.DependencyGraph als Argument übergeben.
Danach ruft man die Methode assignToDependencyGraph des erstellten SemRepAssigner 
mit dem DependencyGraphobjekt als Argument auf.
Durch den Aufruf der Methode `get_by_address` kann jeder Knoten abgefragt 
werden.

Beispiel für den Satz „Eine Taube beißt Peter Müller“ (`>` markiert den Python-Interpreter):

    > import nltk.parse as nlp
    > from montesniere.assign import SemRepAssigner
    > ass = SemRepAssigner.fromfile('rules/heuristic_rules.json')
    > sTaube = open('test/conll/beissende_taube_und_Peter_Mueller.conll').read()
    > dgTaube = nlp.DependencyGraph(sTaube)
    > ass.assignToDependencyGraph(dgTaube)
    > print(dgTaube.get_by_address(3)['semrep'])
    \y x.beissen(x,y)
    > print(dgTaube.get_by_address(3)['semrep'].type)
    <e,<e,t>>


#### merge.py

Dieses Modul kombiniert die zuvor dem Dependenzgraph in assign.py zugewiesenen
logischen Ausdrücke.
Man übergibt bei der Erstellung eines SemMergerobjekt den durch die Anwendung von
assign.py erhaltenen Dependenzgraph als Argument.
Der logische Ausdruck des Satzes wird über die
SemMerger-Methode getSemantics() abgefragt.

Beispiel (`>` markiert den Python-Interpreter):

    > lambdaTaube = SemMerger(dgTaube)
    > lambdaTaube.getSemantics()
    exists x.(Taube(x) & beissen(x, Peter_Mueller)))))


### Regeln

Der `SemRepAssigner` aus dem Modul `montesniere.assign` ist am einfachsten mit
einer Regeldatei im `json`-Format zu benutzen. Wir haben einige Regeln
heuristischer Natur erstellt (`rules/heuristic_rules.json`), die voraussetzen,
dass der Dependenzgraph die POS-Tags des
[Stuttgart-Tübingen-Tagset](http://homepage.ruhr-uni-bochum.de/stephen.berman/Korpuslinguistik/Tagsets-STTS.html)
und Dependenz-Tags des 
[TIGER-Annotations-Schemas](http://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/TIGERCorpus/annotation/tiger_scheme-syntax.pdf)
benutzt.
Diese Regeln decken sehr grundlegende deutsche Sätze ab (eine erwähnenswerte
Ausnahme stellen bestimmte Artikel dar).

Natürlich können eigene Regeln geschrieben werden oder unsere verbessert werden.
Eine `json`-Datei muss aus einem Array von Regel-Objekten bestehen.
Ein Regel-Objekt hat drei Keys zu enthalten:

  * Der Key `conditions` muss auf ein Array aus Strings abbilden, die der Syntax
    eines montesniere.condition.Condition-Objektes genügen.
  * Der Key `semRepPat` muss auf einen String abbilden, der von einem
    nltk.sem.logic.LogicParser-Objekt interpretiert werden kann. Vorher
    wird der String aber noch von der Python-Methode str.format formatiert.
    So kann man das Lemma eines Wortes dynamisch zur semantischen
    Repräsentation hinzufügen, indem man im `semRepPat` `{[lemma]}` verwendet.
  * Der Key `semSig` muss auf ein Signatur-Objekt abbilden, dessen Keys
    Ausdrücke sein sollten, die in `semRepPat` vorkommen. Die Keys müssen auf
    Strings abbilden, die die Typen der jeweiligen Ausdrücke beschreiben.

Außerdem ist es nützlich, zu jedem Regel-Objekt eine Erklärung hinzuzufügen, die
beschreibt, welches Phänomen die Regel behandelt. Andernfalls verliert man leicht
den Überblick, sobald die Regelmenge eine gewisse Größe erreicht.

Beispielregel:

```json
{
    "explanation": "proper name in subject position",
    "conditions": [
        "tag element {NE}",
        "rel element {SB}"
    ],
    "semRepPat": "\\P. P({[lemma]})",
    "semSig": {
        "P": "<e,t>",
        "{[lemma]}": "e"
    }
}
```


### Testsuite
Diese Testsuite ist der englischen [FraCaS-Testsuite](http://www-nlp.stanford.edu/~wcmac/downloads/) nachempfunden.
In dieser Testsuite sind mehrere Prämissen-Hypothesen-Paare im xml-Format im FraCas ähnlichen
Format abgespeichert, wobei der Wahrheitsgehalt der Hypothesen abgefragt werden kann.
Dazu wird folgender Kommandozeilenaufruf verwendet:

    > ./testFracas.py [Regeln] [Fracas Testsuit im xml-Format]

Beispiel (`>` markiert die Shell):
   
    > test/testFracas.py ../rules/heuristic_rules.json testsuite_text_tags.xml
    33 out of 39 failed
    IDs of failed tests: 1, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20,
     21, 22, 23, 24, 26, 27, 28, 29, 31, 32, 33, 34, 35, 36, 37, 38, 38

Für genauere Information über die einzelnen Tests kann die Option `--verbose` hinzugefügt werden.


### Hinzufügen neuer Daten

Sollen weitere Daten hinzugefügt werden, sind folgende Schritte zu befolgen:

* Parsen der hinzuzufügenden Daten, vorzugsweise mit einem RBGParser, der auf dem
  TIGER-Korpus trainiert wurde

* Wir empfehlen die geparsten Daten manuell zu überpfüfen und ggf. Korrekturen
  vorzunehmen

* Nun wird `normalize.py` verwendet, um problematische Phrasenkoordination zu vermeiden

* Wir empfehlen die verarbeiteten Daten manuell zu überprüfn und ggf. zu korrigieren

* Nun die Daten den Testdaten hinzufügen

### Name des Pakets

Der name `montesniere` ruft die beiden Wissenschaftler
[Richard Montague](https://de.wikipedia.org/wiki/Richard_Montague)
und [Lucien Tesnière](https://de.wikipedia.org/wiki/Lucien_Tesnière)
ins Gedächtnis, deren Arbeit auf den Gebieten der Dependenzgrammatik bzw. 
der Formalen Semantik wir zu Dank verpflichtet sein.
