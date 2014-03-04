********
Einstieg
********

Zielsetzung
===========

:dropcaps:`Wo` ist also das konkrete Problem, dass *libmunin* nun lösen soll?
Das erklärte Ziel ist es eine Bibliothek zu schaffen, die
einen auf Musik spezialisierten *Empfehlungsdienst* implementiert. 
Allgemein gesprochen ist ein *Empfehlungsdienst* ein Dienst, der zu bestimmten
Objekten ähnliche Objekte vorschlägt. Zur Ermittelung der ähnlichen Objekte
nutzt er Metadaten welche die einzelnen Objekte beschreiben. Die Metadaten
werden durch Methoden des *Information--Retrieval* besorgt und durch Methoden
des *Data--Minings* analysiert werden. Zudem wird während der Laufzeit der Nutzer
beobachtet um spätere *exaktere* Empfehlungen abzugeben.

In unserem konkreten Fall soll also ein Prototyp eines *Empfehlungsdienstes*
entwickelt werden bei dem die oben genannten *Objekte* einzelne *Lieder*
darstellen. 

Einsatzmöglichkeiten eines auf Musik spezialisierten *Empfehlungsdienstes*:

    #. Einsatz in Mediaplayern für große, meist lokale Musiksammlungen.
    #. Einsatz bei Music Streaming Plattformen als Backend für Empfehlungen.
    #. Einsatz bei Music Shops, um ähnliche Artikel vorzuschlagen.
    #. Einsatz bei Webradios als *DJ-Software* zur Erstellung einer automatischen, 
       intelligenten Playlist.
    #. Einsatz in sozialen Netzwerken, um Menschen mit ähnlichem Musikgeschmack
       zu finden.
   
Ein zusätzlicher Vorteil: Man entgeht einerseits der Werbung, die bei den
meisten Diensten  zwischen allen paar Liedern gespielt wird, andererseits ist
man nicht einer Vorauswahl der Musiklabels unterworfen --- denn meist wird nur die
momentan *populäre* Musik bei den oben genannten Plattformen gespielt. Zudem ist
diese Musik kommerzieller Natur --- freie, *Creative Commons* lizenzierte Musik,
wie man sie beispielsweise auf Jamendo [#f3]_ findet, sucht man anderswo
vergebens.

Weitere Einsatzmöglichkeiten sind natürlich denkbar, und sind bei kreativen
Nutzern zu erwarten. 

Vorhandene Alternativen
=======================

Um Fehler zu vermeiden, die andere bereits gemacht haben, betrachten wir einige
Alternativen und deren Herangehensweise an das Problem. Es werden einige
ausgewählte Plattformen aller Couleur gezeigt und deren Funktionsweise und
Besonderheiten kurz erklärt.

Bekannte Plattformen
--------------------

TODO: Nachweise!

**last.fm:** :cite:`9NT` Der wohl bekannteste Musik Empfehlungs--Service im Netz.
Benutzer können sich mit ihren Account ein personalisiertes Webradio (auch
*Station* genannt, siehe Abb. :num:`fig-lastfm-webradio`) zusammenstellen. Dabei
wählen sie ein Lied auf der Seite aus und lassen sich darauf basierend dann
weitere Lieder oder Künstler (siehe Abb. :num:`fig-lastfm-similar-artists`)
vorschlagen, die in eine ähnliche Richtung gehen. Für viele Musicplayer gibt es
Plugins, die die gespielten Lieder zu last.fm übermitteln. Diesen Vorgang nennen
die Betreiber *scrobbeln*. Durch diese Informationen werden dann spezialisierte
Empfehlungen getroffen --- es handelt sich also um ein lernendes System.

.. subfigstart::

.. _fig-lastfm-similar-artists:

.. figure:: figs/lastfm_similar_artists.png
    :alt: Ähnliche Künstler auf last.fm
    :width: 75%
    :align: center 
    
    Anzeige ähnlicher Künstler auf last.fm

.. _fig-lastfm-webradio:

.. figure:: figs/lastfm_spotify_radio.png
    :alt: Eine *Station* auf Spotify
    :width: 100%
    :align: center
    
    Eine *Station* zu der Band Knorkator, auf Spotify (Empfehlungen von last.fm)

.. subfigend::
    :width: 0.5
    :alt: last.fm Demonstration
    :label: fig-lastfm
 
    Screenshots von Last.fm. 

**YouTube:** :cite:`WNN` Youtube ist vorrangig als Video--Plattform bekannt,
durch die enorme Beliebtheit laden dort Nutzer allerdings auch Musik ---
verpackt als Video --- hoch. Interessant dabei ist, dass in der Sidebar stets
Empfehlungen für weitere Videos angezeigt (siehe Abb. :num:`fig-youtube`) werden
--- in den meisten Fällen dann auch weitere Musikvideos. Dabei haben die
(meisten) Videos auch etwas mit dem Aktuellen zu tun.

Einige der Attribute die in die Empfehlung mit eingehen:

    * Videometadaten (Qualität, Beschreibung, Titel)
    * Upload--Datum
    * ,,Plays" und tatsächliche ,,Plays" (also ob das Video lang genug
      angeschaut wurde)

.. _fig-youtube: 

.. figure:: figs/youtube_sidebar.png
    :alt: Sidebar eines Youtube Videos
    :width: 80%
    :align: center

    Die Vorschläge zu einem Musikvideo auf YouTube

**Myspace:** :cite:`MYS` Obwohl das soziale Netzwerk Myspace seine besten Tage hinter sich hat, haben
viele Bands noch auf der Seite ein Profil unter dem man sich oft kostenlos
Musik anhören kann (siehe Abb. :num:`fig-myspace`). Ähnlich wie bei anderen
populären sozialen Netzen kann man diese Seite *liken*. Diese Information
wird dann dafür genutzt einem Benutzer Bands vorzuschlagen, die auch seine
Freunde mögen --- unter der Annahme dass die Freunde einen ähnlichen
Musikgeschmack haben.

.. _fig-myspace:

.. figure:: figs/myspace_queue.png
    :alt: Die Playlist von MySpace 
    :width: 50%
    :align: center

    Die Vorschläge die MySpace basierend auf den ersten Song macht.

**Amazon:** :cite:`XXX` Den Grundstein für die Empfehlungen bei Amazon bildet die
Warenkorbanalyse.  Dabei werden die Warenkörbe der Benutzer analysiert und es
werden Assoziationsregeln erstellt --- bevorzugtermaßen Regeln, die unerwartete
Zusammenhänge aufdecken. Ein Kauf ist auch eine klarere *Absichtserklärung* als
zB. ein Klick auf *YouTube*. Das typische Beispiel ist dabei: *,,Wer Bier kauft,
kauft auch Windeln"*. Diese Regeln werden dann genutzt um neue Artikel für
bestimmte Artikel vorzuschlagen (siehe Abb. :num:`fig-amazon`).  Natürlich
fließt auch die personalisierte Shopping--Historie in die Empfehlungen mit ein.

.. _fig-amazon: 

.. figure:: figs/amazon_recommendations.png
    :alt: Empfehlungen von Amazon.com 
    :width: 100%
    :align: center

    Zu fast jedem Artikel erhält man Empfehlungen was man noch kaufen
    könnte. Hier zu *Knorkator --- The Schlechtest of*

**Musicovery:** :cite:`ZMF` Diese Seite kategorisiert eine große Anzahl von
Musikstücken nach Stimmung (*dunkel* bis *positiv*) und Tempo (*ruhig* bis
*energiegeladen*). Diese zwei Attribute werden an den Achsen eines
Koordinatensystems aufgetragen. So erhält der Benutzer eine Möglichkeit einen
Punkt darin zu selektieren und basierend auf diesen Eigenschaften sich
Empfehlungen liefern zu lassen (siehe Abb. :num:`fig-musicovery-moodmap`).
    
.. _fig-musicovery-moodmap:

.. figure:: figs/musicovery_moodmap.png 
    :alt: Die Moodmap auf Musicovery.com
    :width: 60%
    :align: center

    Die Moodmap auf Musicovery.com

Der sonstige Hauptzweck der Seite besteht aus der *Music Discovery* (daher
auch das Kofferwort aus *Music* und *Discovery* als Name) --- also dem
Entdecken neuer Musik.  

Software--Bibliotheken
----------------------

Während die Anzahl der Plattformen noch ins Unermeßliche ging, so liefert eine
Suche nach *Music--Recommendation-(Library|System|Engine)* schon deutlich weniger
Resultate. Es scheint keine etablierte Bibliothek zu geben, die dieses Problem
angeht. Nach einiger Suche ließen sich zumindest zwei Projekte finden:

**Mirage:** :cite:`AHX` Eine freie in der Programmiersprache
:math:`\mathrm{C{\scriptstyle\overset{\#}{\vphantom{\_}}}}` (mithilfe von Mono
:cite:`MNO`) implementierte Bibliothek für *Music Recommendations*. Sie kommt
den Zielen des Autors am nähsten, ist aber wenig auf große Datenbanken ausgelegt
und stützt sich allein auf Audioanalyse --- dazu wird während des *Kaltstartes*
die gesamten Audiodaten der Musiksammlung analysiert.

Sie ist momentan nur im freien Mediaplayer Banshee als Plugin nutzbar.
*Banshee* selbst ist ebenfalls in
:math:`\mathrm{C{\scriptstyle\overset{\#}{\vphantom{\_}}}}` geschrieben --- die
Wahl der Programmiersprache ist für die Bibliothek also von nicht geringer
Bedeutung.

**Mufin Audiogen** :cite:`UZB` Eine kommerzielle, in
:math:`\mathrm{C/C{\scriptstyle\overset{\!++}{\vphantom{\_}}}}` entwickelte
Bibliothek, die im (mittlerweile eingestellten) *Mufin--Audioplayer* verwendet
wurde. Sie bietet --- laut der Website --- enorm viele, teils fragwürdige oder
unklare, Features und hat nicht das Problem des *Kaltstartes*. Das soll heißen:
Die Musikdatenbank muss nicht erst aufwändig importiert werden, sondern es
können gleich Empfehlungen getroffen werden.

Zudem sind Visualisierungen und mobile Anwendungen mit der Bibliothek möglich.

Vorhandene Arbeiten
===================

Wie bereits Eingangs erwähnt gibt es eine zwar noch überschaubare aber doch
schon recht umfangreiche Menge an Arbeiten zum Thema *Music Recommendation*.

Einige ausgesuchte Arbeiten werden  im folgenden aufgelistet und deren
Kernaussagen im Bezug auf dieses Projekt erläutert:

* *A self-organizing map based knowledge discovery for music recommendation systems* :cite:`vembu2005self`

    Statt den Computern die Ähnlichkeit zwischen zwei Liedern bestimmen zu
    lassen verwendet diese Arbeit Reviews von *Amazon* um daraus Beziehungen
    zwischen Künstlern abzuleiten.

    Dieser Ansatz fällt unter *Social-based Recommendations* --- man nutzt also
    das Wissen vieler Menschen um Ähnlichkeiten abzubilden. Dies steht im
    Gegensatz zu *Content-based Recommendations* --- bei diesen wird die
    Ähnlichkeit anhand von Audio- und Metadaten automatisch ermittelt.

    *Vorteil:* Elegant und oft sehr akkurat.

    *Nachteil:* Unvollständig, nicht für jeden Künstler ist eine Empfehlung vorhanden.

* *Smart radio-building music radio on the fly* :cite:`hayes2001smart`

    Tendenziell steigt die Nutzung von Streamingdiensten immer mehr an --- viele
    Nutzer verwalten ihre Musik nicht mehr lokal, sondern streamen diese, meist
    gegen einen bestimmten Betrag, aus dem Netz.

    Daraus kann man ableiten, dass es zukünftig noch mehr dieser
    Streamingdienste geben wird --- ein typisches Einsatzszenario für *libmunin*.

* *A music search engine built upon audio-based and web-based similarity measures* :cite:`knees2007music`

    Das in diesem Paper vorgestellte System kommt der Vorstellung von *libmunin*
    am Nähestem. Die Audio- und Metadaten der einzelnen Lieder wird analysiert
    und abgespeichert. Fehlende Metadaten werden automatisch aus dem Netz
    bezogen (*Reviews* und *Lyrics*). Statt die Musikstücke aber zueinander in
    Relation zu setzen, werden die Informationen für eine skalierbare
    Suchmaschine benutzt, die basierend auf natürlicher Sprache (Beispielsuche:
    *rock with great riffs*) passende Lieder findet.

* *Music for my mood* :cite:`lee2006music`

    Die Ähnlichkeit zwischen zwei Stücken wird über die *Stimmung*, welche durch
    Audioanalyse bestimmt wird, in einem Lied definiert. 

.. _schlussfolgerungen:

Schlussfolgerungen
==================

Folgende Ideen erschienen übernehmenswert (*Quellen in Klammern*):

* Ein System welches von seinen Nutzern lernt *(last.fm)*
* Umfangreiche Einbeziehung von Metadaten *(YouTube)*
* Nutze zum Lernen die ,,Warenkorbanalyse" um Assoziationsregeln abzuleiten. *(Amazon)*
* Nutze Audioanalyse *(Mirage)* um Ähnlichkeiten festzustellen --- beispielsweise
  die Stimmung bzw. ,,Mood" in einem Lied. (*Musicovery*)
* Graphen als interne Datenstruktur (*mufin audiogen*)

Es ist natürlich empfehlenswert aus den ,,Fehlern" anderer zu lernen, daher
sollte man folgende Probleme beim Design und der Implementierung berücksichtigen:

* *Kaltstart*, also die Verzögerung beim ersten Start, möglichst klein halten
  *(mufin audiogen)*
* Verwaltung großer Datenmengen sollte möglich sein *(Mirage)*
* Bibliothek Programmiersprachen unabhängig halten *(Mirage)*
* Keine strikte Abhängigkeit von Audiodaten. Ein Betrieb nur mit Metadaten
  sollte möglich sein *(Mirage)*
* Libertäre Lizenz wählen um allgemeine Verfügbarkeit zu gewährleisten *(mufin
  audiogen)*

Anforderungen
=============

Nachdem man sich also das Umfeld angeschaut, hat kann man versuchen
*Anforderungen* abzuleiten die eine gute Schnittmenge aus den obigen Plattformen
und Arbeiten bildet, welche dann das System erfüllen muss.


**Performanz:** Später ist damit zu rechnen, besonders im Client- und Server--Betrieb, dass sehr
viele Anfragen gleichzeitig gestellt werden. Um lange Antwortzeiten zu
verhindern sollte, dass das Ausstellen von Empfehlungen sehr performant
erfolgen.

Die eigentliche Arbeit muss daher in einem vorgelagerten Analyseschritt 
erfolgen und die daraus gewonnenen Kenntnisse in einer geeigneten
Datenstruktur gespeichert werden. Diese soll dann beim Austellen der Empfehlung
dann einfach nur noch ausgelesen werden.


**Empfehlungen bilden eine Kette:** Wird eine Anfrage an das System gestellt, so
wird ein *Iterator* zurückgegeben der alle dem System bekannten Songs nach
Relevanz absteigend sortiert ausgibt. 


**Handhabung großer Datenmengen:** Bei vielen Datamining--Anwendungen ist die
Menge der *Dokumente* der Flaschenhals --- in unserem Fall also sind die
*Dokumente* einzelne *Lieder*.  Herkömmliche private Musiksammlungen können
bereits Größen von Zehntausend Liedern erreichen.  Betreiber von
Streaming--Plattformen haben noch weitaus größere Datenmengen. 


**Lizenz:** Die Lizenz sollte einen libertären Einsatz ermöglichen und
sicherstellen, dass Weiterentwicklungen in das Projekt zurückfließen.
Die GPLv3 Lizenz erfüllt diese Bedingungen. Der kommerzielle Einsatz ist
erwünscht.


**Begründbarkeit:** Empfehlungen sollen begründbar sein.
Es muss möglich sein festzustellen welche Merkmale eines Songs zu der Empfehlung
geführt haben.


**Anpassungsfähige API:** Die bereitgestellte API muss auf die stark variierende
Qualität und Form von Musiksammlungen eingestellt sein.  Viele existierende
Musiksammlungen sind unterschiedlich gut mit Metadaten (*Tags*) versorgt. So
sind manche Tags gar nicht erst vorhanden oder sind je nach Format und
verwendeten Taggingtool/Datenbank anders benannt.

Das fertige System soll mit Szenarien zurecht kommen, wo lediglich die 
Metadaten der zu untersuchenden Songs zur Verfügung stehen, aber nicht die
eigentlichen Audiodaten. Dies kann vorteilhaft sein, wenn man keinen Zugriff auf
die Audiodaten hat, aber die Metadaten bei Musikdatenbanken wie *MusicBrainz*
vervollständigen kann.


**Unabhängigkeit von Programmiersprache:** Das System soll von mehreren
Programmiersprachen aus benutzbar sein.  Dieses Ziel könnte entweder durch
verschiedene *Languagebindings* erreicht werden, oder alternativ durch eine
Server/Client Struktur mit einem definierten Protokoll in der Mitte.

Portabilität ist für das erste zweitrangig.  Für den Prototypen sollen lediglich
unixoide Betriebssysteme, im speziellen *Arch Linux* :cite:`JV6`, dem
bevorzugten Betriebssystem des Autors, unterstützt werden.


**Demonstrations und Debuggeranwendung:** Eine Demonstrationsanwendung soll
entwickelt werden, die zur Fehlersuche, Verbesserung und als Einsatzbeispiel
dient.  Als Demonstrationsanwendung eignet sich ein Musicplayer der dem Nutzer
mithilfe des zu entwickelnden System Musikstücke vorschlägt und diese Empfehlung
auch *begründen* kann. So kann die Anwendung auch als *Debugger* für Entwickler
von *libmunin* dienen.

Die Demoanwendung sollte dabei auf dem freien MPD-Client *Moosecat* :cite:`JH7`
aufsetzen.  Moosecat ist ein vom Autor seit 2012 entwickelter GPLv3 lizensierter
MPD-Client. Im Gegensatz zu den meisten, etablierten Clients hält er eine
Zwischendatenbank, die den Zustand des Servers spiegelt. Dadurch wird die
Netzwerklast und die Startzeit reduziert und interessante Feature wie
Volltextsuche wird möglich.  Er wird in *Python,* *Cython* und *C* entwickelt
und befindet sich noch im Entwicklungsstadium. 


**Einfaches Information Retrieval:** In den meisten privaten
Musiksammlungen sind die wichtigsten Attribute *getaggt* --- sprich in der
Audiodatei sind Werte wie *Artist*, *Album* und *Titel* hinterlegt. Manche
Attribute sind allerdings schwerer zu bekommen, wie beispielsweise die *Lyrics*
zu einem bestimmten *Titel* oder auch das *Genre* eines Albums.

Es sollte aus Komfortgründen auf einfache Art und Weise möglich sein externe
Bibliotheken zur Datenbeschaffung in *libmunin* einzubinden.  Für diesen Einsatz
ist *libglyr* :cite:`9XU` gut geeignet.  *Libglyr* ist eine vom Autor seit Ende
2010 entwickelte C-Bibliothek Musikmetadatensuchmaschine, um schwer zu
besorgende Daten wie Lyrics, Coverart und andere Metadaten im Internet zu suchen
und optional lokal zwischenzuspeichern.  Sie ist GPLv3 lizensiert und wird unter
anderem im *GnomeMusicPlayerClient (gmpc)*, vielen Shellskripten und natürlich
in dem oben genannten *Moosecat* eingesetzt.


**Anpassungsfähigkeit an den Benutzer:** Mit der Zeit soll es *bessere*
Empfehlungen liefern als am Anfang. Es soll dabei auf explizite und auf
implizite Weise lernen. Beim expliziten Lernen gibt der Benutzer Tipps
(beispielsweise kann er eine Empfehlung bewerten), beim implizierten Lernen wird
das Verhalten des Benutzers beobachtet und daraus werden Schlussfolgerungen
getroffen.

Nichtanforderungen
-------------------

Folgendes sind keine Probleme die von *libmunin* gelöst werden müssen:

**Einpflegen manuell erstellter Empfehlungen:** Dies ist per *,,Wrapper"* um die
Bibliothek möglich.

**Social-based music recommendation:** *libmunin* soll eine rein *Content-based
music recommendation Engine* werden.  Die Ähnlichkeit zweier Datensätze wird
also algorithmisch ermittelt, anstatt auf das Wissen von Menschen
zurückzugreifen. 

Zielgruppe
==========

*libmunin* soll eine Bibliothek für Entwickler sein. Es stellt also keine
einfach zu nutzende Webseite bereit wie die oben genannten --- es kann aber als
Backend dafür dienen.

*Vom Autor selbst sind die folgenden zwei Projekte anvisiert:*


**Moosecat:** Implementierung als Plugin für *Intelligente Playlisten*.

**Shellskripte:** Mittels eines Kommandozeilen--Frontends von *libmunin* wäre ein
einfacher Einsatz in Shellskripten möglich. Das Programm könnte versuchen die
gängigsten Musiksammlungen einzulesen und auf Kommando Empfehlungen generieren.


**Mopidy:** :cite:`3W5` Da die Entwickler von Mopidy eine Möglichkeit suchen um
Dynamische Playlists zu implementieren :cite:`XVG`, wäre dies ein guter
Anlaufpunkt.  Mopidy ist eine alternative Implementierung zum *MusicPlayerDaemon
(MPD)* in Python mit erweiterten Features. Sie bietet eine Anbindung zu
Music--Streaming--Plattformen wie *Spotify*. Dabei ist es kompatibel mit den
existierenden MPD-Clients. 

.. rubric:: Footnotes

.. [#f3] Eine Streaming Plattform für freie, *Creative Commons* lizensierte Musik. :cite:`30T`
