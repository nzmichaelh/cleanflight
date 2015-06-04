"""Example of a parser that handles a subset of C and can extract
structs and typedefs for later generation.

See test.h for example input.
"""

import fileinput
import pprint
import collections
import re

from pyparsing import *

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
        if re.match('^[a-z]+:', line):
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

Typedef = collections.namedtuple('Typedef', 'name alias')

def parse_typedef(tokens):
    return Typedef(tokens.name, tokens.alias)

Struct = collections.namedtuple('Struct', 'name fields')

def parse_struct(tokens):
    return Struct(tokens.name, list(tokens.fields))

StructField = collections.namedtuple('StructField', 'type name count comments')

def parse_struct_field(tokens):
    return StructField(tokens.type, tokens.name, tokens.count, first(tokens.comments))

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

struct_field = (
    Optional(comments).setResultsName('comments')
    + identifier.setResultsName('type')
    + identifier.setResultsName('name')
    + Optional(lbracket + number + rbracket).setParseAction(parse_count).setResultsName('count')
    + semi
    )
struct_field.setParseAction(parse_struct_field)

struct_decl = (
    Optional(typedef)
    + struct
    + identifier.setResultsName('name')
    + lbrace
    + OneOrMore(struct_field).setResultsName('fields')
    + rbrace
    + ZeroOrMore(identifier)
    )
struct_decl.setParseAction(parse_struct)

enum_field = (
    Optional(comments).setResultsName('comments')
    + identifier.setResultsName('name')
    + Optional(equals + number).setResultsName('value')
    )
enum_field.setParseAction(parse_enum_field)

enum_decl = (
    Optional(comments).setResultsName('comments')
    + enum
    + identifier.setResultsName('name')
    + lbrace
    + delimitedList(enum_field).setResultsName('fields')
    + Optional(comma)
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

comment_field =(
    identifier.setResultsName('name')
    + colon
    + (number | identifier).setResultsName('value')
    )
comment_field.setParseAction(parse_comment_field)

sub_comments = delimitedList(comment_field, delim=';')

def main():
    contents = '\n'.join(fileinput.input())
    if False:
        for v in schema.searchString(contents):
            results, start, end = v
            results.pprint()
    else:
        schema.parseString(contents, parseAll=True).pprint()

if __name__ == '__main__':
    main()
