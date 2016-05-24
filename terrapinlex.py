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

    # Operators
    'EQ', 'NE',

    # Literals
    'WHITESPACE', 'WORD', 'QUOTEDSTRING', 'STRING',

)

t_ignore = r' '  # string.whitespace

reserved_map = {}
for r in reserved:
    reserved_map[r.lower()] = r


def t_LCODEDELIM(t):
    r'{%'
    return t


def t_RCODEDELIM(t):
    r'%}'
    return t


def t_LVARDELIM(t):
    r'{{'
    return t


def t_RVARDELIM(t):
    r'}}'
    return t


def t_EQ(t):
    r'=='
    return t


def t_NE(t):
    r'!='
    return t


def t_WORD(t):
    r'[A-Za-z0-9_]+'
    t.type = reserved_map.get(t.value, "WORD")
    return t


def t_WHITESPACE(t):
    r'[\s]+'
    t.lexer.lineno += t.value.count("\n")
    return t


def t_DOUBLEQUOTEDSTRING(t):
    r'[\"].+[\"]'
    t.value = t.value[1:-1]
    t.type = reserved_map.get(t.value, "QUOTEDSTRING")
    return t


def t_SINGLEQUOTEDSTRING(t):
    r'[\'].+[\']'
    t.value = t.value[1:-1]
    t.type = reserved_map.get(t.value, "QUOTEDSTRING")
    return t


def t_STRING(t):
    r'.+'
    t.type = reserved_map.get(t.value, "STRING")
    return t


def t_error(t):
    print("Illegal character %s" % repr(t.value[0]))
    t.lexer.skip(1)


lexer = lex.lex()
if __name__ == '__main__':

    tests = [
        '{{ben}}',
        '{% if variable == "test" %}foo{{variable}}{% else %}bar{% endif %}',
        "{% if variable == 'test' %}foo{{variable}}{% else %}bar{% endif %}",
        """
        String
        \t\n\n
        with \t whitespace\n

        """,
        '<body><h1 id="test " class= "testing">This is some html</h1></body>',
        '<a href="http://www.distilled.net/?test=foo;bob=bar">R&amp;D</a>',
        """
        <script type="text/javascript">var bob='test'; var ben="testing"</script>
        """
    ]

    for input_str in tests:
        print('---------------------')
        print(input_str)
        lexer.input(input_str)
        for tok in lexer:
            print(tok)
        print('')
        print('')
