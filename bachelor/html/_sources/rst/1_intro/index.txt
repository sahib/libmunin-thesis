**********
Einleitung
**********

Das allgemeine Problem
======================

:dropcaps:`In` der, zu dieser Arbeit vorangegangenen, Projektarbeit
:cite:`aaa_cpahl` wurde das Musikempfehlungssystems *libmunin* implementiert.
Um Musikempfehlungen auszusprechen, muss ein solches System die Ähnlichkeit
zwischen zwei Liedern feststellen können.  Dies ist das
grundsätzliche Problem: Musik ist nur schwer vergleichbar. Fragt man mehrere
Menschen, wie *ähnlich* ein Musikstück zu einem anderem ist, so erhält man
genauso viele Antworten, wie man Fragen gestellt hat. Die Einschätzung von Musik
ist eine sehr subjektive Angelegenheit, die auch häufig zwischen Menschen
Diskussionen auslöst.  Stuft man den Künstler *Status Quo* als *Rock* ein? Oder
doch eher als *Pop?* Was zählt überhaupt noch als *Rock*? Gibt es eine, für den
Computer verständliche, Definition von *Rock*?

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
geben, selbst Einstellungen vorzunehmen. 
Damit die Bibliotheksanwender diese Anpassungen vornehmen können, sollten sie
verstehen was intern vor sich geht. Genau darum soll es in dieser
Arbeit gehen.  Hauptsächlich wird diskutiert, wie *libmunin* die Ähnlichkeit
zwischen den Attributen eines Liedes berechnet und wie aus diesen Ähnlichkeiten
ein Graph aufgebaut wird. Auch auf *libmunin's* Möglichkeit vom Nutzer zu lernen
wird eingegangen.
Zu jedem vorgestellten Thema werden auch
Überlegungen angestellt, welche Verbesserungen in zukünftigen Versionen gemacht
werden können.
