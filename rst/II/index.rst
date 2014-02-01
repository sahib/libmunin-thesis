********
Einstieg
********

.. epigraph::

    '' *Hart wie ein Windhund, flink wie Leder und zäh wie Kruppstahl - oder so.* ''

    -- *Der Österreicher*

.. figure:: figs/munin_startup.*
    :alt: Allgemeine Benutzung
    :width: 75%
    :align: center

    Allgemeine Benutzung von libmunin

Einsatzszenarien
================

Denkbare Einsatzszenarien wären:

    1. Einsatz in Mediaplayern für große lokale Musiksammlungen.

        Manche Leute haben fei echt das Problem dass die Musiksammlung zu groß
        ist - und sie oft nur eine kleine Gruppe davon hören. Hier wäre eine
        dynanmische Playlist die je nach Lust und Laune bestimmte passende Bands
        vorschlägt.

        TODO: ernst. 

    2. Einsatz bei music streaming plattformen als backend.

        Music streaming plattformen wie last.fm, pandora, spotify.

    3. Einsatz bei music verkäufern - um ähnliche artikel vorzuschlagen.
    4. Einsatz bei DJ Software um eine Auswahl für die nächsten Stücke zu erzeugen. 
    5. Einsatz bei webradios.
    6. Einsatz in sozialen Netzwerken.
    7. ...weitere Einsatzmöglichkeiten sind denkbar.

http://de.wikipedia.org/wiki/Empfehlungsdienst

Vorhandene Arbeiten
===================

Wie bereits eingangs erwähnt gibt es eine zwar noch überschaubare aber doch
schon recht umfangreiche Menge an Arbeiten zum Thema *Music Recommendation*.
Hier werden examplarisch einige Arbeiten gezeigt die einige interessante
Herangehensweisen vorstellen:

... scho. Zuhauf. Aber welche? TODO

Vorhandene Alternativen
=======================

Wenn man vermeiden will das Rad neu zu erfinden ist es hilfreich sich vorhandene
Alternativen anzuschauen und deren Herangehensweise an das Problem. Es werden
einige ausgewählte Plattformen aller Couleur gezeigt und deren Funktionsweise
und Besonderheiten kurz erklärt.


Plattformen
-----------

Im Gegensatz zu einfachen Webseiten sind diese Plattformen auch meist über
Desktopanwendungen nutzbar und bieten eine API. TODO

TODO: Nachweise, Screenshots.

- **last.fm** (http://www.last.fm)

    Der wohl bekannteste Musik Empfehlungs Service im Netz. User können sich mit
    ihren Account ein personalisiertes Webradio (auch *Station* genannt)
    zusammenstellen. Dabei wählen sie ein Lied auf der Seite aus und lassen sich
    darauf basierend dann weitere Lieder oder Künstler vorschlagen die in eine
    ähnliche Richtung gehen. Für viele Musicplayer gibt es Plugins die die
    gespielten Lieder zu last.fm übermitteln. Diesen Vorgang nennen die
    Betreiber *scrobbeln*. Durch diese Informationen werden dann spezialisierte
    Empfehlungen getroffen - es handelt sich also um ein lernendes System.

     [screenshot]

- **YouTube** (http://www.youtube.de)

    Youtube ist vorrangig als Videoplattform bekannt, durch ihre enorme
    Beliebtheit laden dort Nutzer allerdings auch Musik - verpackt als Video -
    hoch. Interessant dabei ist dass in der Sidebar stets Empfehlungen für
    weitere Videos angezeigt - in den meisten Fällen dann auch weitere
    Musikvideos. Dabei haben die meisten Videos auch etwas mit dem aktuellen zu
    tun - nur einige der ersten Empfehlungen sind die ,,Trending Videos''.

    Einige der Attribute die in die Empfehlung mit eingehen:

        * Video-Metadaten (Qualität, Beschreibung, Titel)
        * Upload-Datum
        * ,,Plays'' und tatsächliche ,,Plays'' (also ob das video lang genug
          angeschaut wurde)
        * ...

     [screenshot]

- **MySpace**

     Obwohl das soziale Netzwerk myspace seine besten Tage hinter sich hat haben
     viele Bands noch auf der Seite ein Profil unter dem man sich oft kostenlos
     Musik anhören kann. Ähnlich wie bei anderen populären sozialen Netzen kann
     man diese Seite *liken*. Diese Information wird dann dafür genutzt einem
     User Bands vorzuschlagen die auch seine Freunde mögen - unter der Annahme
     dass die Freunde einen ähnlichen Musikgeschmack haben.

     [screenshot]

- amazon

     Den Grundstein für die Empfehlungen bei amazon bilded die Warenkorbanalyse.
     Dabei werden die Warenkörbe der User analysiert und es werden
     Assoziationsregeln erstellt - bevorzugtermaßen Regeln die unerwartete
     Zusammenhänge aufdecken. Das typische Beispiel ist dabei: ,,Wer Bier kauft,
     kauft auch Windeln''. Diese Regeln werden dann genutzt um neue Artikel für
     bestimmte Artikel vorzuschlagen. Natürlich fließt auch die personalisierte
     Shopping-Historie in die Empfehlunge mit ein.

     Zudem hat amazon im vergleich zu den oben genannten Plattformen den Vorteil
     dass der Kauf eines Artikels ein klare Absichtserklärung ist - bei
     Plattformen wie Youtube schaut man hingegen ein Video oft aus Neugier an 
     obwohl dieses möglicherweise nicht in das Muster des Users passt.

     [screenshot]

Webseiten
---------


**tastekid** (http://www.tastekid.com/)

    Bei den bisherigen Plattformen wurde meist nur eine Art von Items jeweils 
    vorgeschlagen, anders bei dieser Webseite. Man kann einen beliebigen Begriff
    eingeben und die Seite wird versuchen diesen Begriff einer *Sache*
    zuzuordnen und basierend daraufhin ähnliche Sachen vorschlagen.

    TODO: Oh gott. Droooogen.

    Eine interessante Idee ist dabei dass die Resultate auch begründet werden -
    so wird die Suche nach ,,The Beatles'' folgendermaßen begründet: 

        [screenshot]


**Musicovery** (http://musicovery.com/)

    Diese Seite kategorisiert eine groß Anzahl von Musikstücken nach Stimmung
    (*dunkel* bis *positiv*) und Temp (*ruhig* bis *energiegeladen*). Diese zwei
    Attribute werden an den Achsen eines Koordinatensystems aufgetragen. So
    erhält der User eine Möglichkeit einen Punkt darin zu selektieren und
    basierend auf diesen Eigenschaften sich Empfehlungen liefern zu lassen.

    [screenshot von moodmap]
    
    Der sonstige Hauptzweck der Seite besteht aus der *Music Discovery* (daher
    auch das Kofferwort aus *Music* und *Discovery* als Name).  Ein Beispiel
    dafür ist die sogenannte *MusicMap* - ein Koordinatensystem bei dem auf der
    X-Achse die Zeit (1960 - 2010) und nach oben das Verhältnis von *Likes* zu
    *Dislikes*. Mit anderen Worten: Liegt ein Punkt etwa in der Mitte der Höhe
    so mochten ihn genauso viele Leute wie sie ihn nicht mochten. Je weiter weg
    man von der Mitte ist desto einiger sind sich die User ob der Song gut oder
    schlecht ist.

    [screenshot von music map]


Software-Bibliotheken
---------------------

Während die Anzahl der Plattformen noch ins unermeßliche ging, so liefert eine
suche nach *Music Recommendation (Library|System|Engine)* schon deutlich weniger
Resultate. Es scheint keine etablierte Bibliothek zu geben die dieses Problem
angeht.

- **mirage**

    Eine freie in der Programmiersprache C# (mithilfe von Mono) implementierte
    Bibliothek für Music Recommendations. Sie kommt den Zielen des Autors am
    nähesten ist aber wenig auf große Datenbanken ausgelegt und stützt sich
    allein auf Audio-Analyse - dazu wird während des *Kaltstartes* die gesamten
    Audiodaten der Musiksammlung analysiert.

    Sie ist momentan nur im freien Mediaplayer Banshee als Plugin nutzbar. 
    *Banshee* selbst ist ebenfalls in C# geschrieben - die Wahl der
    Programmiersprache ist für die Bibliothek also von nicht geringer Bedeutung.

    Webseite: http://hop.at/mirage/

- **mufin audiogen**

    Eine kommerzielle in C++ entwickelte Bibliothek die im (mittlerweile
    eingestellten) Mufin-Audioplayer verwendet wurde. Sie bietet - laut der
    Werbebroschüre - enorm viele  Features und hat nicht das Problem des
    *Kaltstartes*. Das soll heißen: Die Musikdatenbank muss nicht erst aufwändig
    importiert werden was zu einem, sondern es können gleich Empfehlungen
    getroffen werden.

    Zudem sind Visualisierungen und mobile Anwendungen mit der Bibliothek
    möglich.

    Webseite: http://www.mufin.com/products/audiogen/   

Zusammenfassung
---------------

Folgende Ideen sind übernehmenswert:

    lernendes System, nutzer-erfahrung (last.fm)
    Einbeziehung von Metadaten (youtube)
    warenkorbanalyse zum lernen nutzen (amazon)
    soziele empefhlung (myspace)
    mood basiert (musicovery) / audio analyse (mirage)
    graphen basiert (mufin)

Stolpersteine die man vermeiden sollte:

    Kaltstart (mufin)
    Große Datenmengen (mirage)
    Programmiersprache (mirage)
    Keine Abhängigkeit von Audiodaten (mirage)

Ziele
=====

Ziel ist ein System das folgende Fähigkeiten besitzt:

- Erstellung dynamischer, fortlaufender Playlisten.
- Lernfähigkeit.
- Mögliche "Aufsätze": Erst lookup in von user vorgegebener recommendation db,
                       dann erst automatisch via libmunin.
- Stark anpassbare API, da diese alle möglichen spezialfälle abdecken muss,
  und auf die unterschiedlichen formate der musiksammlungen eingestellt sein
  muss.

Zielgruppe
==========

*libmunin* soll eine Bibliothek für Entwickler sein. Es stellt also keine
einfach zu nutzende Webseite bereit wie die oben genannten - es kann aber als
Backend dafür dienen.

- In früher Phasen: Hauptsächlich interessierte entwickler mit viel geduld.
- Erster interessierter Entwickler wird der Entwickler von moosecat sein.
- Möglichkeit: in mopidy einbauen, dort wird auch ein dynamic playlist 
  feature "gesucht".
- Sobald in "Otto-normal-player": Auch normale anwender mittels DBUS Service und
  cli tool. Momentan eher sperrig benutzbar. 

Primär sind allerdings experimentierfreudige Entwickler die Zielgruppe

Anforderungen
=============

Aus den oben genannten Zielen und Einsatzszenarien können 
*Anforderungen* abgeleitet werden die das fertige System erfüllen muss. 

Dabei wird zwischen **technischen Anforderungen** und **weichen Anforderungen**
unterschieden - erstere sind atomar, sprich sie können ganz oder gar nicht
erfüllt werden, letztere können partiell erfüllt werden.

Technische Anforderungen
------------------------

#. Ausstellen von Empfehlungen muss performant möglich sein.

    Da später sehr viele Anfragen, unter Umständen gleichzeitig, an das System
    gestellt werden darf auch eine Abfrage von 100 Empfehlungen nicht länger 
    als eine Sekunde dauern.

    Die eigentliche Arbeit muss daher in einem vorgelagerten Analyse-Schritt 
    erfolgen und die daraus gewonnenen Kenntnisse in einer geeigneten
    Datenstruktur gespeichert werden.

#. Empfehlungen bilden eine Kette.

    Wird eine Anfrage an das System gestellt so wird ein Iterator zurückgegeben
    der alle dem System bekannten Songs nach Relevanz absteigend sortiert ausgibt. 

#. Handhabung großer Datenmengen.

    Groß definiert sich hierbei durch das Einsatzszenario. Bei privaten
    Musiksammlungen beträgt die maximale Größe die problemlos unterstützt werden
    soll bis zu 40.000 Lieder. 
    
    Größere Datenmengen, wie sie vlt. bei Webradios vorkommen, sollen auch unterstützt
    werden. Hier ist allerdings dann ein höherer Rechenaufwand gerechtfertigt.

Weiche Anforderungen
--------------------

#. Die bereitgestellte API muss auf die stark variierende Qualität und Form von
   Musiksammlungen eingestellt sein. 

     Viele existierende Musiksammlungen sind unterschiedlich gut mit Metadaten 
     (*Tags*) versorgt. So sind manche Tags gar nicht erst vorhanden oder sind
     je nach Format und verwendeten Tagging-Tool/Datenbank anders benannt.

     Auch soll das fertige System mit Szenarien zurecht kommen wo lediglich die 
     Metadaten der zu untersuchenden Songs zur Verfügung stehen, aber nicht die
     eigentlichen Audio-Daten. Dies kann beispielsweise vorteilhaft in Fällen
     sein bei denen man die Lieder nicht selbst besitzt aber Zugriff auf
     Musikdatenbanken wie *MusicBrainz*.

#. Das System soll von mehreren Programmiersprachen aus benutzbar sein.

     Dieses Ziel könnte entweder durch verschiedene Languagebindings erreicht
     werden, oder alternativ durch eine Server/Client Struktur mit einem
     definierten Protokoll in der Mitte.

     Portabilität ist für das erste zweitrangig.
     Für den Prototypen sollen lediglich unixoide Betriebssysteme, im speziellen
     Arch Linux, unterstützt werden.

#. Eine Demonstrations-Anwendung sollte entwickelt werden die auch zur
   Fehlersuche, Verbesserung und als Einsatzbeispiel dient.

     Als Demo-Anwendung eignet sich ein Musicplayer der dem Nutzer mithilfe des
     zu entwickelnden System Musikstücke vorschlägt und optimalerweise diese 
     Empfehlung auch *begründen* kann. Daher soll diese Anwendung auch als
     *Debugger* dienen.

     Die Demonanwendung sollte dabei auf den freien MPD-Client *Moosecat*
     aufsetzen.

     .. admonition:: Exkurs zu *Moosecat*:

        Moosecat ist ein vom Auto seit 2012 entwickelter MPD-Client. Im Gegensatz zu
        den meisten, etablierten Clients hält er eine Zwischendatenbank die den
        Zustand des Servers spiegelt. Dadurch wird die Netzwerklast und die Startzeit
        reduziert und interessante Feature wie Volltextsuche wird möglich.

#. Es sollte einfach sein fehlende Daten zu beschaffen.

     In den meisten privaten Musisammlungen sind die wichtigsten Attribute
     *getaggt* - sprich in der Audiodatei sind Werte wie *Artist*, *Album* und
     *Titel* hinterlegt. Manche Attribute sind allerdings schwerer zu bekommen,
     wie beispielsweise die *Lyrics* zu einem bestimmten *Titel* oder auch das
     *Genre* eines Albums 

     Es sollte aus Komfortgründen auf einface Art und Weise möglich sein externe
     Bibliotheken zur Datenbeschaffung in *libmunin* einzubinden.
    
     .. admonition:: Exkurs zu *libglyr*:

         TODO

Entwicklungsumgebung
====================

Alle Quellen die während dieses Projektes entstanden sind finden sich auf
der sozialen Code-Hosting Plattform Github. User können dort interessante 
Projekte *starren* - bis jetzt hat *libmunin* für seine recht kurze Lebensspanne 
ein recht hohe Zahl von *Stars*: 15. (TODO: srsly?)


Die dazugehörige Dokumentation wird bei jedem commit automatisch aus den
Sourcen, mittels des freien Dokumentationsgenerators Sphinx,
auf der Dokumentations-Hosting Plattform *ReadTheDocs* gebaut und dort
verfügbar gemacht: https://libmunin.rtfd.org

Zudem werden pro Commit unittests auf der Continious-Integration Plattform
*TravisCI* für verschiedene Python-Versionen durchgeführt.
Dies hat den Vorteil dass fehlerhafte Versionen aufgedeckt werden,
selbst wenn man vergessen hat die unittests lokal durchzuführen.

Schlägt der Build fehl so färben sich kleine Buttons in den oben genannten
Diensten rot und man wird per Mail benachrichtigt. TOOD: ref down.

.. figure:: figs/travis_badge.png
    :align: center
    :alt: Screenshot der Statusbuttons auf der Github-Seite.

    Screenshot der Statusbuttons auf der Github-Seite.

Versionen die als stabil eingestuft werden, werden auf *PyPi (Python Package Index)*
veröffentlicht, wo sie mithilfe des folgenden Befehles samt
Python-Abhängigkeiten installiert werden können:

.. code-block:: bash

    $ sudo pip install libmunin

Auf lokaler Seite wird jede Änderungen versioniert, um die Fehlersuche zu
vereinfachen - im Notfall kann man stets auf funktionierende Versionen
zurückgehen. 

Der Quelltext selber wird in gVim geschrieben. Dass sich der Python-Quelltext
dabei an die gängigen Konventionen hält wird durch die Zusatzprogramme *PEP8* und
*flake8* überprüft.
