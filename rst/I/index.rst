**********
Einleitung
**********

.. epigraph::

    *To be is to do, to do ist to be, doo be doo be doo.*

    -- *Frank Sinatra*

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

Die oben genannten Plattformen lösen diese Probleme auf unterschiedliche Weise.
(TODO: Beispiele)

Auch von wissenschaftlicher Seite ist das Problem der ,, *Music
Recommendation Engine* '' noch nicht völlig behandelt - es gibt eine steigende
Anzahl von Arbeiten auf diesem Gebiet:

.. figtable::
    :caption: Anzahl der Arbeiten auf Google Scholar zum Suchbegriff
              *Music Recommendation* aufgeteilt auf die Jahre 1994-2014.
    :alt: Wissenschaftliche Arbeiten zum Thema 'Music Recommendation' auf die Jahre verteilt
    :spec: r l

    ========== ======
    Jahr       Anzahl
    ========== ======
    1994-2000  1
    2001-2002  4
    2003-2004  3
    2005-2006  8
    2007-2008  8
    2009-2010  9
    2011-2012  6
    2013-2014  5+  
    ========== ======

Mittlerweile gibt es mit *Music Recommendation and Discovery* sogar ein 200
Seiten starkes Buch.  :cite:p:`celma2010music`

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
Lösung, da solche Dienste oft bereits enorme Datenmengen zur Verfügung haben und
unter Umständen sehr gute Resultate liefern.

Trotzdem ist die Abhängigkeit von externen Diensten und einer Internetverbindung
nicht immer möglich oder wünschenswert - eine rein clientseitige Lösung wäre
also von Nöten.

Die Tatsache dass der Autor sich schon seit längerer Zeit so ein Feature für den
MPD Client [#f1]_ den er entwickelt wünscht trägt natürlich auch zur Motivation
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
library *libmunin* benannt. Das hat den humorvollen Nebeneffekt dass eine
kommerzielle Library mit ähnlichem Namen (,,*mufin-audiogen*'' [#f2]_) eine
freie Alternative erhält.

.. rubric:: Footnotes

.. [#f2] http://www.mufin.com/usecase/music-recommendation/
