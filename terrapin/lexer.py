from ply import lex

from terrapin.exceptions import TemplateError

word_regex = r'[A-Za-z0-9_\.]+'


class Lexer(object):

    reserved = (
        'IF', 'ELSE', 'ENDIF'
    )

    tokens = reserved + (
        # Code delimiters
        'LCODEDELIM', 'RCODEDELIM', 'LVARDELIM', 'RVARDELIM',
        # Operators
        'EQ', 'NE',
        # Literals
        'WS', 'WORD', 'QUOTEDSTRING', 'STRING',
    )

    # t_ignore = r' '  # string.whitespace

    def token_type(self, value, default):

        if value.upper() in self.reserved:
            return value.upper()
        else:
            return default

    def __init__(self):
        self.lexer = lex.lex(module=self)

    def tokenize(self, template):
        """A debug method to print out the tokens generated by the lexer"""
        self.lexer.input(template)
        while True:
            tok = self.lexer.token()
            if tok:
                yield tok
            else:
                break

    def t_LCODEDELIM(self, t):
        r'{%'
        return t

    def t_RCODEDELIM(self, t):
        r'%}'
        return t

    def t_LVARDELIM(self, t):
        r'{{'
        return t

    def t_RVARDELIM(self, t):
        r'}}'
        return t

    def t_EQ(self, t):
        r'=='
        return t

    def t_NE(self, t):
        r'!='
        return t

    @lex.TOKEN(word_regex)
    def t_WORD(self, t):

        t.type = self.token_type(t.value, "WORD")
        return t

    def t_WS(self, t):
        r'[\s]+'
        t.lexer.lineno += t.value.count("\n")
        return t

    def t_QUOTEDSTRING(self, t):
        r"""[\"].*?[\"]|[\'].*?[\']"""
        return t

    def t_STRING(self, t):
        r'([^\{\}]|[\{](?!%|{)|(?<!%|})[\}])+'
        t.type = self.token_type(t.value, "STRING")
        return t

    def t_error(self, t):
        raise TemplateError(t.lexer.lineno, t.lexer.lexpos, t.value[:10])

if __name__ == '__main__':

    s = """{% if in_context %}{% if in_context == "Working" %}Working ^^ hello{% endif %}{% endif %}"""
    toks = Lexer().tokenize(s)
    for tok in toks:
        print(tok)
