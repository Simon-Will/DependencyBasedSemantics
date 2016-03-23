## Dependency-based semantics construction w/ lambda calculus


### Organisatorisches

* Lukas Mülleder, Simon Will, Rebekka Hubert

* {mülleder, will, hubert}@cl.uni-heidelberg.de

* regelmäßige Treffen und reger Email-Kontakt sowie zu allen Zeiten gegenseitige 
  Kontrolle und kritische Anmerkungen der Gruppenmitglieder

* in dieser Dokumentation werden lediglich die Funktionsweise des Moduls erläutert und
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

* der erste Anhaltspunkt für Fragen ist diese Dokumentation sowie die korrespondierende githup-webpage,
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
Lambda-Ausdrucks dargestellt sowie abgefragt werden. Dieser Algorithmus wurde dann für die 
Erstellung einer Testsuit verwendet, die es ermöglicht, das extrahierte Wissen 
abzuspeichern und abzufragen. Während des gesamten Projekts legten wir besonderen
Wert auf eine intuitive Verwendung und mögliche Weiterentwicklung des Programms.
Im Folgenden wird jeder Programmteil vorgestellt sowie seine genau Verwendung 
erläutert und anhand von Beispielen veranschaulicht. Anschließend wird auf die 
möglichen Anwendungen, dann auf die Grenzen unseres Moduls näher eingegangen. 


### Funktionsweise des Algorithmus

Unserem Plan folgend, haben wir unseren Algorithmus in drei große Schritte und eine
Testsuit geteilt:

* die Vorbereitung des Satzes bzw. der Daten für die weitere Verarbeitung
* die Extraktion der einzelnen Lambda-Ausdrücke
* das Zusammensetzen dieser Einzelrepräsentationen zu einem Lambda-Ausdruck,
  der den kompletten Satz abbildet.
* bei Verwendung de Testsuit wird jedem Prämisse-Hypothese-Paar der Hypothese
  ein Wahrheitswert zugewiesen

#### Bitte Skript noch schreiben
Um die Verwendung des Moduls zu erleichtern, befindet sich im Projektordner 
das bash-Skript "......", das den gesamten Algorithmus in einem Schritt
ausführt und eine komfortable Ausführung ermöglicht. Dies verhindert, dass
man besondere Aufmerksamkeit auf die Abhängigkeiten der einzelnen Skripte
lenken muss und diesbezügliche Fehler vermieden werden. 
"...." wird im Projektordner selbst gestartet, erwartet eine Eingabe / hat die
Konsolenargumente xy, und führt die einzelnen Schritte des Algorithmus in korrekter
Reihenfolge automatisiert aus. Das Ergebnis wird ausgegeben / in der Datei xy gespeichert.

Im Folgenden nun also die einzelnen Schritte:

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
Durch die Audführung des Skripts erhält man den Inhalt der Datei im CoNLL06-Format. 
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



Der Inhalt dieser Datei kann nun für alle weiteren Schritte benutzt werden
und dient im weiteren Verlauf dieser Dokumentation als Beispiel.

#### konkrete Vorbereitung
Wir bezeichnen den ersten Schritt in unserem Verfahren als Normalisierung. Dabei 
handelt es sich um ein Skript, das für unseren Algortihmus nur schwer zu 
verabeitende Sätze in eine leichter zu erfassende Form abändert. Konkret
handelt es sich dabei um Koordinationen von Phrasen, bei denen der Algorithmus
Gefahr läuft zu scheitern (wir verwenden lediglich Dependenzbäume, jedoch lässt sich
dieses Problem unter Einbezug der Phrasenstrukturbegrifflichkeiten verständlicher
erklären).

Der Fokus liegt dabei auf der Koordination von Objekten und Verben, sowie des 
Ersetzens von Pronomen.

am Beispiel:


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

########Quelle hier einfügen###########################
In diesem Fall wurde das Subjekt des Satzes vor dem zweiten Verb wieder verwendet
und somit eine Koordination auf Satzebene erreicht.

Dies schließt die Vorverarbeitung der Daten ab.

#### Extraktion des einzelnen Lambda-Ausdrücke

Dieser Schritt erfolgt über einen Programmaufruf des Skriptes assign.py.
An dieser Stelle ist noch anzumerken, dass der Aufruf dieses Programms
die beiden Skripte condition.py und heuristic\_rules.json benötigt.
Dabei enthält heuristic\_rules.json sämtliche zum Festlegen der 
Lambda-Ausdrücke benötigten Regeln, während condition.py diese zu 
für den Assigner verwendbaren Regeln umwandelt.
Dementsprechend müssen hier diese Abhängigkeiten beachtet werden.

Durch die Ausführung des Skripts wird der Satz mit Hilfe des Moduls nltk.parse
als ein Dependenzbaum dargestellt. Auf diesen wird dann ein 
Assigner Objekt angewandt. Dadurch erhält jeder relevante Bestandteil
des eingegebenen, zuvor geparsten Satzes einen eigenen Lambda-Ausdruck.
Bei der Zuweisung dieser Ausdrücke werden die eingespeisten Regeln
abgefragt. Ein Ausdruck wird nur in Übereinstimmung mit den Regeln 
festgelegt.
Diese Zuweisung kann anschließend beliebig abgefragt werden.

Ein solcher Aufruf als Beispiel:

    >import nltk.parse as nlp
    >ass = SemRepAssigner.fromfile('rules/heuristic_rules.json')
    >sKind = open('test/conll/testsentence.conll').read()
    >dgKind = nlp.DependencyGraph(sKind)
    >ass.assignToDependencyGraph(dgKind)
    >print(dgKind.get\_by\_address(3)['semrep'].type)


#####Quelle einfügen#####

#### Zusammensetzen der einzelnen Lambda-Ausdrücke

Durch die Ausführung des Skriptes merge.py werden die Lambda-Ausdrücke der einzelnen
Wörter zu einem Ausdruck für den gesamten Satz zusammengesetzt. Dabei findet vor 
jeder Applikation zweier Lambda-Ausdrücke ein Typ-Überprüfung statt, sodass
nur gültige Typen erstellt werden.
Folglich handelt es sich bei merge.py um kein eigenständiges Skript, da es den 
vorverarbeiteten Dependenzbaum benötigt. Durch einen Funktionsaufruf kann nun 
der vollständige logische Ausdruck des Satzes abgefragt werden.
Sind die Typen der Worte nicht kompatibel, erhält man eine deskriptive Fehlermeldung.

wieder das Beispiel:

    >lamdaKind = SemMerger(dgKind)
    >lambdaKind.getSemantics()
    >exists x.(kind(x) & (all y.(Keks(y) -> essen(x,y)))) & exists z.(kind(z) & (all u.(Brezel(u) -> essen(z,u))))


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
Aufgaben zu unserer Zufriedenheit lösen kann. So wird eine breite Variation
von Quantoren in jeder Position korrekt erkannt (alle, einige, keine, etc.),
Transitivität und Ditransitivität stellen keine Probleme dar, Eigennamen werden
korrekt erkannt - darunter auch die Erkennung von Vor- und Nachnamen - und die
Wortstellung hat keinerlei Einfluss auf das Ergebnis.

Dennoch ist auch Kritik an unserem Modell angebracht.
Zwar erstellt unser Modul zuverlässig die logische Repräsentation eines Satzes, 
aber es sind ihm Grenzen gesetzt. So erweist sich der Normalizer bei
einigen Sätzen als Hilfe, erschafft jedoch auch neue Probleme.
Dies ist bereits am obigen Beispielsatz zu erkennen. Im eigentlichen Satz besteht
kein Zweifel daran, dass es sich bei dem Keks essenden und dem Brezel verspeisenden
Kind um dasselbe handelt. Betrachtet man den abgewandelten Satz, so existiert diese
Sicherheit nicht. Es besteht kein Grund anzunehmen, dass es sich dabei um dasselbe
Entität handelt. Der logische Ausdruck in unserem letzten Schritt spiegelt diesen
Unterschied auch wieder. Dabei handelt es sich um keinen Einzelfall, denn dieses
Phänomen tritt immer auf, wenn das Subjekt von einem Existenzquantor bestimmt
wird. Dies ließe sich zwar durch die gezielte Verwendung von definiten Artikeln
verwenden, jedoch haben wir uns entschieden diesen Bereich im Rahmen unseres 
Projekts nicht zu behandeln, um den zeitlichen Rahmen einzuhalten. Das gleiche
Problem stellt sich bei der Ersetzung von Pronomen.
An dieser Stelle könnte das Modul noch erweitert werden.

Ebenfalls Schwierigkeiten bereiten uns Negationen, da wir mit unserem Ansatz 
ihren Skopus bisher nicht konkretisieren konnten. Auch hier besteht noch Raum für
Erweiterungen, zumal wir uns mit diesem Problem bisher noch kaum beschäftigen
konnten. Des Weiteren gibt es noch Probleme mit den Anbindungen einiger 
Präpositionalphrasen und Adverbien. Allerdings vermuten wir hier einen
Bug in NLTK gefunden zu haben (näheres kann im Python-Skript assign.py und 
heuristic_rulel.json nachgelesen werden).

Zusammenfassend besteht jedoch kein Zweifel daran, dass unser Modul bei
einem Großteil der ihm gegebenen Sätze keine Fehler macht.




## Literatur:
tiger\_scheme\_syntax.pdf

A Bilingual Treebank for the FraCaS Test Suite [http://gup.ub.gu.se/records/fulltext/168967/168967.pdf]


##Eigenständigkeitserklärung


