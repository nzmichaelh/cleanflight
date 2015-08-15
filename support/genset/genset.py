"""Example of a parser that handles a subset of C and can extract structs and
typedefs for later generation.

See test.h for example input.

"""

import fileinput
import pprint
import collections
import re
import argparse
import jinja2
import sys

from pyparsing import *

BaseType = collections.namedtuple('BaseType', 'name size bits signed')


def make_base_types():
    types = {
        'char': BaseType('char', 1, 8, True),
    }
    for size in 1, 2, 4:
        for signed in True, False:
            bits = size * 8
            name = '{}int{}_t'.format('' if signed else 'u', bits)
            types[name] = BaseType(name, size, bits, signed)
    return types

BASE_TYPES = make_base_types()


def find_type(name):
    if name in BASE_TYPES:
        return BASE_TYPES[name]
    else:
        return BaseType(name, -1, -1, False)


def first(v):
    if len(v) == 0:
        return None
    elif len(v) == 1:
        return v[0]
    else:
        return ' '.join(v)


def parse_number(tokens):
    return int(tokens[0])

Comments = collections.namedtuple('Comments', 'text fields')


def parse_comments(tokens):
    text = []
    fields = {}
    for line in tokens:
        line = line.strip()
        if re.match('^[a-z_]+:', line):
            for field in sub_comments.parseString(line):
                fields[field.name] = field
        else:
            text.append(line)
    return Comments('\n'.join(text), fields)

Enum = collections.namedtuple('Enum', 'name fields comments')


def parse_enum(tokens):
    return Enum(tokens.name, list(tokens.fields), first(tokens.comments))

EnumField = collections.namedtuple('EnumField', 'name value comments')


def parse_enum_field(tokens):
    return EnumField(tokens.name, first(tokens.value), first(tokens.comments))


def parse_compound_value(tokens):
    l = len(tokens)
    left = int(tokens[0])
    for i in range(1, l, 2):
        operator = tokens[i]
        right = int(tokens[i+1])

        if operator == '<<':
            left = left << right
        else:
            assert False
    return left

Typedef = collections.namedtuple('Typedef', 'name alias')


def parse_typedef(tokens):
    return Typedef(tokens.name, tokens.alias)

Struct = collections.namedtuple('Struct', 'type name fields comments repeating count')


def parse_struct(tokens):
    return Struct('Struct', tokens.name, list(tokens.fields), first(tokens.comments), tokens.get('inner', []), tokens.get('count', None))

StructField = collections.namedtuple('StructField', 'type name count comments')


def parse_struct_field(tokens):
    return StructField(find_type(tokens.type), tokens.name, tokens.count, first(tokens.comments))

CommentField = collections.namedtuple('CommentField', 'name value')


def parse_comment_field(tokens):
    return CommentField(tokens.name, tokens.value)


def parse_count(tokens):
    return first(tokens)

struct = Keyword('struct')
typedef = Keyword('typedef')
enum = Keyword('enum')
lbrace = Suppress('{')
rbrace = Suppress('}')
lbracket = Suppress('[')
rbracket = Suppress(']')
semi = Suppress(';')
equals = Suppress('=')
comma = Suppress(',')
colon = Suppress(':')

number = Word(nums).setParseAction(parse_number)

identifier = Word(alphas, alphanums + '_').setName('identifier')

comment = Literal('//').suppress() + restOfLine
comments = OneOrMore(comment).setParseAction(parse_comments)

#type_alias = Optional(comments) + typedef + identifier + identifier
array_count = lbracket + Optional(number) + rbracket
array_count.setParseAction(parse_count)

struct_field = (
    Optional(comments).setResultsName('comments')
    + identifier.setResultsName('type')
    + identifier.setResultsName('name')
    + Optional(lbracket + Optional(number) +
               rbracket).setParseAction(parse_count).setResultsName('count')
    + semi
)
struct_field.setParseAction(parse_struct_field)

inner_struct = (
    Optional(comments).setResultsName('comments')
    + struct
    + lbrace
    + OneOrMore(struct_field).setResultsName('fields')
    + rbrace
    + identifier.setResultsName('name')
    + array_count.setResultsName('count')
    + semi
)
inner_struct.setParseAction(parse_struct)

struct_decl = (
    Optional(comments).setResultsName('comments')
    + Optional(typedef)
    + struct
    + identifier.setResultsName('name')
    + lbrace
    + ZeroOrMore(struct_field).setResultsName('fields')
    + Optional(inner_struct).setResultsName('inner')
    + Optional(comments)
    + rbrace
    + ZeroOrMore(identifier)
)
struct_decl.setParseAction(parse_struct)

operator = Literal('<<')
enum_value = Word(nums) + Optional(operator + Word(nums))
enum_value.setParseAction(parse_compound_value)

enum_field = (
    Optional(comments).setResultsName('comments')
    + identifier.setResultsName('name')
    + Optional(equals + enum_value).setResultsName('value')
)
enum_field.setParseAction(parse_enum_field)

enum_decl = (
    Optional(comments).setResultsName('comments')
    + enum
    + identifier.setResultsName('name')
    + lbrace
    + delimitedList(enum_field).setResultsName('fields')
    + Optional(comma)
    + Optional(comments)
    + rbrace
)
enum_decl.setParseAction(parse_enum)

typedef_decl = (
    typedef
    + identifier.setResultsName('name')
    + identifier.setResultsName('alias')
)
typedef_decl.setParseAction(parse_typedef)

schema = ZeroOrMore((struct_decl | typedef_decl | enum_decl) + semi)

comment_field = (
    identifier.setResultsName('name')
    + colon
    + (number | identifier).setResultsName('value')
)
comment_field.setParseAction(parse_comment_field)

sub_comments = delimitedList(comment_field, delim=';')


def constname(v):
    return re.sub(r'([a-z])([A-Z])', r'\1_\2', v).upper()


def ucfirst(v):
    return v[0].upper() + v[1:]


def makeargs(v):
    for field in v:
        if field.count:
            yield 'const {} *{}'.format(field.type.name, field.name)
        else:
            yield '{} {}'.format(field.type.name, field.name)


def totalsize(v):
    type = v.type
    if v.count:
        return '{}*{}'.format(v.count, type.size)
    else:
        return type.size


def norm(v):
    """Turn a typedef or struct name into the normalised name."""
    if v.endswith('_t') or v.endswith('_s') or v.endswith('_e'):
        v = v[:-2]
    if v.startswith('msp'):
        v = v[3:]
    return v

types = {
    'Enum': Enum,
    'Struct': Struct,
}


def main():
    strict = False

    parser = argparse.ArgumentParser()
    parser.add_argument('-o')
    parser.add_argument('-t', type=argparse.FileType('r'))
    parser.add_argument('src', type=argparse.FileType('r'))
    args = parser.parse_args()

    env = jinja2.Environment(trim_blocks=True)
    env.filters.update({
        'constname': constname,
        'ucfirst': ucfirst,
        'makeargs': makeargs,
        'totalsize': totalsize,
        'norm': norm,
    })
    t = env.from_string(args.t.read())
    decls = []

    contents = args.src.read()
    if strict:
        docs = [schema.parseString(contents, parseAll=True)]
    else:
        docs = schema.scanString(contents)

    for doc in docs:
        decls.extend(doc[0])

    rendered = t.render(decls=decls,
                        types=types,
                        isinstance=isinstance,
                        )

    if args.o:
        with open(args.o, 'w') as f:
            f.write(rendered)
    else:
        sys.stdout.write(rendered)

if __name__ == '__main__':
    main()
