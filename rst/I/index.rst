**********
Einleitung
**********

.. epigraph:: 

   '' *Sei froh dass du du bist, und nicht dieser Fisch.* ''

   -- *Das Lied von der Makrele, Marc Uwe Kling*
   

Motivation
==========

State of the Art
----------------

:dropcaps:`Empfehlungen` sind allgegenwärtig. Ob in sozialen Netzwerken, ob in
Webshops oder gar im Supermarkt.  Besonders im weltweitem Netz gibt es eine
Vielzahl von Plattformen die Musik anbieten, entweder zum kaufen (amazon), zum
streamen (``last.fm``, spotify, rhapsody, pandora, webradios...) oder auch um
Menschen mit ähnlichem Musikgeschmack zu finden (youtube, myspace).

All diese Plattformen bieten neben der eigentlichen Musik auch immer
Empfehlungen zu anderer Songs die der User möglicherweise ebenfalls anhören
möchte - natürlich mit dem Hintergedanken dass der User sich auch diese anhört
oder gar kauft. Kunden die neue Bands entdecken und später weitere Alben von
diesen sind natürlich ein wichtiger wirtschaftlicher Faktor.

Doch wie entstehen solche Empfehlungen eigentlich? Werden diese manuell
von den Betreibern gepflegt? Bei der großen Anzahl an ,,Waren'' wohl kaum.
Schaut sich ein System an was die User oft zusammen hören?
Kann es ein System geben das komplett automatisch arbeitet?

Die oben genannten Plattformen lösen diese Probleme auf unterschiedliche Weise.
Amazon verlässt sich dabei auf die großen Mengen an gespeicherten Warenkörben -
aus diesen werden dann Alben abgeleitet die oft zusammen gekauft werden. 
Last.fm hingegen setzt auf mehrere Strategien indem es seine Nutzer die
gestreamten Lieder raten lässt und dann deren Hörverhalten analysiert - Lieder
die nur selten ganz angehört werden, werden auch selten empfohlen.
Myspace setzt auf die Annahme dass befreundete Personen auch einen ähnlichen
Musikgeschmack haben. Spotify's Empfehlungen basieren u.a. auf Interviews mit
echten Personen.

Wie man sieht sind die Wege nahezu unendlich, das Ziel aber immer gleich:
Musik-Empfehlungen aussprechen die den Nutzer länger auf der Seite halten

Auch von wissenschaftlicher Seite ist das Problem der ,, *Music Recommendation
Engine* '' noch nicht abschließend behandelt - es gibt allerdings eine steigende
Anzahl von Arbeiten auf diesem Gebiet:

.. figtable::
    :caption: Anzahl der Arbeiten auf Google Scholar zum Suchbegriff
              ,,Music Recommendation'' aufgeteilt auf die Jahre 1994-2014.
    :alt: Arbeiten zum Thema 'Music Recommendation' über die Jahre
    :spec: | r l | r l |

    ========== ====== ========== ======
    Jahre      Anzahl Jahre      Anzahl
    ========== ====== ========== ======
    1994-2000  1      2007-2008  8
    2001-2002  4      2009-2010  9
    2003-2004  3      2011-2012  6
    2005-2006  8      2013-2014  5+  
    ========== ====== ========== ======

Und mittlerweile gibt es mit *Music Recommendation and Discovery* sogar ein 200
Seiten starkes Buch. :cite:`celma2010music`.

Was fehlt also?
---------------

Viele dieser Arbeiten präsentieren jeweils einen Weg um die Ähnlichkeit zweier 
Musikstücke zu bestimmen - viele greifen dabei auf Audioanalyse zurück, also 
beispielsweise die Bestimmung der Schnelligkeit und der Stimmung des Liedes,
oder nutzen vorhandene Metadaten um beispielsweise auf den Songtexten die Themen 
zu extrahieren die im Lied behandelt werden.

Dabei sind heutzutage die Metadaten zu den Musikstücken dank Musikdatenbank wie
*MusicBrainz* [#f1]_ leicht aufzufinden - lediglich die Audiodaten sind aus
verständlichen Gründen schwer zu besorgen.

Die nötigen Bauteile um ein System zu schaffen dass gute Musikempfehlungen zu
schaffen sind also vorhanden - nur die Umsetzung fehlt.

.. rubric:: Footnotes

.. [#f1] eine frei verfügbare Musikmetadatendatenbank. :cite:`3A3`

Wie ist die aktuelle Situation?
-------------------------------

Weit verbreitet sind bei Musicplayern ,,Dynamische Playliste'' die allerdings
bei den meisten Implementierungen bei vorhandenen Plattformen wie ``last.fm``
suchen um Musikempfehlungen auszusprechen. Das ist keineswegs eine schlechte
Lösung, da solche Dienste sehr gute Resultate liefern können.

Trotzdem ist die Abhängigkeit von externen Diensten und einer Internetverbindung
nicht immer möglich oder überhaupt wünschenswert - eine Lösung die rein auf
einen Rechner laufen kann wäre von Nöten. Gewißermaßen das Backend von
``last.fm`` für den freien (frei wie in *Free Open Source Software*) Einsatz.

Ein zusätzlicher Vorteil: Man entgeht einerseits der Werbung die zwischen allen
paar Liedern gespielt wird, andererseits ist man nicht einer Vorauswahl der
Musiklabes ausgeliefert - denn meist wird nur die momentan *populäre* Musik bei
den oben genannten Plattformen gespielt. Zudem ist diese Musik kommerzieller
Natur - freie, Creative Commons-lizensierte Musik wie man sie beispielsweise auf
Jamendo [#f2]_ zu finden ist sucht man anderswo vergebens.

Dadurch dass das entstehende System frei in den Quellen verfügbar sein soll kann
jeder daran mitarbeiten und es selbst einsetzen. Im Gegensatz zu den
existierenden Backends, wie sie beispielsweise hinter ``last.fm`` stehen, wäre
ein solches System auf Qualität optimiert - weniger auf Wirtschaftlichkeit,
sprich anstatt Empfehlungen die mehr Geld einbringen sollen nachvollziehbare
qualitative Empfehlungen möglich sein. 

Die Tatsache dass der Autor sich schon seit längerer Zeit ein ,, *echtes Dynamic
Playlist Feature* '' für den MPD Client [#f3]_ den er entwickelt wünscht trägt
natürlich auch zur Motivation bei - vor allem soll auch nach dem Abschluss
dieser Arbeit das Projekt weiterentwickelt werden. 

.. rubric:: Footnotes

.. [#f2] Eine Streaming Plattform für freie, Creative Commons-lizensierte Musik. :cite:`30T`

.. [#f3] Ein MPD Client ist eine ,, *Fernbedienung* '' für den unter Unix weit
   vebreitenden MPD (MusicPlayerDaemon).

Was hat das mit Datamining zu tun?
==================================

Sehr viel.

Namensgebung
============

Menschen neigen dazu Dingen einen Namen zu geben - im Folgenden wird unser 
Musikempfehlungssystem *libmunin* genannt.

.. epigraph::

    In Norse mythology, Hugin (from Old Norse “thought”)
    and Munin (Old Norse “memory” or “mind”)
    are a pair of ravens that fly all over the world Midgard,
    and bring information to the god Odin.

    -- http://en.wikipedia.org/wiki/Huginn_and_Muninn :cite:`wiki2014hugin`

Der Name *Munin* war bereits vergeben an ein Monitoring Tool, deswegen wurde die
library *libmunin* benannt. Das hat den humorvollen Nebeneffekt dass eine
kommerzielle Library mit ähnlichem Namen (*mufin-audiogen* :cite:`IKC`) eine
freie Alternative erhält.
