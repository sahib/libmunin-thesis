.. only:: latex

   .. raw:: latex

       \appendix

Abkürzungsverzeichnis
======================

.. figtable::
    :spec: >{\raggedleft\arraybackslash}p{0.25\linewidth} | p{0.65\linewidth}

    =======================  ==================================
    Abkürzung                Bedeutung
    =======================  ==================================
    **API**                  *Application Programming Interface*
    **GUI**                  *Graphical User Interface*
    **LoC**                  *Lines of Code*
    =======================  ==================================

.. only:: latex

   .. raw:: latex

       \newpage

Glossar
=======

.. glossary:: 

    Song

        Im Kontext von *libmunin* ist ein Song eine Menge von Attributen.
        Jedem Attribut ist, wie in einer Hashmap, ein Wert zugeordnet. 

        Beispielsweise haben alle Songs ein Attribut ``artist``, aber jeder
        einzelner Song kennt dafür einen bestimmten Wert.

        Desweiteren wird für jeden Song die Distanz zu einer Menge ähnlicher
        Songs gespeichert, sowie einen Integer der als Identifier dient.

    Distanz

        Eine Distanz beschreibt die Ähnlichkeit zweier Songs oder Attribute. 
        Eine Distanz von 0 bedeutet dabei eine maximale Ähnlichkeit (oder
        minimale *Entfernung* zueinander), eine Distanz von 1.0 maximale
        Unähnlichkeit (oder maximale *Entfernung*).

        Die Distanz wird durch eine :term:`Distanzfunktion` berechnet.

    Distanzfunktion

        Eine Distanzfunktion ist im Kontext von *libmunin* eine Funktion, die 
        zwei Songs als Eingabe nimmt und die :term:`Distanz` zwischen
        diesen berechnet.

        Dabei wird jedes :term:`Attribut` betrachte welchesi n beiden Songs
        vorkommt betrachtet. Für diese wird von der :term:`Maske` eine
        spezialisierte :term:`Distanzfunktion` festgelegt, die weiß wie diese
        zwei bestimmten Werte sinnvoll verglichen werden können. Die so
        errechneten Werte werden, gemäß der Gewichtung in der :term:`Maske`, zu
        einem Wert verschmolzen.

        Fehlen Attribute in einen der beiedn Songs wird für diese jeweils eine
        Distanz von 1.0 angenommen und ebenfalls in die gewichtete Oberdistanz
        eingerechnet.

        Die folgenden Bedingungen müssen sowohl für die allgemeine
        Distanzfunktion, als auch für die speziellen Distanzfunktionen gelten:
 
        *Uniformität:*
        
        .. math::

            0 \leq D(i, j) \leq 1 \, \forall \, i,j \in D

        *Symmetrie:*

        .. math::

            D(i, j) = D(j, i) \, \forall \, i,j \in D

        *Identität:*

        .. math::

            D(i, i) = 0.0 \, \forall \, i \in D

        *Dreiecksungleichung:*

        .. math::

            D(i, j) \leq D(i, x) + (x, j)

    Session

        Eine *Session* ist eine Nutzung von *libmunin* über einem bestimmten
        Zeitraum. Zum Erstellen einer Session werden die Daten importiert,
        analysiert und ein :term:`Graph` wird daraus aufgebaut.
    
        Zudem kann eine *Session* persistent für späteren Gebrauch gespeichert
        werden. 

        Für Nutzer der Bibliothek ist die :term:`Session` auch Eintrittspunkt
        für jegliche von *libmunin* bereitgestellte Funktionalität.

    Maske

        Die :term:`Session` benötigt eine Beschreibung der Daten die importiert
        werden. So muss ich darauf geeinigt werden was beispielsweise unter dem
        Schlüssel ``genre`` abgespeichert wird.
    
        In der *Maske* werden daher die einzelnen Attribute festgelegt, die ein
        einzelner Song haben kann und wie diese anzusprechen sind. Zudem wird
        pro Attribut ein :term:`Provider` und eine :term:`Distanzfunktion`
        festgelegt die bei der Verarbeitung dieses Wertes genutzt wird. Zudem
        wird die Gewichtung des Attributes festgelegt - manche Attribute sind
        für die Ähnlichkeit zweier Songs entscheidender als andere.

    Attribut

        Ein Attribut ist ein *Schlüssel* in der :term:`Maske`. Er repräsentiert
        eine Vereinbarung mit dem Nutzer unter welchem Namen das Attribut in
        Zukunft angesprochen wird. Zu jedem gesetzten Attribut gehört ein Wert,
        andernfalls ein spezieller leerer Wert. Ein Song besteht aus einer 
        Menge dieser Paare.

    Provider

        Ein *Provider* normalisiert einen Wert anhand verschiedener
        Charakteristiken. Sie dienen als vorgelagerte Verarbeitung von den Daten
        die in das System geladen werden. Jeder *Provider* ist dabei einem 
        :term:`Attribut` zugeordnet.

        Ihr Ziel ist für die :term:`Distanzfunktion` einfache und effizient 
        vergleichbare Werte zu liefern - da die :term:`Distanzfunktion` sehr
        viel öfters aufgerufen wird als der *Provider*.

    Assoziationsregel
        
        Eine Assoziationsregel verbindet zwei Mengen *A* und *B* von Songs
        miteinander. Wird eine der beiden Mengen miteinander gehört, ist es
        wahrscheinlich dass auch die andere Menge daraufhin angehört wird.

        Sie werden aus dem Verhalten des Nutzers abgeleitet.

        Die Güte der Regel wird durch ein *Rating* beschrieben:

        .. math::

            Rating(A, B) = (1.0 - Kulczynski(A, B)) \cdot ImbalanceRatio(A, B)

        wobei:

        .. math::

            Kulczynski(A, B) =  \frac{p(A \vert B) + p(B \vert A)}{2}

        .. math::

            ImbalanceRatio(A, B) = \frac{\vert support(A) - support(B) \vert}{support(A) + support(B) - support(A \cup B)}


        .. admonition:: Vergleiche dazu:

            :cite:`datamining-concepts-and-techniques`
            Datamining Concepts and Techniques.


    Recommendation

        Eine Recommendation (dt. Empfehlung) ist ein :term:`Song` der vom System
        auf Geheiß des Benutzers hin vorgeschlagen wird. 

        Die Empfehlunge sollte eine geringe Distanz zum :term:`Seedsong` haben.

    Seedsong

        Ein Song der als Basis für Empfehlungen ausgewählt wurde. 

    Graph 

        Im Kontext von *libmunin* ist der Graph eine Abbildung aller Songs (als
        Knoten) und deren Distanz (als Kanten) untereinander. Im idealen Graphen
        kennt jeder :term:`Song` *N* zu ihm selbst ähnlichsten Songs als
        Nachbarn.

        Da die Erstellung eines idealen Graphen sehr aufwendig ist, wird auf
        eine schneller zu berechnende Approximation zurückgegriffen.

.. only:: latex

   .. raw:: latex

       \newpage


.. _coldstart-example:

``coldstart.py``
================

Führt die in :num:`fig-startup` gezeigten Schritte *Kaltstart* bis *Rebuild*
aus. Als Eingabe wird die Datenbank des MPD-Servers verwendet, fehlende
Songtexte werden ergänzt und die Audiodaten für die ``moodbar`` und für die
Beats-per-Minute-Analyse wird lokalisiert. 

Im Anschluss wird die Session aufgebaut und unter
``$HOME/.cache/libmunin/EasySession.gz`` gespeichert.

.. code-block:: python

    #!/usr/bin/env python
    # encoding: utf-8
    # Stdlib:
    import logging

    # Internal:
    import moosecat.boot
    from moosecat.boot import g

    # External:
    from munin.easy import EasySession
    from munin.provider import PlyrLyricsProvider

    # Fetch missing lyrics, or load them from disk.
    # Also cache missed items for speed reasons.
    LYRICS_PROVIDER = PlyrLyricsProvider(cache_failures=True)

    def make_entry(song):
        # Hardcoded, Im sorry:
        full_uri = '/mnt/testdata/' + song.uri
        return song.uri, {
            'artist': song.artist,
            'album': song.album,
            'title': song.title,
            'genre': song.genre,
            'bpm': full_uri,
            'moodbar': full_uri,
            'rating': None,
            'date': song.date,
            'lyrics': LYRICS_PROVIDER.do_process((
                song.album_artist or song.artist, song.title
            ))
        }

    if __name__ == '__main__':
        # Bring up moosecat
        moosecat.boot.boot_base(verbosity=logging.DEBUG)
        g.client.connect(port=6601)
        moosecat.boot.boot_metadata()
        moosecat.boot.boot_store()

        # Fetch the whole database into entries:
        entries = []
        with g.client.store.query('*', queue_only=False) as playlist:
            for song in playlist:
                entries.append(make_entry(song))

        # Instance a new EasySession and fill in the values.
        session = EasySession()
        with session.transaction():
            for uri, entry in entries:
                try:
                    print('Processing:', entry['bpm'])
                    session.mapping[session.add(entry)] = uri
                except:
                    import traceback
                    traceback.print_exc()

        # Save the Session to disk (~/.cache/libmunin/EasySession.gz)
        session.save()

        # Plot if desired.
        if '--plot' in sys.argv:
            session.database.plot()

        # Close the connection to MPD, save cached database
        moosecat.boot.shutdown_application()

.. only:: latex

   .. raw:: latex

       \newpage


.. _complex-example:

Ausführliches Beispiel
======================

Der Vollständigkeit halber soll hier noch ein ausführliches Beispiel 
gezeigt werden, das auch im Vergleich zum einfachen Beispiel folgende Features
zeigt:

    - Das Erstellen einer eigenen Session
    - Das Speichern und Laden derselben
    - Das Füttern der History
    - Ableiten von Assoziationsregeln
    - Mehrere Möglichkeiten zur Empfehlung

.. code-block:: python

    #!/usr/bin/env python
    # encoding: utf-8

    import sys

    from munin.helper import pairup
    from munin.session import Session
    from munin.distance import GenreTreeDistance, WordlistDistance
    from munin.provider import \
            ArtistNormalizeProvider, \
            GenreTreeProvider, \
            WordlistProvider,  \
            StemProvider


    MY_DATABASE = [(
            'Devildriver',                # Artist
            'Before the Hangmans Noose',  # Title
            'metal'                       # Genre
        ), (
            'Das Niveau',
            'Beim Pissen gemeuchelt',
            'folk'
        ), (
            'We Butter the Bread with Butter',
            'Extrem',
            'metal'
        ), (
            'Lady Gaga',
            'Pokerface',
            'pop'
    )]


    def create_session(name):
        print('-- No saved session found, loading new.')
        session = Session(
            name='demo',
            mask={
                # Each entry goes like this:
                'Genre': pairup(
                    # Pratice: Go lookup what this Providers does.
                    GenreTreeProvider(),
                    # Practice: Same for the DistanceFunction.
                    GenreTreeDistance(),
                    # This has the highest rating of the three attributes:
                    8
                ),
                'Title': pairup(
                    # We can also compose Provider, so that the left one
                    # gets the input value, and the right one the value
                    # the left one processed.
                    # In this case we first split the title in words,
                    # then we stem each word.
                    WordlistProvider() | StemProvider(),
                    WordlistDistance(),
                    1
                ),
                'Artist': pairup(
                    # If no Provider (None) is given the value is forwarded as-is.
                    # Here we just use the default provider, but enable
                    # compression. Values are saved once and are givean an ID.
                    # Duplicate items get the same ID always.
                    # You can trade off memory vs. speed with this.
                    ArtistNormalizeProvider(compress=True),
                    # If not DistanceFunctions is given, all values are
                    # compare with __eq__ - which might give bad results.
                    None,
                    1
                )
            }
        )

        # As in our first example we fill the session, but we dont insert the full
        # database, we leave out the last song:
        with session.transaction():
            for idx, (artist, title, genre) in enumerate(MY_DATABASE[:3]):
                # Notice how we use the uppercase keys like above:
                session.mapping[session.add({
                    'Genre': genre,
                    'Title': title,
                    'Artist': artist,
                })] = idx

        return session


    def print_recommendations(session, n=5):
        # A generator that yields at max 20 songs.
        recom_generator = session.recommend_from_heuristic(number=n)
        seed_song = next(recom_generator)
        print('Recommendations to #{}:'.format(seed_song.uid))
        for munin_song in recom_generator:
            print('  normalized values:')

            # Let's take
            for attribute, normalized_value in munin_song.items():
                print('    {:<7s}: {:<20s}'.format(attribute, normalized_value))

            original_song = MY_DATABASE[session.mapping[munin_song.uid]]
            print('  original values:')
            print('    Artist :', original_song[0])
            print('    Album  :', original_song[1])
            print('    Genre  :', original_song[2])
            print()


    if __name__ == '__main__':
        print('The database:')
        for idx, song in enumerate(MY_DATABASE):
            print('  #{} {}'.format(idx, song))
        print()

        # Perhaps we already had an prior session?
        session = Session.from_name('demo') or create_session('demo')
        rules = list(session.rule_index)
        if rules:
            print('Association Rules:')
            for left, right, support, rating in rules:
                print('  {:>10s} <-> {:<10s} [supp={:>5d}, rating={:.5f}]'.format(
                    str([song.uid for song in left]),
                    str([song.uid for song in right]),
                    support, rating
                ))
            print()

        print_recommendations(session)

        # Let's add some history:
        for munin_uid in [0, 2, 0, 0, 2]:
            session.feed_history(munin_uid)

        print('Playcounts:')
        for song, count in session.playcounts().items():
            print('  #{} was played {}x times'.format(song.uid, count))

        # Let's insert a new song that will be in the graph on the next run:
        if len(session) != len(MY_DATABASE):
            with session.fix_graph():
                session.mapping[session.insert({
                    'Genre': MY_DATABASE[-1][2],
                    'Title': MY_DATABASE[-1][1],
                    'Artist': MY_DATABASE[-1][0]
                })] = 3

        if '--plot' in sys.argv:
            session.database.plot()

        # Save it under ~/.cache/libmunin/demo
        session.save()

Ausgabe nach dem ersten Lauf:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    The database:
      #0 ('Devildriver', 'Before the Hangmans Noose', 'metal')
      #1 ('Das Niveau', 'Beim Pissen gemeuchelt', 'folk')
      #2 ('We Butter the Bread with Butter', 'Extrem', 'metal')
      #3 ('Lady Gaga', 'Pokerface', 'pop')

    -- No saved session found, loading new.
    matching ['metal']
    matching ['folk']
    matching ['metal']
    Recommendations to #0:
      normalized values:
        Artist : (3,)                
        Genre  : ((583,),)           
        Title  : ['Extrem']          
      original values:
        Artist : We Butter the Bread with Butter
        Album  : Extrem
        Genre  : metal

    Playcounts:
      #0 was played 3x times
      #2 was played 2x times
    matching ['pop']

Ausgabe nach dem 10ten Lauf:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    The database:
      #0 ('Devildriver', 'Before the Hangmans Noose', 'metal')
      #1 ('Das Niveau', 'Beim Pissen gemeuchelt', 'folk')
      #2 ('We Butter the Bread with Butter', 'Extrem', 'metal')
      #3 ('Lady Gaga', 'Pokerface', 'pop')

    Association Rules:
             [2] <-> [0]        [supp=    8, rating=0.83951]

    Recommendations to #2:
      normalized values:
        Artist : (1,)                
        Genre  : ((583,),)           
        Title  : ['the', 'Befor', 'Noos', 'Hangman']
      original values:
        Artist : Devildriver
        Album  : Before the Hangmans Noose
        Genre  : metal

    Playcounts:
      #0 was played 30x times
      #2 was played 20x times

.. only:: latex

   .. raw:: latex

       \newpage
