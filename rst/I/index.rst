**********
Motivation
**********

Stand der Technik
=================

:dropcaps:`Empfehlungen` sind allgegenwärtig. Ob in sozialen Netzwerken, ob in
Webshops oder gar im Supermarkt.  Besonders im weltweitem Netz gibt es eine
Vielzahl von Plattformen die Musik anbieten, entweder zum Kaufen (*Amazon*), zum
*Streamen* (``Last.fm``, *Spotify*, *Rhapsody*, *Pandora*, *u.v.m*) oder auch um
Menschen mit ähnlichem Musik Geschmack zu finden (*YouTube,* *Myspace*).

All diese Plattformen bieten neben der eigentlichen Musik auch immer
Empfehlungen zu anderen Songs die der Benutzer möglicherweise ebenfalls anhören
möchte --- natürlich mit dem Hintergedanken, dass der Benutzer sich auch diese anhört
oder gar kauft. Kunden die neue Bands entdecken und später weitere Alben von
diesen bestellen sind natürlich ein wichtiger wirtschaftlicher Faktor.

Doch wie entstehen solche Empfehlungen eigentlich? Werden diese manuell
von den Betreibern gepflegt? Bei der großen Anzahl an *,,Waren"* wohl kaum.
Schaut sich ein System an was die Benutzer oft zusammen hören?
Kann es ein System geben, das komplett automatisch arbeitet?

Die oben genannten Plattformen lösen diese Probleme auf unterschiedliche Weise.
Amazon verlässt sich dabei auf die großen Mengen an gespeicherten Warenkörben -
aus diesen werden dann Alben abgeleitet, die oft zusammen gekauft werden.
``Last.fm`` hingegen setzt auf mehrere Strategien indem es seine Nutzer die
gestreamten Lieder bewerten lässt und dann deren Hörverhalten analysiert -
Lieder die nur selten ganz angehört werden, werden auch selten empfohlen.
*Myspace* setzt auf die Annahme, dass befreundete Personen auch einen ähnlichen
Musikgeschmack haben. *Spotify's* Empfehlungen basieren teilweise auf Interviews
mit echten Personen.

Wie man sieht sind die Wege nahezu unendlich, das Ziel aber immer gleich:
Musikempfehlungen auszusprechen, die den Nutzer länger auf der Seite halten.

Zielsetzung
===========

Viele dieser Arbeiten präsentieren jeweils einen Weg, um die Ähnlichkeit zweier 
Musikstücke zu bestimmen --- viele greifen dabei auf Audioanalyse zurück, also 
beispielsweise die Bestimmung der Schnelligkeit und der Stimmung des Liedes,
oder nutzen vorhandene Metadaten, um beispielsweise aus den Songtexten die Themen 
zu extrahieren, die im Lied behandelt werden.

Dabei sind heutzutage die Metadaten zu den Musikstücken anhand von
Musikmetadatenbanken wie *MusicBrainz* [#f1]_ leicht aufzufinden --- lediglich die
Audiodaten sind aus verständlichen, legalen Gründen schwer zu besorgen.

Die nötigen Bauteile und das Wissen, um ein allgemein einsetzbares, qualitatives
Musikempfehlungssystem zu schaffen, sind also vorhanden --- nur eine frei
verfügbare Umsetzung fehlt.

Verbesserungsmöglichkeiten
==========================

Weit verbreitet sind bei Musicplayern *Intelligente Playlists* [#f2]_  die
allerdings bei den meisten Implementierungen bei vorhandenen Plattformen wie
``Last.fm`` suchen, um Musikempfehlungen auszusprechen --- was  keineswegs eine
schlechte Lösung ist, denn solche Dienste können sehr gute Resultate liefern. 

Trotzdem ist die Abhängigkeit von externen Diensten und einer Internetverbindung
nicht immer möglich oder gar wünschenswert --- eine Lösung welche rein auf
einem Rechner laufen kann wäre von Nöten --- gewißermaßen das Backend von
``Last.fm`` für den freien (frei wie in *Free Open Source Software*) Einsatz.

Dadurch dass das entstehende System frei in den Quellen verfügbar sein soll, kann
jeder daran mitarbeiten und es selbst einsetzen. Im Gegensatz zu den
existierenden Backends, wie sie beispielsweise hinter ``Last.fm`` stehen, wäre
ein solches System auf Qualität optimiert --- weniger auf Wirtschaftlichkeit,
sprich anstatt Empfehlungen die mehr Geld einbringen sollen nachvollziehbare
qualitative Empfehlungen möglich sein. 

Die Tatsache, dass der Autor sich schon seit längerer Zeit ein *,,echtes"*
Feature für *Intelligente Playlisten* für den MPD Client [#f4]_, den er
entwickelt wünscht, trägt natürlich auch zur Motivation bei --- vor allem soll
deshalb auch nach dem Abschluss dieser Arbeit das Projekt weiterentwickelt
werden. 

Namensgebung
============

Menschen neigen dazu Dingen einen Namen zu geben --- im Folgenden wird unser
geplantes Musikempfehlungssystem *libmunin* genannt.

.. epigraph::

    *In Norse mythology, Hugin (from Old Norse “thought”)*
    *and Munin (Old Norse “memory” or “mind”)*
    *are a pair of ravens that fly all over the world Midgard,*
    *and bring information to Odin.*

    -- http://en.wikipedia.org/wiki/Huginn_and_Muninn :cite:`wiki2014hugin`

Der Name *Munin* war bereits vergeben an ein Monitoring Tool, deswegen wurde die
Bibliothek *libmunin* benannt. Das hat den humorvollen Nebeneffekt, dass eine
kommerzielle Bibliothek mit ähnlichem Namen (*mufin-audiogen* :cite:`IKC`) eine
freie Alternative erhält.

.. rubric:: Footnotes

.. [#f1] *MusicBrainz* ist eine freie, populäre Online-Musikmetadaten-Datenbank. :cite:`3A3`

.. [#f2] *Intelligente Playlisten* bezeichnen Playlisten, die nach bestimmten,
   vom Nutzer vorgegebenen, Kriterien aus einer Menge von Songs fortlaufend generiert werden.

.. [#f4] Ein MPD Client ist eine *,,Fernbedienung"* für den unter Unix weit
   vebreitenden MPD (MusicPlayerDaemon).
