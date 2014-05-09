**********
Einleitung
**********

Aktueller Stand
===============

:dropcaps:`In` der, zu dieser Arbeit vorangegangenen, Projektarbeit
:cite:`aaa_cpahl` wurde die Softwarebibliothek *libmunin* implementiert.  Die
Bibliothek ist in der Programmiersprache Python geschrieben und implementiert
ein Musikempfehlungssystems auf Graphen--Basis. Der dahinterstehende Graph
bildet die Nachbarschaftsbeziehungen zwischen den einzelnen Musikstücken ab. Um
den Graphen aufbauen zu können, müssen, während des sogenannten Kaltstartes, vom
Nutzer der Bibliothek alle Songs, aus denen Empfehlungen gebildet werden soll,
mit allen relevanten Attributen eingegeben werden. Damit *libmunin* weiß, wie
die einzelnen Werte zu behandeln sind, wird jedem Attribut ein sogenannter
*Provider* und eine *Distanzfunktion* zugeordnet.

Ein Provider normalisiert einen Wert anhand verschiedener Charakteristiken.
Sein Ziel ist es, für die Distanzfunktion einfache und effizient vergleichbare
Werte zu erzeugen, da die Distanzfunktion sehr viel öfters aufgerufen wird als
der Provider. Die Distanzfunktion erzeugt dann aus diesen normalisierten Werten
eine Distanz, also ein Maß dafür, wie ähnlich diese Werte sind. Die Distanzen
gehen dabei von :math:`0` (vollkommen ähnlich) bis :math:`1` (absolut
unähnhlich). *Libmunin* implementiert eine große Anzahl von vorgefertigten
Providern und Distanzfunktionen für gängige Attribute, wie dem Genre, den
Audiodaten oder den aus den Liedtext extrahierten Schlüsselwörtern.

Aus den einzelnen Distanzen wird dann der obige Graph aufgebaut. Um aus diesen
Graphen dann Empfehlungen abzuleiten, werden einzelne Knoten, sogenannte
Seedsongs, nach bestimmten Kriterien ausgewählt. Beginnend von diesen wird eine
Breitensuche gestartet, also eine sich kreisförmig vom Seedsong ausbreitende
Traversierungstrategie. Bereits besuchte Knoten werden dabei nicht nochmal besucht. 
Die einzelnen besuchten Knoten werden, nach dem Filtern von doppelten Künstlern
und Alben, dann als Empfehlungen angenommen

Zudem lernt *libmunin* während einer Sitzung vom Nutzer, indem es die
Gewohnheiten des Nutzers beobachtet und daraus Regeln ableitet. Alle gehörten
Songs werden in einer Historie abgespeichert.  Im Vergleich zu bestehenden
Systemen ist *libmunin* nicht von den Audiodaten abhängig, sondern kann durch
seine flexible Schnittstelle auch alleine auf den Metadaten eines Stückes, wie
den Tags eines Musikstückes, operieren. Ein Tag ist eine direkt in der
Audiodatei hinterlegte Information um bestimmte Werte wie den Künstler des
Stückes zu beschreiben. Das erklärte Ziel der Bibliothek ist es, eine freie
Bibliothek zu schaffen, die sowohl offline (in Musicplayern) als auch online (in
Streamingdiensten) funktioniert und mit großen Datenmengen umgehen kann.  Durch
die GPLv3--Lizenz :cite:`gplv3` ist ein libertärer, weitläufiger Einsatz
möglich. 

Das allgemeine Problem
======================

Einem Musikempfehlungssystem liegt ein grundsätzliches Problem zugrunde:
Musik ist nur schwer vergleichbar. Fragt man mehrere Menschen, wie
*ähnlich* ein Musikstück zu einem anderem ist, so erhält man genauso viele
Antworten, wie man Fragen gestellt hat. Die Einschätzung von Musik ist eine sehr
subjektive Angelegenheit, die auch häufig zwischen Menschen Diskussionen
auslöst.  Stuft man den Künstler *Status Quo* als *Rock* ein? Oder doch eher als
*Pop?* Was zählt überhaupt noch als *Rock*? Gibt es eine, für den Computer
verständliche, Definition von *Rock*?

Wenn man jetzt noch versucht, einem Computer den Begriff der *Musikähnlichkeit*
beizubringen, so wird es noch weitaus komplizierter. Dieser kann nur objektiv
nach bestimmten Metriken entscheiden. Diese Metriken zu definieren, muss dann
wiederum die Aufgabe eines Menschen sein --- also sind auch diese wiederum
subjektiv, da sie die Vorlieben des Autors widerspiegeln. Auch können diese
Metriken nie für alle Fälle funktionieren. Ein gutes Stück
*,,Kaffeesatzleserei"* lässt sich leider nie ganz vermeiden. Daher werden in
dieser Arbeit einige Annahmen getroffen, die sich aufgrund ihrer Natur nur
schwer empirisch nachweisen lassen.  An den entsprechenden Stellen wird auf die
gemachten Annahmen hingewiesen.

Das konkrete Problem
====================

Erschwerend kommt hinzu, dass jeder Nutzer andere Vorlieben und Gewohnheiten
hat.  So gesehen, ist *libmunin* in der *,,Standardeinstellung"* ein
Musikempfehlungssystem, das genau auf einen Nutzer und dessen Vorlieben
zugeschnitten ist: Seinem Entwickler. Bibliotheksanwender können jedoch die
Bibliothek an ihre Präferenzen anpassen oder ihren Endnutzern eine Möglichkeit
geben, selbst Einstellungen vorzunehmen. So könnte man im praktischen Einsatz
die Gewichtung einzelner Attribute während der Laufzeit ändern.

Damit die Bibliotheksanwender diese Anpassungen vornehmen können, sollten sie
verstehen was intern vor sich geht. Genau darum soll es hauptsächlich in dieser
Arbeit gehen.  Es wird insbesondere auf die wichtigsten Provider und deren
Funktionalität eingegangen, wie diese sich auf die Distanzfunktionen auswirken
und wie aus den einzelnen Distanzen der komplette Graph aufgebaut wird. Zudem
wird auf die Lernfähigkeiten von *libmunin* eingegangen und die generierten
Empfehlungen werden näher betrachtet. Zu jedem vorgestellten Thema werden auch
Überlegungen angestellt, welche Verbesserungen in zukünftigen Versionen gemacht
werden können.
