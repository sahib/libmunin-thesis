from docutils import nodes


class dropcaps(nodes.TextElement):
    pass


def visit_dropcaps_node_latex(self, node):
    text = node.astext()
    self.body.append(
        '\\lettrine[lines=1]{{{w}}}{{{i}}}'.format(
            w=text[0],
            i=text[1:].upper()
        )
    )
    node.clear()


def visit_dropcaps_node_generic(self, node):
    pass


def depart_dropcaps_node(self, node):
    pass


def dropcaps_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    return[dropcaps(text=text)], []


def setup(app):
    app.add_node(
        dropcaps,
        html=(
            visit_dropcaps_node_generic,
            depart_dropcaps_node
        ),
        latex=(
            visit_dropcaps_node_latex,
            depart_dropcaps_node
        ),
        text=(
            visit_dropcaps_node_generic,
            depart_dropcaps_node
        )
    )

    app.add_role('dropcaps', dropcaps_role)
