import libmsp

{%- macro make_enum(decl) -%}
class {{ decl.name }}(libmsp.Enum):
{% for field in decl.fields %}
    {{ field.name }} = {{ field.value }}
{% endfor %}
{% endmacro %}

{% macro make_struct(decl) %}
class {{ decl.name|norm|ucfirst }}(libmsp.Message):
{% if decl.comments and decl.comments.text %}
    """{{ decl.comments.text|replace('\n', '\n    ') }}"""
{% endif %}
    PGN = PGN.{{ decl.comments.fields.pgn.value }}
    PARAMS = (
{% for field in decl.fields %}
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
)
{% endfor %}
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

