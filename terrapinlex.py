"""
    https://github.com/dabeaz/ply/blob/master/example/ansic/clex.py
"""

import string

import ply.lex as lex

reserved = (
    'IF', 'ELSE', 'ENDIF'
)

tokens = reserved + (
    # Code delimiters
    'LCODEDELIM', 'RCODEDELIM', 'LVARDELIM', 'RVARDELIM',

    # Literals
    'HTML', 'QUOTEDSTRING', 'STRING',

    # Operators
    'EQ', 'NE'
)

t_ignore = string.whitespace


def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# Operators
t_EQ = r'=='
t_NE = r'!='

# Delimiters
t_LCODEDELIM = r'{%'
t_RCODEDELIM = r'%}'
t_LVARDELIM = r'{{'
t_RVARDELIM = r'}}'

reserved_map = {}
for r in reserved:
    reserved_map[r.lower()] = r


def t_QUOTEDSTRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    return t


def t_STRING(t):
    r'[A-Za-z0-9_"]+'
    t.type = reserved_map.get(t.value, "STRING")
    return t


def t_HTML(t):
    r'[A-Za-z0-9<>/"]+'
    r'[^\s]+'
    t.type = reserved_map.get(t.value, "HTML")
    return t


def t_error(t):
    print("Illegal character %s" % repr(t.value[0]))
    t.lexer.skip(1)


lexer = lex.lex()
if __name__ == '__main__':

    tests = [
        '{{ben}}',
        '{% if variable == "test" %}foo{{variable}}{% else %}bar{% endif %}',
        'This should be text with {{a_variable}} followed by more text',
        """
        This should be text with {{a_variable}} followed by more text
        {% if variable == "test" %}
        foo
        {{variable}}
        {% else %}
        bar
        {% endif %}
        """,
        '<body><h1>This is some html</h1></body>',
        """{% if variable == "test" %}
        <body><h1>This is some {{variable}} html</h1></body>
        {% endif %}
        """
    ]

    for input_str in tests:
        print('Lexing', input_str)
        lexer.input(input_str)
        for tok in lexer:
            print(tok)
