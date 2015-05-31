"""Example of a parser that handles a subset of C and can extract
structs and typedefs for later generation.

See test.h for example input.
"""

import fileinput
import pprint
from pyparsing import *

struct = Keyword('struct')
lbrace = Literal('{')
rbrace = Literal('}')
semi = Literal(';')
identifier = Word(alphas, alphanums + '_')
typedef = Keyword('typedef')

comment = Literal('//').suppress() + restOfLine
comments = Group(OneOrMore(comment))

type_alias = Optional(comments) + typedef + identifier + identifier

field_def = Optional(comments) + identifier + identifier + semi

struct_def = struct + Optional(identifier) + lbrace + OneOrMore(field_def) + rbrace

typedef_def = Optional(comments) + typedef + struct_def + identifier

bnf = ZeroOrMore((struct_def | typedef_def | type_alias) + semi)

def main():
    for v in bnf.scanString('\n'.join(fileinput.input())):
        results, start, end = v
        results.pprint()

if __name__ == '__main__':
    main()
