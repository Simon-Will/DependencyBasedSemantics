## Dependency-based semantics construction w/ lambda calculus


### Organisatorisches

* Lukas Mülleder, Simon Will, Rebekka Hubert

* {mülleder, will, hubert}@cl.uni-heidelberg.de

* regelmäßige Treffen und reger Email-Kontakt sowie zu allen Zeiten gegenseitige 
  Kontrolle und kritische Anmerkungen der Gruppenmitglieder

* es werden lediglich die Funktionsweise des Moduls und
  die Voraussetzungen für dessen Verwendung erläutert,  die konkreten
  Funktionsaufrufe und die modularen Abhängigkeiten können unserem README entnommen werden

* Link zum README

* Projekt auf github [https://github.com/Simon-Will/montesniere]

* Arbeitsteilung: Folgender Tabelle sind die Arbeitsschritte, die Scripte und deren Authoren zu
  entnehmen:

    >Planung des Projekts		Simon, Lukas, Rebekka
    
    >process\_with\_spmrl.sh		Simon
    
    >normalize.py			Rebekka
    
    >condition.py			Simon
    
    >heuristic_rules.json		Simon
    
    >assign.py			        Simon
    
    >merge.py			        Simon, Rebekka
    
    >\__init\__.py			Simon
    
    >context.py		 	        Simon
    
    >testNormalizer.py		        Rebekka
       
    >testAssign.py			Simon
    
    >testMerge.py			Simon
  
    >to_xml.awk				Simon
 
    >montesniere_get_Semantics		Rebekka

    >conll-files			Simon, Rebekka
  
    >testsuite			        Lukas, Simon, Rebekka
  
    >Evaluation der Ergebnisse	        Simon, Rebekka, (Lukas?)
  
    >README & Dokumentation		Rebekka

* Voraussetzungen:

	* Python 3.4

	* NLTK 3.0

	* tiger\_release\_aug07.corrected.16012013.conll06

	* RGBParser

	* TIGER-Korpus und RBGParser werden nur zum erstellen neuer Daten benötigt,
	  im Algorithmus selbst finden sie keine Verwendung

* der erste Anhaltspunkt für Fragen ist diese Dokumentation sowie die korrespondierende github-webpage,
  des Weiteren können Fragen auch per Mail an die angegebene Adressen der einzelnen Gruppenmitglieder gestellt 
  werden


### Motivation
Es gibt viele Formalismen, um die Semantik einer Äußerung darzustellen. Für dieses Projekt haben wir
uns das Ziel gesetzt, ein python-Modul für die automatische Verwendung einer dieser Formalismen zu entwickeln:
Die Semantikkonstruktion mit Lambda-Kalkül in NLTK. Damit erweitern wir nicht nur die 
Verwendungsmöglichkeiten von NLTK, sondern erhalten zudem eine leicht 
anzuwendende Möglichkeit mit einfachen Mitteln einen vergleichsweise großen Bereich 
zu erfassen.

Dabei legen wir unseren Schwerpunkt auf die Extraktion von Lambda-Ausdrücken aus 
einzelnen Satzteilen, die dann zur kompletten Repräsentation des Satzes 
zusammengesetzt werden. So kann nun eine relativ hohe Anzahl an Phänomenen mit 
relativ allgemein formulierten Vorgaben aus Sätzen extrahiert und in Form eines 
Lambda-Ausdrucks dargestellt sowie abgefragt werden. 
Ebenfalls wurde eine Testsuit erstellt, in der so extrahiertes Wissen abgefragt
und angewendet werden kann.

Während des gesamten Projekts legten wir besonderen
Wert auf eine intuitive Verwendung und mögliche Weiterentwicklung des Programms.
Im Folgenden wird jeder Programmteil vorgestellt sowie seine genaue Verwendung 
erläutert und anhand von Beispielen veranschaulicht. Anschließend wird auf die 
möglichen Anwendungen, dann auf die Grenzen unseres Moduls näher eingegangen. 


### Funktionsweise des Algorithmus

Unserem Plan folgend haben wir unseren Algorithmus in drei große Schritte und eine
Testsuit geteilt:

* die Vorbereitung des Satzes bzw. der Daten für die weitere Verarbeitung
* die Extraktion der einzelnen Lambda-Ausdrücke
* das Zusammensetzen dieser Einzelrepräsentationen zu einem Lambda-Ausdruck,
  der den kompletten Satz abbildet.
* bei Verwendung de Testsuit wird jedem Prämisse-Hypothese-Paar der Hypothese
  ein Wahrheitswert zugewiesen



Um die Verwendung des Moduls zu erleichtern, befindet sich im Projektordner 
das bash-Skript montesniere_get_Semantics, das den Algorithmus in einem Schritt
ausführt und eine komfortable Ausführung ermöglicht. Dies verhindert, dass
man besondere Aufmerksamkeit auf die Abhängigkeiten der einzelnen Skripte
lenken muss und diesbezügliche Fehler vermieden werden. 

Im Folgenden nun also die einzelnen Schritte unseres Algorithmus:

#### Vorbereitung der Sätze
Der erste Schritt ist optional und sollte nur ausgeführt werden. wenn ein
Hinzufügen von weiteren Daten erwünscht ist.

Möchte man dies, empfiehlt es sich den folgenden Schritt mit einer möglichst
großen Anzahl an Daten durchzuführen, da dieser Schritt im Vergleich zu
den anderen Scripten des Algorithmus recht lange dauert.
Jegliche hinzuzufügende Daten werden in einer Datei gespeichert. Dabei sollte
es sich vorzugsweise um eine txt-Datei handeln.
Das Skript process\_with\_spmrl.sh wird mit der zu verabeitenden Datei als
Konsolenargument angegeben. Beim Ausführen dieser Datei wird der Inhalt des
angegebenen Files tokenisiert und mit einem Model eines RBGParser geparst. 
Dafür wird unserer Default-Modell verwendet, das auf dem 
tiger\_release\_aug07.corrected.16012013.conll06 Korpus auf ella trainiert 
wurde und unter[einfügen] zu finden ist.
Durch die Ausführung des Skripts erhält man den Inhalt der Datei im CoNLL06-Format. 
Soll ein anderes Modell verwendet werden, muss dieses als zweites Konsolenargument 
angegeben werden. Dabei sollte man aber darauf achten, anschließend eine Datei 
im CoNLL09-Format zu erhalten, da bei der Verwendung des CoNLL09-Formats im 
weiteren Verlauf des Algorithmus Probleme auftreten.
Die Ausgabe wird in {Name des Input-Files}.morph.conll gespeichert.

ein kurzes Bsp:

>Ein Kind isst alle Kekse und alle Brezeln.

>Inhalt der Datei testsentence.conll:

    >1       Ein     ein     DET     ART     _       2       NK      _       _
    >2       Kind    kind    NOUN    NN      _       3       SB      _       _
    >3       isst    issen   VERB    VVFIN   _       0       --      _       _
    >4       alle    aller   PRON    PIAT    _       5       NK      _       _
    >5       Kekse   keks    NOUN    NN      _       3       OA      _       _
    >6       und     und     CONJ    KON     _       5       CD      _       _
    >7       alle    aller   PRON    PIAT    _       8       NK      _       _
    >8       Brezeln brezel  NOUN    NN      _       6       CJ      _       _
    >9       .       --      .       $.      _       3       --      _       _



Der Inhalt dieser Datei kann nun für alle weiteren Schritte benutzt werden.


#### Normalisierierng
Wir bezeichnen den ersten Schritt in unserem Verfahren als Normalisierung. Dabei 
handelt es sich um ein Skript, das für unseren Algortihmus nur schwer zu 
verabeitende Sätze in eine leichter zu erfassende Form abändert. Konkret
handelt es sich dabei um Koordinationen von Phrasen, bei denen der Algorithmus
Gefahr läuft zu scheitern. Darunter fallen z. B. solche Äußerungen:
"Peter lädt Maria auf einen Tee und ein Stück Kuchen ein."
Um die spätere Verabeitung zu erleichtern, würde dieser Satz folgendermaßen
abgeändert werden:
"Peter lädt Maria auf einen Tee und Peter lädt Maria auf ein Stück Kuchen ein."
Dieser längere Satz könnte von unserem Algorithmus zumindest teilweise verarbeitet
werden, in seiner urpsrünglichen Fassung würde kein Ergebnis erzielt werden.

Der Fokus liegt dabei auf der Koordination von Objekten und Verben, sowie des 
Ersetzens von Pronomen, wenn das Subjekt im Satz explizit genannt wird.

an einem Beispiel: "Ein Kind isst alle Kekse und alle Brezeln."

    > original
    >1       Ein     ein     DET     ART     _       2       NK      _       _
    >2       Kind    kind    NOUN    NN      _       3       SB      _       _
    >3       isst    issen   VERB    VVFIN   _       0       --      _       _
    >4       alle    aller   PRON    PIAT    _       5       NK      _       _
    >5       Kekse   keks    NOUN    NN      _       3       OA      _       _
    >6       und     und     CONJ    KON     _       5       CD      _       _
    >7       alle    aller   PRON    PIAT    _       8       NK      _       _
    >8       Brezeln brezel  NOUN    NN      _       6       CJ      _       _
    >9       .       --      .       $.      _       3       --      _       _
########aus: test/conll/testsentence.conll

    > normalisierte Struktur
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


In diesem Fall wurde das Subjekt des Satzes vor dem zweiten Verb wieder verwendet
und somit eine Koordination auf Satzebene erreicht.

Dies schließt die Vorverarbeitung der Daten ab

#### Extraktion des einzelnen Lambda-Ausdrücke

Nach der Vorverarbeitung werden die einzelnen Lamda-Ausdrücke für den
eingegebenen Satz erstellt. Dafür wird aus dem Satz durch Verwendung von
NLTK's parse Modul ein Dependenzgraph erstellt. Jedem der Knoten des Graphs
weist unser Algorithmus einen logischen Ausdruck unter Verwendung des 
Lambda-Kalküls zu.
Zur Zuordnung des korrekten Lambda-Ausdrucks verwenden wir eine Datei, in der
Paare aus selbst erstellten Regeln und logischen Ausdrücken gespeichert sind.
Dabei wird jedes Wort des Satzes auf diese Regeln getestet. Kann eine Regel
angewandt werden, wird dem Knoten der entsprechende logische Ausdruck zugewiesen
und kann über den neu erstellten Eintrag 'semrep' abgerufen werden.
Greift keine Regel, wird dem Knoten kein logischer Ausdruck zugewiesen. Ein solcher Fall
tritt z. B. beim ROOT-Knoten auf.

An einem Beispielsatz: "Eine Taube beißt Peter Mueller."

    >import nltk.parse as nlp
    >ass = SemRepAssigner.fromfile('rules/heuristic_rules.json')
    >sTaube = open('test/conll/beissende_taube_und_Peter_Mueller.conll').read()
    >dgTaube = nlp.DependencyGraph(sTaube)
    >ass.assignToDependencyGraph(dgTaube)
    >print(dgTaube.get_by_address(3)['semrep'])
    >\y x.beissen(x,y)
    >print(dgTaube.get_by_address(3)['semrep'].type)
    ><e,<e,t>>
    >print(dgTaube.get_by_address(1)['semrep'])
    >\P Q.exists x.(P(x) & Q(x)


#####test/conll/beissenden\_taube\_und\_Peter\_Mueller.conll

#### Zusammensetzen der Lambda-Ausdrücke

Durch die Ausführung des Skriptes merge.py werden die Lambda-Ausdrücke durch
funktionale Applikaton zu einem Ausdruck für den gesamten Satz zusammengesetzt. 
Dabei findet vor jeder Applikation zweier Lambda-Ausdrücke ein Typ-Überprüfung statt, sodass
nur gültige Typen erstellt werden können.

Dabei schreitet unser Algorithmus den Dependenzbaum von den Blättern zur Wurzel ab. 
Dementsprechend werden erst die Lambda-Ausdrücke der Kinder eines Knotens behandelt
bevor der Algorithmus sich dem Mutterknoten zuwendet. Da sich die gewählte 
Reihenfolge der Applikationen als nicht zielführend erweisen kann, beherrscht 
unser Algorithmus eine Variation des Backtrackings: Die ursprünglichen logischen 
Ausdrücke werden nicht überschrieben. Kann dem gewählte Weg nicht bis zur Wurzel
des Dependenzbaums gefolgt werden, wird dieser Versuch abgebrochen und automatisch
ein andere Reihenfolge ausgewählt. Sobald die Wurzel des Baums erreicht ist, wird
der vollständige logische Ausdruck abgespeichert und kann durch einen 
Funktionsaufruf abgefragt werden.
Sind die Typen der Worte nicht kompatibel, wird nach der Abfrage aller möglichen
Applikationsreihenfolgen eine deskriptive Fehlermeldung ausgegeben.

Der Ablauf am Beispielsatz: "Eine Taube beißt Peter Mueller."
    
    >import nltk.parse as nlp
    >ass = SemRepAssigner.fromfile('rules/heuristic_rules.json')
    >sTaube = open('test/conll/beissende_taube_und_Peter_Mueller.conll').read()
    >dgTaube = nlp.DependencyGraph(sTaube)
    >ass.assignToDependencyGraph(dgTaube)
    >lamdaTaube = SemMerger(dgTaube)
    >lambdaTaube.getSemantics()
    >exists x.(Taube(x) & beissen(x, Peter_Mueller))

Die Fehlermeldung, wenn der Algorithmus die Wurzel des Dependenbaums nicht errreicht,
hier am Beispielsatz "Ein Kind isst alle Kekse und Brezeln."

    >montesniere.merge.NoMergePossibleException: Could not merge the following types:
    >\R x.all y.(brezel(y) -> R(y,x))
    >\Q. exists x.(kind(x) & Q(x))
    >\y x.essen(x,y)
    >\R x.all y.(keks(y) -> R(y,x))

###Testsuite
Bei unserer Testsuit handelt es sich um eine partielle Form der FraCas-Testsuit
für das Deutsche.
In Anlehung an FraCas sind in unserer Testsuite Beispielsätze, sowie deren 
logische Form als Prämissen abgespeichert. Dabei folgt auf jede Prämisse -oder auch auf 
mehrere - eine Hypothese mit ihrer logischen Form, der auf Basis der Prämisse den Wahrheitswert wahr oder
falsch zugewiesen wird.
Diese können abgefragt werden.

#TODO



### Conclusion

Abschließend lässt sich sagen, dass unser Modul einen Großteil der ihm gestellten
Aufgaben zu unserer Zufriedenheit löst. So wird eine breite Variation
von Quantoren in jeder Position korrekt erkannt (alle, einige, keine, etc.),
auch solche, die im betreffenden Satz nicht explizit als solche gekennzeichnet
sind, so wird z. B. in "Große Pferde essen leckeres Futter." die allgemeine 
Aussage erkannt und ein Allquantor verwendet:

    >all x.((pferd(x) & groß(x)) -> exists y.(leck(y) & futter(y) & essen(x,y)))

Zudem stellen sowohl Transitivität und Ditransitivität kein Probleme dar,
 Eigennamen werden korrekt erkannt - darunter auch die Erkennung von Vor- und 
Nachnamen - und die Wortstellung hat keinen Einfluss auf das Ergebnis. 
Hinzu kommt noch eine recht genaue Erkennung und Zuordnung von Adjektiven, 
Negation und wenigen Konjunktionen.

Dennoch ist auch Kritik an unserem Modell angebracht.
Zwar erstellt unser Modul zuverlässig die logische Repräsentation eines Satzes, 
aber es sind ihm Grenzen gesetzt. So erweist sich der Normalizer bei
einigen Sätzen als Hilfe, erschafft jedoch auch neue Probleme.
Dies ist bereits am obigen Beispielsatz "Ein Kind ist alle Kekse und Brezeln."zu 
erkennen. Im eigentlichen Satz besteht kein Zweifel daran, dass es sich bei dem 
Keks essenden und dem Brezel verspeisenden Kind um dasselbe handelt. Betrachtet
man den abgewandelten Satz, so existiert diese Sicherheit nicht. Es besteht kein 
Grund anzunehmen, dass es sich dabei um dieselbe Entität handelt. Dabei handelt es
sich um keinen Einzelfall, sondern um ein prinzipielles Problem:
Wenn das Subjekt oder ein Objekt unter Verwendung eines  Existenzquantors bestimmt
wird, wird das zur Normalisierung eingeschobene Sub- oder Objekt ebenfalls einen
Existenzquantor aufweisen. Dies ließe sich zwar durch die gezielte Verwendung 
von definiten Artikeln verwenden, jedoch haben wir uns entschieden diesen Bereich 
im Rahmen unseres Projekts nicht zu behandeln, um den zeitlichen Rahmen unseres
Projets einzuhalten. 
Das gleiche Problem stellt sich bei der Ersetzung von Pronomen und deren Verarbeitung,
sofern sie nicht auf einen Eigennamen verweisen.
An dieser Stelle könnte das Modul noch erweitert werden.

Ebenfalls Schwierigkeiten bereiten uns noch einige Negationen, deren Skopus teilweise
noch nicht korrekt erkannt wird. Eine genaue Bestimmung mit Hilfe unserer Regeln
erweist sich in diesem Fall als schwierig. Auch hier besteht noch Raum für
Erweiterungen, zumal wir uns erst seit kurzem damit beschäftigen.
Des Weiteren gibt es noch Probleme mit den Anbindungen einiger
Präpositionalphrasen, Adverbien und Adjektive. Allerdings vermuten wir hier einen
Bug in NLTK gefunden zu haben (näheres kann im Python-Skript assign.py und 
heuristic_rules.json nachgelesen werden).

Zusammenfassend besteht jedoch kein Zweifel daran, dass unser Modul bei
einem Großteil der ihm gegebenen Sätze keine Fehler macht.




## Literatur:
tiger\_scheme\_syntax.pdf

A Bilingual Treebank for the FraCaS Test Suite [http://gup.ub.gu.se/records/fulltext/168967/168967.pdf]


##Eigenständigkeitserklärung


