********
Ausblick
********

Verbesserung der Algorithmik
============================

:dropcaps:`Im` Folgenden werden einige Ideen für mögliche Weiterenwicklungen an
den vorgestellten Algorithmen gegeben.  Einige davon sind vergleichsweise
einfach umsetzbar. Andere könnten die Grundlage für fortführende Arbeiten sein.

Audioanalyse
------------

Wie bereits erwähnt, ist *libmunin's* momentane *,,Audioanalyse"* eher simpler
Natur.  Als konkrete Vorlage für eine verbesserte Audioanalyse könnte *Mirage*
dienen. In seiner Arbeit stellt der Mirage--Autor :cite:`schnitzer2007high`
Dominik Schnitzer, einige Herangehensweisen zum performanten Vergleich von
Audiodaten vor. 

Angesichts der hohen Entwicklungsgeschwindigkeit in der Informatik und dem
*,,hohem"* Alter der Arbeit (:math:`2007`), sollte allerdings beachtet werden,
dass es bereits neuere Methoden geben könnte. Beispielsweise arbeitet Schnitzer
*nur* mit MP3--Audiodaten [#f1]_. Eine Abhilfe wäre die relativ neue Bibliothek
*libaubio*, die von *Paul Brossier* :cite:`AUBIO` entwickelt wird. Zum
Dekodieren der Audiodaten (*libaubio* erwartet bereits dekodierte PCM--Daten),
könnte das weit verbreitete Audio--Framework *GStreamer* :cite:`gstreamer`
verwendet werden.

*Aubio* könnte folgendes leisten:

- Exaktere Bestimmung des *BPM--Wertes*. Beziehungsweise könnte man auch einen
  Verlauf des *BPM--Wertes*, über das Musikstück aufzeichnen, um exaktere
  Vergleiche ziehen zu können.
- *Onset--Detection*, also das Erkennen einzelner Noten, beziehungsweise
  *Sounds* innerhalb des Musikstücks. 
- Eine direkte Möglichkeit, die Stimmung in einem Lied zu analysieren, wird
  momentan zwar noch nicht geboten, aber die dazu benötigten Informationen, wie
  die Erkennung der Tonlage zu einem bestimmten Zeitpunkt werden angeboten. 
  Die technischen Details dazu werden in :cite:`schnitzer2007high` diskutiert.

Die Bibliothek selber ist in `C` geschrieben, bietet aber eine komfortable 
Python--Schnittstelle.

Eine weitere Idee, wäre der Versuch, möglichst intelligent reine Sprachdateien
(wie *Hörbücher),* Instrumental--Lieder ohne Stimme (wie *Intros)* und normale
Musik zu unterscheiden. Oft werden zu bestimmten Titeln unpassenderweise
*Intros* vorgeschlagen, die man für gewöhnlich nur hören möchte, wenn man das
gesamte Album von vorn bis hinten anhört. Auch hier wäre ein Einsatz von
*libaubio* denkbar.

.. rubric:: Footnotes

.. [#f1] Mirage verlässt sich dabei auf bestimmte Eigenschaften von MP3,
         um die Daten schneller in seine interne Datenrepräsentation zu
         konvertieren.

Andere Provider
---------------

Wie man im Playlistenvergleich unter Kapitel :ref:`ref-playlist-compare` gesehen
hat, ist momentan der Vergleich der Metadaten, die Stärke von *libmunin*. Diese
Fähigkeit könnte noch weiter ausgebaut werden, indem die Sprache der einzelnen
Titel (denn nicht immer sind Liedtexte vorhanden) erkannt wird. Dann könnte man
mittels eines Thesaurus synonyme Titel finden. Für Python existiert mit
*TextBlob* :cite:`TEXTBLOB` hierfür eine passende Bibliothek. |br| Kommt
beispielsweise in einem Liedtitel das Wort *,,Sofa"* vor, so könnte ein Titel
mit dem synonymen Wort ,,Couch" darin vorgeschlagen werden.  Auch Taxonomien,
also ähnliche Klassifikationen, sind denkbar. Man denke hier an einem Lied,
welches das Wort *,,Katze"* enthält und ein anderes das *,,Tier"* beinhaltet.
|br| In der momentanen Implementierung wird jedes Wort im Titel, auf seinen
Wortstamm gebracht und mittels der Levenshtein--Distanzfunktion verglichen.
Diese Lösung ist zwar leicht zu implementieren, ist aber algorithmisch teuer und
verhindert lediglich Tippfehler oder leicht divergente Schreibweisen.

Auch interessant zu sehen wäre es, ob die Länge der einzelnen Stücke in
irgendeiner Form mit der Ähnlichkeit korrelieren. Hier müssten statistische
Auswertungen gemacht werden, um diesen Zusammenhang zu überprüfen. Falls sich
ein Zusammenhang zeigen sollte, ließe sich eine einfache
``DurationDistanceFunction`` schreiben, welche ähnlich lange Stücke gut bewertet.

Empfehlungen
------------

.. _fig-traverse-areas:

.. figure:: figs/traverse_areas.*
   :alt: Schematische Darstellung der idealen Traversierungsreihenfolge
   :align: center
   :width: 75%
   
   Schematische Darstellung der idealen Traversierungsreihenfolge.
   Die roten Knoten stellen die Seedsongs dar, die gelben und orangen Knoten sind
   direkte Nachbarn. Die grünen Knoten sind ,,irgendwo” dazwischen. Die
   Traversierungsreihenfolge sollte hier sein: Orange, Gelb, Grün.

Oft kommt es vor, dass es mehr als einen *Seedsong* gibt. Die momentane, simple
Herangehensweise, ist für jeden einen Iterator zu erstellen und die einzelnen
Iteratoren, im Reißverschlussverfahren zu verweben. Das ist durchaus valide, wenn
man annimmt, dass die *Seedsongs* im Graphen verteilt und alle gleich
wichtig sind. Oft ballen sich Seedsongs aber auf einem bestimmten Gebiet. 
Schematisch ist das in Abbildung :num:`fig-traverse-areas` dargestellt. Besitzen zwei
*Seedsongs* gemeinsame Nachbarn, dann sollten diese zuerst besucht werden.

Auch ist das Ausgabeformat von *libmunin* noch auf einzelne Songs als
Empfehlung beschränkt. Nicht selten möchte man jedoch eine allgemeinere
Auskunft wie *,,Gib mir einen ähnlichen Künstler/Album/Genre"*. Momentan wäre
dies nur durch Auslesen der jeweiligen Attribute aus den einzelnen Empfehlungen
möglich. Allerdings könnten hier von *libmunin* optimierte
Traversierungsstrategien implementiert werden.

Erweiterungen
=============

Die verwendeten Metadaten könnten ebenfalls erweitert werden. Für die
Ähnlichkeit sind unter Umständen auch Attribute wie der *Producer*, die
*Band--Mitglieder* oder die *Herkunft der Band* relevant. Einfache Beispiele
wären hier: ,,Wer Songs von den Ärzten hört, der hört vermutlich auch gern Farin
Urlaub Racing Team" --- natürlich unter der Annahme, dass derselbe Künstler auch
immer ähnliche Musik produziert. 

Was das Lernen von *libmunin* angeht, so sollten auch *,,negative Impulse"*
behandelt werden. Wird ein bestimmtes Lied oder gar ein Künstler sehr oft
übersprungen, könnte *libmunin* dies berücksichtigen, indem es bei der
Traversierung diesen Knoten umgeht. Alternativ wäre auch ein nachträgliches
Filtern der entsprechenden Lieder möglich.

Allgemein wäre auch eine Erweiterung von Assoziationsregeln denkbar. Momentan
verbindet eine Regel immer zwei Mengen von Songs miteinander. Alternativ könnten
aber auch verschiedene Genres, Künstler oder auch Alben in einer
Regel miteinander verbunden werden. Das Erstellen solcher  Regeln wäre relativ
einfach mit der existierenden Implementierung. Was problematisch ist, ist diese neuen
Regeln als *Traversierungshilfe* zu nutzen. 

Ein weiterer Punkt, den man beim Lernen verbessern könnte, sind die
Gewichtungen, die manuell für jedes Attribut festgelegt werden. Man könnte den
Nutzer detaillierter beobachten und sehen, nach welchem Attribut er bevorzugt
seine Lieder auswählt (beispielsweise nach Genre). Das entsprechende Attribut
könnte dann höher gewertet werden.

Auch wäre ein zusätzliches Modul möglich, das *libmunin* nutzt, um Suchanfragen
basierend auf natürlicher Sprache zu ermöglichen. So könnten Anfragen wie
*,,Happy Indie Pop"* aufgelöst werden. Im Beispiel würde sich *Happy* auf die
Stimmung beziehen, *Pop* auf das Genre und *Indie* auf einen
Independent--Künstler. Letztere Information könnte man aus der Künstlerbiografie
extrahieren. Die Biografie kann automatisch von Tools wie *libglyr* 
besorgt werden oder man greift alternativ auf Amazon--Rezensionen zurück. So
gesehen, bietet sich hier ein Erweiterungspotenzial in Richtung
*,,Social--based--Recommendations"*. Also nutzt man das Wissen von vielen
Menschen, um bestimmte Attribute zu bestimmen, anstatt diese mithilfe von Metriken
zu errechnen. 
Die eigentliche Schwierigkeit bestünde aber darin, die einzelnen Wörter
bestimmten Attributen zuzuordnen. Diese Idee basiert auf der Musiksuchmaschine
von *Peter Knees* :cite:`knees2007music`.

Fazit
=====

Momentan ist *libmunin* vor allem eine Spielwiese für verschiedene Ideen, rund um
die Frage, wie man einem Computer die Ähnlichkeit von zwei Musikstücken
feststellen lässt. Trotzdem erstellt *libmunin* selbst als Prototyp in seiner
Standardeinstellung bereits durchaus nützliche Playlisten. Aufgrund der 
kurzen Implementierungszeit für ein solches System, von etwas mehr als 3
Monaten, ist dies nach Meinung des Autors durchaus als Erfolg zu werten. 

Die größte Schwäche ist aus Sicht des Autors der langsame Kaltstart, der einen
produktiven Einsatz der Bibliothek verhindert. In punkto Weiterentwicklung,
sollte dies die höchstpriosierte Aufgabe sein.

Die Neuerung dieser Arbeit ist weniger die vorgestellte Algorithmik. Der
allergrößte Teil dieser, existiert natürlich bereits in ähnlicher Form,
verstreut über viele Softwarepakete. Die tatsächliche Neuerung ist, dass diese
Funktionalität erstmals in einer allgemein nutzbaren, freien Bibliothek
vorhanden ist.
