#!/usr/bin/env python
# encoding: utf-8


from docutils import nodes


class latex_sign(nodes.General, nodes.Element):
    pass


def visit_latex_sign_latex(self, node):
    self.body.append('\\LaTeX')


def visit_latex_sign_text(self, node):
    self.add_text('LaTeX')


def visit_latex_sign_html(self, node):
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


def depart_latex_sign(self, node):
    pass


def latex_sign_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    return[latex_sign()], []


def setup(app):
    app.add_node(
        latex_sign,
        html=(
            visit_latex_sign_html,
            depart_latex_sign
        ),
        latex=(
            visit_latex_sign_latex,
            depart_latex_sign
        ),
        text=(
            visit_latex_sign_text,
            depart_latex_sign
        )
    )

    latex_sign_role.content = False
    app.add_role('latex_sign', latex_sign_role)
