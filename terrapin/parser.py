from ply import yacc

from terrapin.lexer import Lexer


class Parser(object):

    def __init__(self):

        self.lexer = Lexer()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self, debug=False)

    def parse(self, template, context):

        self.context = context

        if template:
            return self.parser.parse(template, lexer=self.lexer.lexer)

    def show_tokens(self, template):
        return self.lexer.tokenize(template)

    def p_output(self, p):
        """output : html
                  | output output
        """
        p[0] = ' '.join([wrd for wrd in p[1:]])

    def p_html(self, p):
        """html : WORD
                | STRING
                | WHITESPACE
                | variable
                | html html
        """
        p[0] = ' '.join([wrd for wrd in p[1:]])

    def p_variable(self, p):
        'variable : LVARDELIM WORD RVARDELIM'
        p[0] = self.context.get(p[2], '')

    def p_if_statement(self, p):
        """output : if_result html end_if
        """
        p[0] = p[2] if p[1] else ''

    def p_if_else_statement(self, p):
        """output : if_result html else html end_if
        """
        p[0] = p[2] if p[1] else p[4]

    def p_truthy_if(self, p):
        """if_result : LCODEDELIM IF WORD RCODEDELIM
        """
        p[0] = True if p[3] else False

    def p_equality_if(self, p):
        """if_result : LCODEDELIM IF WORD EQ QUOTEDSTRING RCODEDELIM
        """
        p[0] = True if self.context.get(p[3]) == p[5] else False

    def p_non_equality_if(self, p):
        """if_result : LCODEDELIM IF WORD NE QUOTEDSTRING RCODEDELIM
        """
        p[0] = True if not self.context.get(p[3]) == p[5] else False

    def p_else(self, p):
        """else : LCODEDELIM ELSE RCODEDELIM
        """
        p[0] = None

    def p_end_if(self, p):
        """end_if : LCODEDELIM ENDIF RCODEDELIM
        """
        p[0] = None

    def p_error(self, p):
        if p:
            print("Syntax error Line: {l} Pos: {p} at '{s}'".format(
                l=p.lineno, p=p.lexpos, s=p.value))
        else:
            print("Syntax error at EOF")
