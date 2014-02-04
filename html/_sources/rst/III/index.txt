******
Design
******

.. epigraph::

    | *If the implementation is hard to explain, it's a bad idea.*
    | *If the implementation is easy to explain, it* may *be a good idea.*

    -- *Zen of Python*, ``import this``

Wie fügt sich libmunin in seine Welt ein?
=========================================
.. figure:: figs/integration.*
    :alt: Integrationsübersicht
    :width: 100%
    :align: center

    Wie integriert sich libmunin in seine Umgebung?

.. figure:: figs/provider_process.*
    :alt: Attributverarbeitung
    :width: 75%
    :align: center

    Ablauf bei der Verarbeitung eines einzelnen Attributes.

Architektur
===========

.. figure:: figs/munin_startup.*
    :alt: Allgemeine Benutzung
    :width: 75%
    :align: center

    Allgemeine Benutzung von libmunin


.. figure:: figs/arch.*
    :alt: Architekturübersicht.
    :width: 100%
    :align: center

    Grobe Übersicht über die Architektur.

Algorithmik
===========

Die genaue Beschreibung der Algorithmik wird in der Bachelorarbeit detailliert
besprochen. Hier nur ein kurzer Überblick was mit welchem Ziel implementiert
wird.

Graphenoperationen
------------------

add
~~~

insert
~~~~~~

remove
~~~~~~

modify
~~~~~~

(Re)build
~~~~~~~~~

Bevor der Graph benutzt werden kann muss er natürlich erstmal aufgebaut werden. 
TODO

Fixing
~~~~~~

Durch das Löschen und Hinzufügen von Songs können *Einbahnstraßen* im Graphen
entstehen. Durch dem nachgelagerten *fixing* Schritt werden diese, nach
bestimmten Regeln, entweder entfernt oder in bidirektionale Verbindungen
umgebaut.

Ausstellen von Recommendations
------------------------------

Das Ausstellen von Empfehlungen wird durch das Traversieren des Graphen
mittelseiner Breitensuche erledigt. 

Sieben von Recommendations
--------------------------

Oft es nötig die gegebenen Empfehlungen noch zusätzlich zu filtern. Das hat den
simplen Grund das im Graphen einzelne Alben einzelne *Cluster* bilden - die
Lieder auf einem Album sind unter sich sehr ähnlich. Da man aber vermeiden
möchte dass zu einem Seed-Song ein Lied vom selben Album oder gar selben
Künstler empfohlen wird müssen diese beim Iterieren über den Graphen ausgesiebt
werden.

Lernen durch die History
------------------------

Nur eine bestimmte Anzahl von Regeln wird gespeichert - zuviele Regeln würden
*historische Altlasten* immer weiter mitschleppen und der aktuelle Geschmack des
Benutzers würde nicht widergespiegelt werden.

Softwareaufbau
==============

Da wir jetzt wissen aus welchen Teilen unsere Software besteht können wir uns
Gedanken darüber machen wie diese einzelnen Teile konkret aussehen.

Maske
-----

- Beschreibung der Musikdatenbank die von außen reinkommt.
- Besteht aus einem Mapping, bei dem die keys den Namen eines Attributes
  festlegt das ein einzelner Song haben wird, das zugehörige Value legt
  den dafür zuständigen Provider, die zuständige Distanzfunktion und 
  wie stark dieses Attribut des Songs gewichtet werden soll.

Session
-------

- API Entry für alle Funktionen
- Speichert songs ab
- Speichert die Maske

Song
----

- Speichert nur values, keine

Distance
--------

- Speichert alle Teildistanzen, statt einzelne weighted Distanz.
- Macht 'explanations' leicht.


