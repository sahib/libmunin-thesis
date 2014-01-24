**********
Einleitung
**********

Motivation
==========

Im weltweitem Netz gibt es eine Vielzahl von Angeboten die Musik anbieten,
entweder zum kaufen (amazon), zum streamen (``last.fm``, spotify, rhapsody,
pandora, webradios) oder auch um Menschen mit ähnlichem Musikgeschmack zu finden
(youtube, myspace).

All diese Plattformen bieten neben der eigentlichen Musik auch immer
Empfehlungen zu anderer Songs die der User möglicherweise ebenfalls anhören
möchte - natürlich mit dem Hintergedanken dass der User sich auch diese anhört
oder gar kauft. Kunden die neue Bands entdecken und diese später wieder kaufen
sind natürlich ein enormer wirtschaftlicher Faktor.

Doch wie entstehen solche Empfehlungen eigentlich? Werden diese manuell
von den Betreibern gepflegt? Schaut sich ein System an was die User oft zusammen
hören? Kann es ein System geben das komplett automatisch arbeitet?

Die Antwort auf die letzte Frage ist: Nein, es kann kein System geben dass
komplett automatisch arbeitet - zumindest keines das auf den User reagiert.
Viele existierende Plattformen lösen dieses Problem oft auf sehr
unterschiedliche Weise. (TODO: Beispiele nennen)

Auch von wissenschaftlicher Seite ist das Problem der ,, *Music
Recommendation Engine* '' noch nicht völlig behandelt - es gibt eine steigende
Anzahl von Arbeiten auf diesem Gebiet:


.. figtable::
    :caption: Anzahl der Arbeiten auf Google Scholar zum Suchbegriff
              *Music Recommendation* aufgeteilt auf Jahre.
    :alt: Wissenschaftliche Arbeiten auf die Jahre verteilt
    :spec: r l

    ==== ======
    Jahr Anzahl
    ==== ======
    1990 0
    1991 1
    ==== ======


http://scholar.google.de/scholar?q=music+recommendation+engine

(TODO: daten)

Was fehlt?
----------

Viele dieser Arbeiten präsentieren jeweils einen Weg um die Ähnlichkeit zweier 
Musikstücke zu bestimmen - viele greifen dabei auf Audioanalyse zurück, also 
beispielsweise die Bestimmung der Schnelligkeit und der Stimmung des Liedes,
oder nutzen vorhandene Metadaten um beispielsweise auf den Songtexten die Themen 
zu extrahieren die im Lied behandelt werden.

Doch gibt es de facto kein System dass diese verschiedenen Attribute vereint
oder diese Implementierung in eine allgemein nutzbare Open Source Library
verpackt.

Wie ist die aktuelle Situation?
-------------------------------

Weit verbreitet sind bei Musicplayern ,,Dynamische Playliste'' die allerdings
bei den meisten Implementierungen bei vorhandenen Plattformen wie ``last.fm``
suchen um Musikempfehlungen auszusprechen. Das ist keineswegs eine schlechte
Lösung, da solche Dienste oft bereits enorme Datenmengen zur Verfügung haben
und unter Umständen sehr gute Resultate liefern.

Trotzdem ist die Abhängigkeit von externen Diensten und einer Internetverbindung 
nicht immer möglich oder wünschenswert - eine rein clientseitige Lösung wäre also 
von Nöten.

Die Tatsache dass der Autor sich schon seit längerer Zeit so ein Feature 
für den MPD Client [#f1]_ den er entwickelt wünscht trägt natürlich auch zur Motivation 
bei - vor allem soll auch nach dem Abschluss dieser Arbeit das Projekt
weiterentwickelt werden. 

.. rubric:: Footnotes

.. [#f1] Ein MPD Client ist eine ,, *Fernbedienung* '' für den unter Unix weit
   vebreitenden MPD (MusicPlayerDaemon).

Namensgebung
============

.. epigraph::

    In Norse mythology, Hugin (from Old Norse “thought”)
    and Munin (Old Norse “memory” or “mind”)
    are a pair of ravens that fly all over the world Midgard,
    and bring information to the god Odin.

    -- http://en.wikipedia.org/wiki/Huginn_and_Muninn

Der Name *Munin* war bereits vergeben an ein Monitoring Tool, deswegen wurde die
library *libmunin* benannt. Das hat den witzigen Nebeneffekt dass eine
kommerzielle Library namens *mufin* eine freie Alternative erhält.
