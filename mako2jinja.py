# -*- coding: utf-8 -*-

"""Mako2Jinja

Usage:
    mako2jinja.py FILE
    mako2jinja.py (-h | --help)
    mako2jinja.py --version

Converts a given mako template into a jinja template, badly. It's just intended to help with the mechanical editing - you'll probably have to fixup anything complicated yourself.

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

    # TODO: OMG, this code is so horrible. Just look at it:

    macro_start = re.compile(r'(.*)<%.*def name="(.*?)".*>(.*)', re.IGNORECASE)
    macro_end = re.compile(r'(.*)</%def>(.*)', re.IGNORECASE)

    if_start = re.compile(r'(.*)% *if (.*):(.*)', re.IGNORECASE)
    if_else = re.compile(r'(.*)% *else.*:(.*)', re.IGNORECASE)
    if_end = re.compile(r'(.*)% *endif(.*)', re.IGNORECASE)

    for_start = re.compile(r'(.*)% *for (.*):(.*)', re.IGNORECASE)
    for_end = re.compile(r'(.*)% *endfor(.*)', re.IGNORECASE)

    namespace = re.compile(r'(.*)<% *namespace name="(.*?)".* file="(.*?)".*/>(.*)', re.IGNORECASE)
    inherit = re.compile(r'(.*)<% *inherit file="(.*?)".*/>(.*)', re.IGNORECASE)

    block_single_line = re.compile(r'(.*)<% *block.*name="(.*?)".*>(.*)</% *block>(.*)', re.IGNORECASE)
    block_start = re.compile(r'(.*)<% *block.*name="(.*?)".*>(.*)', re.IGNORECASE)
    block_end = re.compile(r'(.*)</%block>(.*)', re.IGNORECASE)

    val = re.compile(r'\$\{(.*?)\}', re.IGNORECASE)
    func_len = re.compile(r'len\((.*?)\)', re.IGNORECASE)
    filter_h = re.compile(r'\|h', re.IGNORECASE)

    comment_single_line = re.compile(r'^\s*#+ *(.*?)$', re.IGNORECASE)

    for line in input_file:

        # Process line for repeated inline replacements
        m_val = val.search(line)
        m_func_len = func_len.search(line)
        m_filter_h = filter_h.search(line)

        if m_val:
            line = val.sub(r'{{ \1 }}', line)

        if m_filter_h:
            line = filter_h.sub(r'|e', line)

        if m_func_len:
            line = func_len.sub(r'\1|length', line)

        # Process line for single 'whole line' replacements
        m_macro_start = macro_start.search(line)
        m_macro_end = macro_end.search(line)
        m_if_start = if_start.search(line)
        m_if_else = if_else.search(line)
        m_if_end = if_end.search(line)
        m_for_start = for_start.search(line)
        m_for_end = for_end.search(line)
        m_namspace = namespace.search(line)
        m_inherit = inherit.search(line)
        m_block_single_line = block_single_line.search(line)
        m_block_start = block_start.search(line)
        m_block_end = block_end.search(line)

        m_comment_single_line = comment_single_line.search(line)

        if m_comment_single_line:
            output += m_comment_single_line.expand(r'{# \1 #}') + '\n'

        elif m_macro_start:
            output += m_macro_start.expand(r'\1{% macro \2 %}\3') + '\n'
        elif m_macro_end:
            output += m_macro_end.expand(r'\1{% endmacro %}\1') + '\n'

        elif m_if_start:
            output += m_if_start.expand(r'\1{% if \2 %}\3') + '\n'
        elif m_if_else:
            output += m_if_else.expand(r'\1{% else %}\2') + '\n'
        elif m_if_end:
            output += m_if_end.expand(r'\1{% endif %}\2') + '\n'

        elif m_for_start:
            output += m_for_start.expand(r'\1{% for \2 %}\3') + '\n'
        elif m_for_end:
            output += m_for_end.expand(r'\1{% endfor %}\2') + '\n'

        elif m_namspace:
            output += m_namspace.expand(r"\1{% import '\3' as \2 with context %}\4") + '\n'
        elif m_inherit:
            output += m_inherit.expand(r"{% extends '\2' %}\3") + '\n'

        elif m_block_single_line:
            output += m_block_single_line.expand(r'\1{% block \2 %}\3{% endblock %}\4') + '\n'
        elif m_block_start:
            output += m_block_start.expand(r'\1{% block \2 %}\3') + '\n'
        elif m_block_end:
            output += m_block_end.expand(r'\1{% endblock %}\2') + '\n'

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
