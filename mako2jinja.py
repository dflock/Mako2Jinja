# -*- coding: utf-8 -*-

"""Mako2Jinja

Usage:
    mako2jinja.py FILE
    mako2jinja.py (-h | --help)
    mako2jinja.py --version

Converts a given mako template into a jinja template, badly.

Arguments:
    FILE                      Input file.

Options:
    -h --help                 Show this screen.
    --version                 Show version.

"""
from docopt import docopt
import re


def mako2jinja(input_file):

    output = ''

    macro_start = re.compile('(.*)<%.*def name="(.*)">(.*)', re.IGNORECASE)
    macro_end = re.compile('(.*)</%def>(.*)', re.IGNORECASE)
    val = re.compile('(.*)\$\{(.*)\}(.*)', re.IGNORECASE)

    if_start = re.compile('(.*)%.*if (.*):(.*)', re.IGNORECASE)
    if_end = re.compile('(.*)%endif(.*)', re.IGNORECASE)

    for_start = re.compile('(.*)%.*for (.*):(.*)', re.IGNORECASE)
    for_end = re.compile('(.*)%endfor(.*)', re.IGNORECASE)

    for line in input_file:
        m_start = macro_start.search(line)
        m_end = macro_end.search(line)
        m_val = val.search(line)
        m_if_start = if_start.search(line)
        m_if_end = if_end.search(line)
        m_for_start = for_start.search(line)
        m_for_end = for_end.search(line)

        if m_start:
            output += m_start.expand(r'\1{% macro \2}\3') + '\n'
        elif m_end:
            output += m_end.expand(r'\1{% endmacro }\1') + '\n'

        elif m_val:
            output += val.sub(r'\1{{\2}}\3', line)

        elif m_if_start:
            output += m_if_start.expand(r'\1{% if \2}\3') + '\n'
        elif m_if_end:
            output += m_if_end.expand(r'\1{% endif %}\2') + '\n'

        elif m_for_start:
            output += m_for_start.expand(r'\1{% for \2}\3') + '\n'
        elif m_for_end:
            output += m_for_end.expand(r'\1{% endfor %}\2') + '\n'

        else:
            # Doesn't match anything we're going to process, pass though
            output += line

    return output


if __name__ == '__main__':
    args = docopt(__doc__, version='Mako2Jinja 0.1')

    if args['FILE']:
        try:
            input = open(args['FILE'])
            print mako2jinja(input)

        except IOError, e:
            print e
