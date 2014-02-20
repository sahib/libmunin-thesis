*********
Hauptteil
*********

Algorithmen
===========

Genre Splitting
---------------

Problem: Der Vergleich von Musikgenres ist aufgrund der 


- Aufbau der Datenbank: wikipedia, echonest



.. code-block:: python

    from docutils import nodes
 
 
    # Code Documentation
    class latex_sign(nodes.General, nodes.Element):
        """ DOCSTRING """
        pass
 
 
    def visit_todo_node_latex(self, node):
        self.body.append('\\LaTeX')
 
 
    def visit_todo_node_text(self, node):
        self.body.append('LaTeX')
 
 
    def visit_todo_node_html(self, node):
        self.body.append('''
            <style type="text/css">
                .tex sub, .latex sub, .latex sup {
                    text-transform: uppercase;
                }
 
                .tex sub, .latex sub {
                    vertical-align: -0.5ex;
                    margin-left: -0.1667em;
                    margin-right: -0.125em;
                }
 
                .tex, .latex, .tex sub, .latex sub {
                    font-size: 1em;
                }
 
                .latex sup {
                    font-size: 0.85em;
                    vertical-align: 0.15em;
                    margin-left: -0.36em;
                    margin-right: -0.15em;
                }
            </style>
            <span class="latex">L<sup>a</sup>T<sub>e</sub>X</span>
        ''')
 
 
    def depart_todo_node(self, node):
        pass
 
 
    def latex_sign_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
        return[latex_sign()], []
 
 
    def setup(app):
        app.add_node(
            latex_sign,
            html=(
                visit_todo_node_html,
                depart_todo_node
            ),
            latex=(
                visit_todo_node_latex,
                depart_todo_node
            ),
            text=(
                visit_todo_node_text,
                depart_todo_node
            )
        )
        app.add_role('latex_sign', latex_sign_role)


Keword Extraction
-----------------

KeywordExtraction - KeywordSelection - KeywordDistance

Rule Generation
---------------


Graph Generation
----------------

add, rebuild, fix_graph

distance_add
------------

"max_neighbors Dilemma"


Graphenoperationen
------------------

insert, remove, modify

Graphentraversierung
--------------------

Infinite Iteratos - konzept aus funktionalen Programmiersprachen wie Haskell

Sieving Algorithm
-----------------

Erklärung & Configuration.


Various Providers
-----------------

Erwähnenswerte Algorithmik hinter den anderen Providern.

levenshtein, bpm, moodbar, wordlist distance, normalize provider, stemming
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj

ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj

ijieojfijweifjjijj

ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj

ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj

ijieojfijweifjjijj

ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj

ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj

ijieojfijweifjjijj

ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj

ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj

ijieojfijweifjjijj

ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj

ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj

ijieojfijweifjjijj

ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
ijieojfijweifjjijj
