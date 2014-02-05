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

Baukastenprinzip

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

Um die Distanzen zu speichern wird bei vielen Datamining-Projekten eine
Distanzmatrix genutzt - also eine quadratische Dreiecksmatrix in der
die Distanzen von jedem Dokument zu jedem anderen gespeichert werden.

Da das System auch für eine sehr hohe Anzahl von Songs funktionieren soll 
schließt sich die Benutzung einer Distanzmatrix allerdings von alleine aus.
Nehmen wir an ein Benutzer möchte seine Musiksammlung mit 40.000 Liedern
importieren, so bräuchten wir soviele Felder in der Matrix:

.. math:: 

    \frac{(40.000^2 - 40.0000)}{2} = 799.980.000

Nimmt man für jedes Feld einen günstig geschätzten Speicherverbrauch von 4 Byte
an, so bräuchte man allein für die Distanzmatrix hier aufgerundet 3 Gigabyte
Hauptspeicher - was selbst für diesen günstig geschätzten Fall unakzeptabel
wäre. Auch eine Sparsematrix wäre hier kaum sinnvoll da in allen Fällen ja etwas
weniger als die Hälfte aller Felder befüllt ist.

Man muss also versuchen nur eine bestimmte Anzahl von Distanzen für einen Song
zu speichern - vorzugsweise eine Menge von Songs mit der kleinsten
:term:`Distanz`. Als geeignete Datenstruktur erscheint hier ein Graph - die
Knoten desselben sind die Songs und die Kanten dazwischen die Distanzen.

TODO: Erläuterung: kNN Graph

Graphenoperationen
------------------

Um mit unseren Graphen arbeiten zu können müssen wir einige Operationen auf ihm
definieren:

add
~~~

Füge einen einzelnen Song zu dem Graphen hinzu, verbinde ihn aber noch nicht.
Dies ist die bevorzugte Operation um viele Songs dem Graphen hinzuzufügen -
beispielsweise am Anfang - da das Verbinden später in einem Schritt erledigt
werden kann.

insert
~~~~~~

Fügen einen einzelnen Song zu dem Graphen hinzu und verbinde ihn. Suche dazu
erst eine passende Stelle in der eingepasst wird.

remove
~~~~~~

Entferne einen einzelnen Song aus dem Graphen und versuche das entstandene
*Loch* zu flicken indem die Nachbarn des entfernte Songs untereinander
verkuppelt werden.

``modify``
~~~~~~~~~~

Manchmal ist es nötig das Attribut eines einzelnen Songs - wie beispielsweise
das **Rating** - zu ändern. 

``rebuild``
~~~~~~~~~~~

Bevor der Graph benutzt werden kann muss er natürlich erstmal aufgebaut werden. 
TODO

Fixing
~~~~~~

Durch das Löschen und Hinzufügen von Songs können *Einbahnstraßen* im Graphen
entstehen. Durch dem nachgelagerten *fixing* Schritt werden diese, nach
bestimmten Regeln, entweder entfernt oder in bidirektionale Verbindungen
umgebaut.

Ausstellen von Empfehlungen
---------------------------

Das Ausstellen von Empfehlungen wird durch das Traversieren des Graphen
mittelseiner Breitensuche erledigt. 

Filtern von Empfehlungen
------------------------

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


