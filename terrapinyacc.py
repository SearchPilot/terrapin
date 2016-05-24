import ply.yacc as yacc

from terrapinlex import tokens, lexer

context = {
    'in_context': 'Working',
}


def p_output(p):
    """output : html
              | output output
    """
    p[0] = ' '.join([wrd for wrd in p[1:]])


def p_html(p):
    """html : WORD
            | STRING
            | WHITESPACE
            | variable
            | html html
    """
    p[0] = ' '.join([wrd for wrd in p[1:]])


def p_variable(p):
    'variable : LVARDELIM WORD RVARDELIM'
    p[0] = context.get(p[2], '')


def p_if_statement(p):
    """output : if_result html end_if
    """
    p[0] = p[2] if p[1] else ''


def p_if_else_statement(p):
    """output : if_result html else html end_if
    """
    p[0] = p[2] if p[1] else p[4]


def p_truthy_if(p):
    """if_result : LCODEDELIM IF WORD RCODEDELIM
    """
    p[0] = True if p[3] else False


def p_equality_if(p):
    """if_result : LCODEDELIM IF WORD EQ QUOTEDSTRING RCODEDELIM
    """
    p[0] = True if context.get(p[3]) == p[5] else False


def p_non_equality_if(p):
    """if_result : LCODEDELIM IF WORD NE QUOTEDSTRING RCODEDELIM
    """
    p[0] = True if not context.get(p[3]) == p[5] else False


def p_else(p):
    """else : LCODEDELIM ELSE RCODEDELIM
    """
    p[0] = None


def p_end_if(p):
    """end_if : LCODEDELIM ENDIF RCODEDELIM
    """
    p[0] = None


def p_error(p):
    if p:
        print("Syntax error Line: {l} Pos: {p} at '{s}'".format(l=p.lineno, p=p.lexpos, s=p.value))
    else:
        print("Syntax error at EOF")


if __name__ == '__main__':

    test_templates = [
        'Working',
        'Working working',
        '<body><h1>Working</h1></body>',
        '<body><h1>Working working</h1></body>',
        """
        This \t has \t some\n\n
        white space


        in it
        """,
        '{{in_context}}',
        '{{not_in_context}}',
        '{% if in_context %}Working{% endif %}',
        '{% if in_context == "Working" %}Working{% endif %}',
        '{% if in_context == "Working" %}Working {{in_context}}{% endif %}',
        '{% if in_context == "Working" %}Working {{not_in_context}}{% endif %}',
        '{% if in_context == "Not Working" %}Not Working{% else %}Working {{in_context}}{% endif %}',
        '{% if in_context == "Not Working" %}Not Working{% else %}Working {{not_in_context}}{% endif %}',
        """
        {% if in_context == "Not Working" %}
            Not Working
        {% else %}
            <body><h1 id="test " class= "testing">This is some html</h1></body>
            <a href="http://www.distilled.net/?test=foo;bob=bar">R&amp;D</a>
            Working {{in_context}}
        {% endif %}
        """
    ]

    n = 1000

    # lexer = lex.lex()

    for i, template in enumerate(test_templates):

        lexer.lineno = 1

        print('----------------')
        print("Template {i}: {t}".format(i=i, t=template))
        parser = yacc.yacc(debug=False)
        # lexer.input(template)
        # for tok in lexer:
        #     print(tok)
        result = parser.parse(template, lexer=lexer)
        print('Result: ', result)
        print('')

    for i, template in enumerate(test_templates):
        import time
        start_time = time.time()
        for _ in range(n):
            parser = yacc.yacc(debug=False)
            result = parser.parse(template, lexer=lexer)
        end_time = time.time()
        ms = (end_time - start_time) * 1000
        a = ms / n
        print('Template {i} completed {n} loops in {ms}ms Avg ({a})'.format(i=i, n=n, ms=ms, a=a))
