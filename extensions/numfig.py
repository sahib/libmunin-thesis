#!/usr/bin/env python
# encoding: utf-8


from docutils import nodes
from sphinx.roles import XRefRole
import figtable
import subfig

from collections import OrderedDict
from collections.abc import MutableSet

# Helper

# Modified from original source, available here:
# http://code.activestate.com/recipes/577624-orderedset/


class OrderedSet(MutableSet):
    '''Set that remembers original insertion order.'''

    KEY, PREV, NEXT = range(3)

    def __init__(self, iterable=None):
        self.end = end = []
        end += [None, end, end]         # sentinel node for doubly linked list
        self.map = {}                   # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def __contains__(self, key):
        return key in self.map

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)

    def __iter__(self):
        end = self.end
        curr = end[self.NEXT]
        while curr is not end:
            yield curr[self.KEY]
            curr = curr[self.NEXT]

    def __len__(self):
        return len(self.map)

    def __reversed__(self):
        end = self.end
        curr = end[self.PREV]
        while curr is not end:
            yield curr[self.KEY]
            curr = curr[self.PREV]

    def add(self, key):
        if key not in self.map:
            end = self.end
            curr = end[self.PREV]
            curr[self.NEXT] = end[self.PREV] = self.map[key] = [key, curr, end]

    def discard(self, key):
        if key in self.map:
            key, prev, next = self.map.pop(key)
            prev[self.NEXT] = next
            next[self.PREV] = prev

    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')
        key = next(reversed(self)) if last else next(iter(self))
        self.discard(key)
        return key

    def __del__(self):
        self.clear()

    def __repr__(self):
        class_name = self.__class__.__name__
        if not self:
            return '{0!s}()'.format(class_name)
        return '{0!s}({1!r})'.format(class_name, list(self))


# Element classes


class page_ref(nodes.reference):
    pass


class num_ref(nodes.reference):
    pass


# Visit/depart functions

def skip_page_ref(self, node):
    raise nodes.SkipNode


def latex_visit_page_ref(self, node):
    self.body.append("\\pageref{%s:%s}" % (node['refdoc'], node['reftarget']))
    raise nodes.SkipNode


def latex_visit_num_ref(self, node):
    fields = node['reftarget'].split('#')

    if len(fields) > 1:
        label, target = fields
    else:
        label = None
        target = fields[0]

    if target not in self.builder.env.docnames_by_figname:
        raise nodes.SkipNode
    targetdoc = self.builder.env.docnames_by_figname[target]

    ref_link = '%s:%s' % (targetdoc, target)

    if label is None:
        latex = '\\ref{%s}' % ref_link
    else:
        latex = "\\hyperref[%s]{%s \\ref*{%s}}" % (ref_link, label, ref_link)

    self.body.append(latex)
    raise nodes.SkipNode


def doctree_read(app, doctree):
    # first generate figure numbers for each figure
    env = app.builder.env

    docname_figs = getattr(env, 'docname_figs', {})
    docnames_by_figname = getattr(env, 'docnames_by_figname', {})

    for figure_info in doctree.traverse(
        lambda n:
            isinstance(n, nodes.figure) or
            isinstance(n, subfig.subfigend) or
            isinstance(n, figtable.figtable)
    ):

        for id in figure_info['ids']:
            docnames_by_figname[id] = env.docname

            fig_docname = docnames_by_figname[id]
            if fig_docname not in docname_figs:
                docname_figs[fig_docname] = OrderedDict()

            if isinstance(figure_info.parent, subfig.subfig):
                mainid = figure_info.parent['mainfigid']
            else:
                mainid = id

            if mainid not in docname_figs[fig_docname]:
                docname_figs[fig_docname][mainid] = OrderedSet()

            if isinstance(figure_info.parent, subfig.subfig):
                docname_figs[fig_docname][mainid].add(id)

    env.docnames_by_figname = docnames_by_figname
    env.docname_figs = docname_figs


def doctree_resolved(app, doctree, docname):
    # replace numfig nodes with links
    if app.builder.name in ('html', 'singlehtml', 'epub'):
        env = app.builder.env

        docnames_by_figname = env.docnames_by_figname
        figids = getattr(env, 'figids', {})

        secnums = []
        fignames_by_secnum = {}
        for figdocname, figurelist in env.docname_figs.items():
            if figdocname not in env.toc_secnumbers:
                continue
            secnum = env.toc_secnumbers[figdocname]['']
            secnums.append(secnum)
            fignames_by_secnum[secnum] = figurelist

        last_secnum = 0
        secnums = sorted(secnums)
        figid = 1
        for secnum in secnums:
            if secnum[0] != last_secnum:
                figid = 1
            for figname, subfigs in fignames_by_secnum[secnum].items():
                figids[figname] = str(secnum[0]) + '.' + str(figid)
                for i, subfigname in enumerate(subfigs):
                    subfigid = figids[figname] + chr(ord('a') + i)
                    figids[subfigname] = subfigid
                figid += 1
            last_secnum = secnum[0]

            env.figids = figids

        for figure_info in doctree.traverse(lambda n: isinstance(n, nodes.figure) or \
                                                      isinstance(n, subfig.subfigend) or \
                                                      isinstance(n, figtable.figtable)):
            try:
                id = figure_info['ids'][0]
            except IndexError:
                return

            try:
                fignum = figids[id]
            except KeyError:
                return

            for cap in figure_info.traverse(nodes.caption):
                cap.insert(1, nodes.Text(" %s" % cap[0]))
                if fignum[-1] in list(map(str, list(range(10)))):
                    boldcaption = "%s %s:" % (app.config.figure_caption_prefix, fignum)
                else:
                    boldcaption = "(%s)" % fignum[-1]
                cap[0] = nodes.strong('', boldcaption)

        for ref_info in doctree.traverse(num_ref):
            if '#' in ref_info['reftarget']:
                label, target = ref_info['reftarget'].split('#')
                labelfmt = label + " %s"
            else:
                labelfmt = '%s'
                target = ref_info['reftarget']

            if target not in docnames_by_figname:
                app.warn('Target figure not found: %s' % target)
                link = "#%s" % target
                linktext = target
            else:
                target_doc = docnames_by_figname[target]

                if app.builder.name == 'singlehtml':
                    link = "#%s" % target
                else:
                    link = "%s#%s" % (app.builder.get_relative_uri(docname, target_doc),
                                      target)

                linktext = labelfmt % figids.get(target, '[broken link :-(]')

            html = '<a href="%s">%s</a>' % (link, linktext)
            ref_info.replace_self(nodes.raw(html, html, format='html'))


def setup(app):
    # Config values:
    app.add_config_value('number_figures', True, True)
    app.add_config_value('figure_caption_prefix', "Figure", True)

    # Nodes:
    app.add_node(
        page_ref,
        text=(skip_page_ref, None),
        html=(skip_page_ref, None),
        singlehtml=(skip_page_ref, None),
        latex=(latex_visit_page_ref, None)
    )

    app.add_node(
        num_ref,
        latex=(latex_visit_num_ref, None),
        text=(skip_page_ref, None),
        singlehtml=(skip_page_ref, None),
        html=(skip_page_ref, None)
    )

    # Roles:
    app.add_role('num', XRefRole(nodeclass=num_ref))
    app.add_role('page', XRefRole(nodeclass=page_ref))

    # Signals:
    app.connect('doctree-read', doctree_read)
    app.connect('doctree-resolved', doctree_resolved)
