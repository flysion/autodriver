import ply.yacc as yacc

from .lex import TokenError, LexToken, lexer, tokens


def p_error(t: LexToken):
    raise TokenError(t)


def p_start(p):
    """
    start : body
          | newlines
          | newlines body
          | body newlines
          | newlines body newlines
          |
    """
    if len(p) >= 3 and p[2] is not None:
        p[0] = p[2]
    elif len(p) >= 2 and p[1] is not None:
        p[0] = p[1]
    else:
        p[0] = []


def p_body(p):
    """
    body : comment
         | command
         | label
    """
    p[0] = [p[1]]


def p_body_1(p):
    """
    body : body newlines comment
         | body newlines command
         | body newlines label
    """
    p[0] = [*p[1], p[3]]


def p_newlines(p):
    """
    newlines : iNEWLINE
             | newlines iNEWLINE
    """
    p[0] = None


def p_comment(p):
    """
    comment : iCOMMENT
    """
    p[0] = {'type': 'comment', 'text': p[1], 'lineno': p.lineno(1), 'pos': p.lexpos(1)}


def p_label(p):
    """
    label : iKEYWORD ':'
    """
    p[0] = {'type': 'label', 'name': p[1], 'lineno': p.lineno(1), 'pos': p.lexpos(1)}


def p_command(p):
    """
    command : iKEYWORD
    """
    p[0] = {'type': 'command', 'name': p[1], 'args': [], 'kwargs': [], 'lineno': p.lineno(1), 'pos': p.lexpos(1)}


def p_command_1(p):
    """
    command : iKEYWORD args
    """
    p[0] = {'type': 'command', 'name': p[1], 'args': p[2], 'kwargs': [], 'lineno': p.lineno(1), 'pos': p.lexpos(1)}


def p_command_2(p):
    """
    command : iKEYWORD kwargs
    """
    p[0] = {'type': 'command', 'name': p[1], 'args': [], 'kwargs': p[2], 'lineno': p.lineno(1), 'pos': p.lexpos(1)}


def p_command_3(p):
    """
    command : iKEYWORD args ',' kwargs
    """
    p[0] = {'type': 'command', 'name': p[1], 'args': p[2], 'kwargs': p[4], 'lineno': p.lineno(1), 'pos': p.lexpos(1)}


def p_args(p):
    """
    args : value
    """
    p[0] = [p[1]]


def p_args_1(p):
    """
    args : args ',' value
    """
    p[0] = [*p[1], p[3]]


def p_value_int(p):
    """
    value : iINTEGER
    """
    p[0] = {'type': 'integer', 'text': p[1], 'lineno': p.lineno(1), 'pos': p.lexpos(1)}


def p_value_float(p):
    """
    value : iFLOAT
    """
    p[0] = {'type': 'float', 'text': p[1], 'lineno': p.lineno(1), 'pos': p.lexpos(1)}


def p_value_bool(p):
    """
    value : TRUE
          | FALSE
    """
    p[0] = {'type': 'bool', 'text': p[1], 'lineno': p.lineno(1), 'pos': p.lexpos(1)}


def p_value_null(p):
    """
    value : NULL
    """
    p[0] = {'type': 'null', 'text': p[1], 'lineno': p.lineno(1), 'pos': p.lexpos(1)}


def p_value_str(p):
    """
    value : str
    """
    p[0] = {'type': 'string', 'text': p[1][0], 'lineno': p[1][1], 'pos': p[1][2]}


def p_value_keyword(p):
    """
    value : keyword
    """
    p[0] = {'type': 'keyword', 'text': p[1][0], 'lineno': p[1][1], 'pos': p[1][2]}


def p_keyword(p):
    """
    keyword : iKEYWORD
    """
    p[0] = (p[1], p.lineno(1), p.lexpos(1))


def p_keyword_1(p):
    """
    keyword : keyword '.' iKEYWORD
    """
    p[0] = (p[1][0] + '.' + p[3], p[1][1], p[1][2])


def p_kwarg(p):
    """
    kwarg : iKEYWORD '=' value
    """
    p[0] = {'name': p[1], 'value': p[3], 'lineno': p.lineno(1), 'pos': p.lexpos(1)}


def p_kwargs(p):
    """
    kwargs : kwarg
    """
    p[0] = [p[1]]


def p_kwargs_1(p):
    """
    kwargs : kwargs ',' kwarg
    """
    p[0] = [*p[1], p[3]]


def p_str(p):
    """
    str : iLBRACE chars iRBRACE
    """
    p[0] = (p[2], p.lineno(1), p.lexpos(1))


def p_chars(p):
    """
    chars : char
    """
    p[0] = p[1]


def p_chars_1(p):
    """
    chars : chars char
    """
    p[0] = p[1] + p[2]


def p_char(p):
    """
    char : iCHAR
    """
    p[0] = p[1]


def p_char_escape(p):
    """
    char : iESCAPE iESCAPE_CHAR
    """
    p[0] = p[2]


parser = yacc.yacc(start='start', debug=False)


def parse(input: str):
    return parser.parse(input, lexer=lexer())
