from ply.lex import lex, LexToken


class TokenError(BaseException):
    def __init__(self, token: LexToken):
        self._token = token

    def token(self) -> LexToken:
        return self._token


literals = [',', '.', '=', ':', ';']

reserved = ['TRUE', 'FALSE', 'NULL']

tokens = [*reserved, 'iFLOAT', 'iINTEGER', 'iKEYWORD', 'iCHAR', 'iESCAPE_CHAR', 'iESCAPE', 'iLBRACE', 'iRBRACE']

states = (
    ('str', 'inclusive'),
    ('escape', 'inclusive'),
)

t_ignore = " \t\r"
t_ignore_comment = r"\#[^\n]{0,}"

t_iINTEGER = r'\d+'
t_iFLOAT = r'\d+\.\d+'


def t_iKEYWORD(t: LexToken):
    r'[a-zA-Z][a-zA-Z0-9_]+'
    if t.value.upper() in reserved:
        t.type = t.value.upper()
    else:
        t.type = 'iKEYWORD'

    return t


def t_begin_str(t: LexToken):
    r"\""
    t.lexer.push_state('str')
    t.type = 'iLBRACE'
    return t


def t_str_escape(t: LexToken):
    r"\\"
    t.lexer.push_state('escape')
    t.type = 'iESCAPE'
    return t


def t_escape_end(t: LexToken):
    r"."
    t.lexer.pop_state()
    t.type = 'iESCAPE_CHAR'
    return t


# t_str_end 比 t_str_iCHAR 优先级高
def t_str_end(t: LexToken):
    r"\""
    t.lexer.pop_state()
    t.type = 'iRBRACE'
    return t


def t_str_iCHAR(t: LexToken):
    r"."
    return t


def t_newline(t: LexToken):
    r"\n"
    t.lexer.lineno += 1


def t_error(t: LexToken):
    raise TokenError(t)


lexer = lex(debug=True)
