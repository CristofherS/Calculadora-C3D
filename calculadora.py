#clase que guardara nuestro codigo tres direcciones y variables temporales
class Nodo():
    def __init__(self, temporal = '', c3d = ''):
        self.temporal = temporal
        self.c3d = c3d

#Tokens
tokens = (
    'ID','ENTERO', 'DECIMAL',
    'SUMA','RESTA','MULTIPLICA','DIVIDE',
    'PARIZQ','PARDER',
    )

t_SUMA    = r'\+'
t_RESTA   = r'-'
t_MULTIPLICA   = r'\*'
t_DIVIDE  = r'/'
t_PARIZQ  = r'\('
t_PARDER  = r'\)'

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Error, entero fuera de rango %d", t.value)
        t.value = 0
    return t

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Error, decimal fuera de rango %d", t.value)
        t.value = 0
    return t

def t_ID(t):
     r'[a-zA-Z_@#][a-zA-Z_0-9@$#]*'
     t.type = 'ID'
     return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Caracter incorrecto '%s'" % t.value[0])
    t.lexer.skip(1)

import ply.lex as lex
lexer = lex.lex()

#funcion que manejara las varibales temporales para nuestro codigo tre direcciones
t = -1
def getTemporal():
    global t 
    t += 1
    return 't' + str(t)

#Gramatica y reglas gramaticales
precedence = (
    ('right','UMINUS'),
    )

def p_inicio_expr(t):
    'inicio : expression'
    t[0] = t[1]

def p_expression(t):
    '''expression : expression SUMA termino
                  | expression RESTA termino
                  | termino '''
    if len(t) > 2:
        t[0] = Nodo(temporal = getTemporal())
        if t[2] == '+'  : 
            t[0].c3d = t[1].c3d + t[3].c3d + t[0].temporal + ' = ' + t[1].temporal + ' + ' + t[3].temporal + ';\n'
        else:
            t[0].c3d = t[1].c3d + t[3].c3d + t[0].temporal + ' = ' + t[1].temporal + ' - ' + t[3].temporal + ';\n'
    else:
        t[0] = Nodo(t[1].temporal, t[1].c3d)

def p_expression_uminus(t):
    'expression : RESTA termino %prec UMINUS'
    t[0] = Nodo(temporal = getTemporal())
    t[0].c3d = t[2].c3d + t[0].temporal + ' = 0 - ' + t[2].temporal + ';\n'
    
def p_termino(t):
    '''termino : termino MULTIPLICA final
               | termino DIVIDE final
               | final'''
    if len(t) > 2:
        t[0] = Nodo(temporal = getTemporal())
        if t[2] == '*': 
            t[0].c3d = t[1].c3d + t[3].c3d + t[0].temporal + ' = ' + t[1].temporal + ' * ' + t[3].temporal + ';\n'
        else:
            t[0].c3d = t[1].c3d + t[3].c3d + t[0].temporal + ' = ' + t[1].temporal + ' / ' + t[3].temporal + ';\n'
    else:
        t[0] = Nodo(t[1].temporal, t[1].c3d)

def p_final_idNum(t):
    '''final : PARIZQ expression PARDER
             | ENTERO
             | DECIMAL
             | ID'''
    if len(t) > 2:
        t[0] = Nodo(t[2].temporal, t[2].c3d)
    else:
        t[0] = Nodo(temporal = str(t[1]))


def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()

while True:
    try:
        s = input('calcular > ')
    except EOFError:
        break
    print(parser.parse(s).c3d)
    t = -1