#!/usr/bin/env python
# encoding: utf-8

import re
import sys
import datetime

import string
import random
random.seed(42)

from urllib import urlopen

import HTMLParser

TEMPLATE = '''
@Misc{{{key},
    {title}
    note = {{[Stand: {date}]}},
    url = {{{url}}},
    howpublished = "\\url{{{url}}}",
    key = {{{key}}}
}}
'''


def id_generator(size, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def fix_title(title):
    title = HTMLParser.HTMLParser().unescape(title)
    title = title.split('-')[0]
    title = title.split(':')[0]
    title.strip()
    title = re.sub('<[^<]+?>', '', title)
    return title.split()[0]


def print_bibtex_entry(url):
    text = urlopen(url).read()

    # I know. Dont do this kids.
    match = re.search('<\s*title\s*>\s*(.*)\s*<\s*/\s*title\s*>', text)
    if match is None:
        match = re.search('<\s*h1\s*>\s*(.*)\s*<\s*/\s*h1\s*>', text)

    if match is not None:
        title = fix_title(match.group(1))
    else:
        title = None

    date = datetime.datetime.now()
    date_string = '{d}.{m}.{y}'.format(d=date.day, m=date.month, y=date.year)
    key = id_generator(size=3)

    try:
        entry = 'title = {{{t}}},'.format(t=title) if title is not None else ''
    except:
        entry = ''

    print(TEMPLATE.format(
        key=key,
        title=entry,
        date=date_string,
        url=url
    ))


if __name__ == '__main__':
    import os

    if os.access(sys.argv[1], os.R_OK):
        with open(sys.argv[1], 'r') as handle:
            for line in handle:
                print_bibtex_entry(line.strip())
    else:
        print_bibtex_entry(sys.argv[1])
