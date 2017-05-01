#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CAVEAT UTILITOR
#
# This file was automatically generated by Tatsu.
#
#    https://pypi.python.org/pypi/tatsu/
#
# Any changes you make to it will be overwritten the next time
# the file is generated.


from __future__ import print_function, division, absolute_import, unicode_literals

from tatsu.buffering import Buffer
from tatsu.parsing import graken, Parser
from tatsu.util import re, RE_FLAGS, generic_main  # noqa


KEYWORDS = {}


class CalcBuffer(Buffer):
    def __init__(
        self,
        text,
        whitespace=None,
        nameguard=None,
        comments_re=None,
        eol_comments_re=None,
        ignorecase=None,
        namechars='',
        **kwargs
    ):
        super(CalcBuffer, self).__init__(
            text,
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            namechars=namechars,
            **kwargs
        )


class CalcParser(Parser):
    def __init__(
        self,
        whitespace=None,
        nameguard=None,
        comments_re=None,
        eol_comments_re=None,
        ignorecase=None,
        left_recursion=False,
        parseinfo=True,
        keywords=None,
        namechars='',
        buffer_class=CalcBuffer,
        **kwargs
    ):
        if keywords is None:
            keywords = KEYWORDS
        super(CalcParser, self).__init__(
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            left_recursion=left_recursion,
            parseinfo=parseinfo,
            keywords=keywords,
            namechars=namechars,
            buffer_class=buffer_class,
            **kwargs
        )

    @graken()
    def _start_(self):
        self._expression_()
        self._check_eof()

    @graken()
    def _expression_(self):
        with self._choice():
            with self._option():
                self._term_()
                self._token('+')
                self._cut()
                self._expression_()
            with self._option():
                self._term_()
                self._token('-')
                self._cut()
                self._expression_()
            with self._option():
                self._term_()
            self._error('no available options')

    @graken()
    def _term_(self):
        with self._choice():
            with self._option():
                self._factor_()
                self._token('*')
                self._cut()
                self._term_()
            with self._option():
                self._factor_()
                self._token('/')
                self._cut()
                self._term_()
            with self._option():
                self._factor_()
            self._error('no available options')

    @graken()
    def _factor_(self):
        with self._choice():
            with self._option():
                self._token('(')
                self._cut()
                self._expression_()
                self._token(')')
            with self._option():
                self._number_()
            self._error('no available options')

    @graken()
    def _number_(self):
        self._pattern(r'\d+')


class CalcSemantics(object):
    def start(self, ast):
        return ast

    def expression(self, ast):
        return ast

    def term(self, ast):
        return ast

    def factor(self, ast):
        return ast

    def number(self, ast):
        return ast


def main(filename, startrule, **kwargs):
    with open(filename) as f:
        text = f.read()
    parser = CalcParser()
    return parser.parse(text, startrule, filename=filename, **kwargs)


if __name__ == '__main__':
    import json
    from tatsu.util import asjson

    ast = generic_main(main, CalcParser, name='Calc')
    print('AST:')
    print(ast)
    print()
    print('JSON:')
    print(json.dumps(asjson(ast), indent=2))
    print()
