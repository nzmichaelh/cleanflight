import libmsp

{%- macro make_enum(decl) -%}
class {{ decl.name|norm|ucfirst }}(
{%- if decl.comments and decl.comments.fields.is_flags -%}
libmsp.Flags
{%- else -%}
libmsp.Enum
{%- endif -%}
):
{% set value = 0 %}
{% for field in decl.fields %}
{% set value = field.value if field.value != None else value %}
    {{ field.name }} = {{ value }}
{% set value = value + 1 %}
{% endfor %}
{% endmacro %}

{% macro make_struct(decl, prefix='') %}
class {{ prefix }}{{ decl.name|norm|ucfirst }}(libmsp.Message):
{% if decl.comments and decl.comments.text %}
    """{{ decl.comments.text|replace('\n', '\n    ') }}"""
{% endif %}
{% if decl.comments and decl.comments.fields.pgn %}
    PGN = PGN.{{ decl.comments.fields.pgn.value }}
{% endif %}
{% for inner in decl.repeating %}

    {{ make_struct(inner)|indent(4) }}
{% endfor %}

    PARAMS = (
{% for field in decl.fields %}
        '{{ field.name }}',
{% endfor %}
{% for field in decl.repeating %}
        '{{ field.name }}',
{% endfor %}
        )
{% for field in decl.fields %}
{% if field.comments and field.comments.text %}
    # {{ field.comments.text|replace('\n', '\n    #') }}
{% endif %}
    {{ field.name }} = libmsp.Field('{{ field.name }}', {{ field.type.size }}, {{ field.type.signed }}
{%- if field.count != '' -%}
, {{ field.count or -1 }}
{%- endif -%}
{% if field.comments and field.comments.fields.type %}
, type_={{ field.comments.fields.type.value|norm|ucfirst }}
{% endif %}
)
{% endfor %}
{% for field in decl.repeating %}
    {{ field.name }} = libmsp.InnerMessage('{{ field.name }}', {{ field.name|norm|ucfirst }}
{%- if field.count != '' -%}
, {{ field.count or -1 }}
{%- endif -%}
)
{% endfor %}

    def __init__(self
{%- for field in decl.fields -%}
, {{ field.name }}={% if field.count != '' %}[]{% else %}0{% endif %}
{%- endfor -%}
{%- for field in decl.repeating -%}
, {{ field.name }}=[]
{%- endfor -%}
):
{% for field in decl.fields %}
        self.{{ field.name }} = {{ field.name }}
{% endfor %}
        pass
{% endmacro %}

{% for decl in decls %}
{% if isinstance(decl, types.Struct) %}
{{ make_struct(decl) }}
{% elif isinstance(decl, types.Enum) %}
{{ make_enum(decl) }}
{% endif %}
{% endfor %}

def register():
    registry = libmsp.Registry()
{% for decl in decls if isinstance(decl, types.Struct) %}
    registry.register({{ decl.name|norm|ucfirst }})
{% endfor %}
    return registry

