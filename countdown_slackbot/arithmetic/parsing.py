import ply.lex as lex
import ply.yacc as yacc


PLY_INITIALISED = False


def raw_parse(some_string):
    global PLY_INITIALISED

    if not PLY_INITIALISED:
        lex.lex()
        yacc.yacc()
        PLY_INITIALISED = True

    return yacc.parse(some_string)


# Grammar code starts here!
# Ultimately I implemented a subset of http://users.monash.edu/~lloyd/tildeProgLang/Grammar/Arith-Exp/
# with ply.


tokens = ["NUMBER", "PLUS", "MINUS", "MULTIPLY", "DIVIDE", "EQUALS", "LPAREN", "RPAREN"]

t_PLUS = r"\+"
t_MINUS = r"-"
t_MULTIPLY = r"\*"
t_DIVIDE = r"/"
t_EQUALS = r"="
t_LPAREN = r"\("
t_RPAREN = r"\)"

t_ignore = " \t"


def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


precedence = [
    ("left", "PLUS", "MINUS"),
    ("left", "MULTIPLY", "DIVIDE"),
]


def p_statement_assertion(p):
    """statement : expression assertion
    """
    p[0] = ("assertion", p[1], p[2])


def p_assertion_simple(p):
    """assertion : EQUALS expression
    """
    p[0] = [p[2]]


def p_assertion_multiple(p):
    """assertion : EQUALS expression assertion
    """
    p[0] = [p[2]] + p[3]


def p_statement_expression(p):
    """statement : expression
    """
    # Return the parsed format... ?
    p[0] = ("expression", p[1])


def p_expression_binop(p):
    """expression : expression PLUS term
                  | expression MINUS term
    """
    p[0] = (p[1], p[2], p[3])


def p_expression_term(p):
    """expression : term
    """
    p[0] = p[1]


def p_term_binop(p):
    """term : term MULTIPLY factor
            | term DIVIDE factor
    """
    p[0] = (p[1], p[2], p[3])


def p_term_factor(p):
    """term : factor
    """
    p[0] = p[1]


def p_factor_number(p):
    """factor : NUMBER
    """
    p[0] = p[1]


def p_factor_expression(p):
    """factor : LPAREN expression RPAREN
    """
    p[0] = p[2]


def p_error(p):
    raise Exception("Syntax error at '%s'" % p.value)
