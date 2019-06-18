# Test per il progetto "Logo"

# I test contenuti in questo file operano sotto l'assunzione che esistano due funzioni
# di nome parse e run dal seguente comportamento:
#
# * parse: accetta in ingresso una stringa e ne effettua il parsing, se la stringa
#          rappresenta un programma Logo sintatticamente corretto, la funzione non 
#          solleva eccezioni (il suo valore di ritorno è ignorato).
# * run:   accetta in ingresso una stringa e, se la stringa rappresenta un programma
#          Logo sintatticamente corretto lo esegue, se il programma non contiene errori
#          semantici la funzione non solleva eccezioni (il suo valore di ritorno è ignorato).
#          L'interprete è tale per cui l'istruzione PRINT emette il suo risultato nel
#          flusso d'uscita standard (seguito da un '\n').
# 
# Le seguenti importazioni assumono che le due funzioni si trovino in due file distinti,
# se la vostra implementazione è differente potete alterare le prossime righe di questo file
# in modo da importare quanto necessario dal vostro codice ed eventualmente avvolgerlo
# in due funzioni "parse" e "run" dal comportamento specificato sopra.

from parser import parse
from interpreter import run

# Per eseguire i test è sufficiente invocare il comando 'python3 tests.py'.
#
# In caso di fallimento di un test, la libreria di testing unittest di Python ne riporta
# il nome, come ad esempio in
# 
#   FAIL: test_simple_make (__main__.TestInterpreter)
#
# per rintracciare il sorgente del programma Logo (e l'eventuale output atteso) è sufficiente
# consultare i dizionari PARSER_TESTS e INTERPRETER_TESTS alla chiave corrispondente al 
# nome del test fallito (omettendo il prefisso 'test_'); ad esempio nel caso precedente,
# trattandosi di un fail in 'TestInterpreter' sorgente e valore atteso saranno in
# 
#   INTERPRETER_TESTS['simple_make']
#
# La parte finale di questo file contiene le funzioni che eseguono i test e non
# deve essere modificata.

# Test per il parser, l'unica cosa verificata è che non vengano sollevate eccezioni.

PARSER_TESTS = {
    
    'commands': r"""
    
        ARC 1 2
        BACK 1
        CLEAN
        CLEARSCREEN
        FORWARD 1
        HIDETURTLE
        HOME
        LEFT 1
        MAKE "a 1
        PENDOWN
        PENUP
        PRINT 1
        ( PRINT 1 2 )
        RERANDOM
        ( RERANDOM 1 )
        RIGHT 1
        SETHEADING 1
        SETPENCOLOR [ 1 2 3 ]
        SETPENSIZE 1
        SETX 1
        SETXY 1 2 
        SETY 1
        SHOWTURTLE

    """, 'operations': r"""
    
        ( PRINT

            ARCTAN 1
            ( ARCTAN 1 1 )
            COS 1
            DIFFERENCE 1 2
            EXP 1
            GREATEREQUALP 1 2 
            GREATERP 1 2 
            INT 1
            LESSEQUALP 1 2 
            LESSP 1 2 
            LN 1
            LOG10 1
            MINUS 1
            MODULO 1 2
            POWER 1 2 
            PRODUCT 1 2
            ( PRODUCT 1 2 3 )
            QUOTIENT 1 2
            ( QUOTIENT 1 )
            RADARCTAN 1
            ( RADARCTAN 1 1 )
            RADCOS 1
            RADSIN 1
            RANDOM 1
            ( RANDOM 1 1 )
            READWORD
            REMAINDER 1 2
            ROUND 1
            SIN 1
            SUM 1 2
            ( SUM 1 2 3 )
            SQRT 1

        )

    """, 'dots': r"""
    
        PR :a

    """, 'thing': r"""
    
        PR THING "a

    """, 'make1': r"""

        MAKE "RESULT 1

    """, 'make2': r"""

        MAKE :VAR AND [NOT (:X = 0)] [(1 / :X) > .5]
    
    """, 'repeat': r"""
    
        repeat 4 [fd 100 rt 90]

    """, 'while': r"""
    
        while :c < 1 [make "c :c + 1]
        
    """, 'koch': r"""
    
        to line :count :length
         ifelse :count = 1 [fd :length] [
           make "count :count -1 
           (line :count :length)
           lt 60 (line :count :length)
           rt 120 (line :count :length)
           lt 60 (line :count :length)
          ]
        end

        to koch :count :length  
          rt 30 (line :count :length)
          rt 120 (line :count :length)
          rt 120 (line :count :length)
        end

        cs
        setxy  0 0
        (koch 5 5)
        
    """, 'ifelse': r"""
    
        if :x < 1 [pr 2]
        ifelse "a = "b [pr 3] [pr 4]
        pr if :a = 0 [5]
        pr ifelse :a = 0 [6] [7]
        
    """, 'userprocinv': r"""
        
        USER 1
        (USER 1 2 3)
        
    """, 'logic1': r"""

        ( PRINT 

            AND :a = 0 :b > 1
            ( AND :a = 0 :b > 1 NOT :c )
            OR  :a = 0 :b > 1
            ( OR :a = 0 :b > 1 NOT :c )
            NOT :c
        )

    """, 'logic2': r"""
        
        ( PRINT 
            AND [:a = 0 :b > 1] [:a = 0 :b > 1]
            ( AND [:a = 0 :b > 1] [:a = 0 :b > 1] [OR :c NOT :d] )
            OR  [:a = 0 :b > 1] [:a = 0 :b > 1]
            ( OR [:a = 0 :b > 1] [:a = 0 :b > 1] [OR :c NOT :d] )
            NOT [OR :c NOT :d]
        )
    """
}

# Test per l'interprete, viene verificato che non vengano sollevate eccezioni 
# e l'output sia uguale a quello atteso.

INTERPRETER_TESTS = {
    
    'simple_make': [
        r"""
            MAKE "A 1
            PR :A
        """, 
        '1\n'
    ], 'make_with_expr_name': [
        r"""
            MAKE "NAME "A
            MAKE :NAME 1
            PR :A
        """,
        '1\n'
    ], 'if_as_statement_true': [
        r"""
            IF "TRUE [PRINT 1]
            PRINT 2
        """,
        '1\n2\n'
    ], 'if_as_statement_false': [
        r"""
            IF FALSE [PRINT 1]
            PRINT 2
        """,
        '2\n'
    ], 'ifelse_as_statement_true': [
        r"""
            IFELSE "TRue [PRINT 1] [PRINT 2]
            PRINT 3
        """,
        '1\n3\n'
    ], 'ifelse_as_statement_false': [
        r"""
            IFELSE "FALSE [PRINT 1] [PRINT 2]
            PRINT 3
        """,
        '2\n3\n'
    ], 'ifelse_as_operation_true': [
        r"""
            PRINT IFELSE "TRue [1] [2]
            PRINT 3
        """,
        '1\n3\n'
    ], 'ifelse_as_operation_multiple_expr': [
        r"""
            PRINT IFELSE "TRue [1 2 3] [4]
            PRINT 5
        """,
        '3\n5\n'
    ], 'ifelse_as_operation_side_effects': [
        r"""
            PRINT IFELSE "TRue [MAKE "A 1 2 :A MAKE "A 3] [3]
            PRINT 4
        """,
        '1\n4\n'
    ], 'ifelse_as_operation_false': [
        r"""
            PRINT IFELSE FALSE [1] [2]
            PRINT 3
        """,
        '2\n3\n'
    ], 'short_circuit' : [
        r"""
            MAKE "X 0
            IFELSE AND [NOT (:X = 0)] [(1 / :X) > .5] [PR 1] [PR 2]
            MAKE "X 1
            IFELSE AND [NOT (:X = 0)] [(1 / :X) > .5] [PR 1] [PR 2]
        """,
        '2\n1\n'
    ], 'bool_expr_and_false' : [
        r"""
            IF AND "TRUE "FALSE [PR 1] PR 2
            IF AND TRUE "FALSE [PR 3] PR 4
            IF AND "TRUE FALSE [PR 5] PR 6
            IF AND TRUE FALSE [PR 7] PR 8
        """,
        '2\n4\n6\n8\n'
    ], 'bool_expr_and_true' : [
        r"""
            IF AND "TRUE "TRUE [PR 1] PR 2
            IF AND TRUE "TRUE [PR 3] PR 4
            IF AND "TRUE TRUE [PR 5] PR 6
            IF AND TRUE TRUE [PR 7] PR 8
        """,
        '1\n2\n3\n4\n5\n6\n7\n8\n'
    ], 'bool_expr_or_true' : [
        r"""
            IF OR "TRUE "FALSE [PR 1] PR 2
            IF OR TRUE "FALSE [PR 3] PR 4
            IF OR "TRUE FALSE [PR 5] PR 6
            IF OR TRUE FALSE [PR 7] PR 8
        """,
        '1\n2\n3\n4\n5\n6\n7\n8\n'
    ], 'bool_expr_or_false' : [
        r"""
            IF OR "FALSE "FALSE [PR 1] PR 2
            IF OR FALSE "FALSE [PR 3] PR 4
            IF OR "FALSE FALSE [PR 5] PR 6
            IF OR FALSE FALSE [PR 7] PR 8
        """,
        '2\n4\n6\n8\n'
    ], 'bool_three' : [
        r"""
            IF AND [AND "TRUE TRUE] TRUE [PR 1] PR 2
        """,
        '1\n2\n'
    ], 'repeat' : [
        r"""
        MAKE "C 0
        REPEAT 4 [MAKE "C :C + 1]
        PR :C
        """,
        '4\n'
    ], 'while' : [
        r"""
        MAKE "C 0
        WHILE :C < 4 [MAKE "C :C + 1]
        PR :C
        """,
        '4\n'
    ], 'func_biarg' : [
        r"""
            TO FUNC :X :Y
                OUTPUT :X + :Y
            END

            PR (FUNC 3 4)
        """,
        '7\n'
    ], 'stop' : [
        r"""
            TO FUNC
                PR 1
                STOP 
                PR 2
            END

            (FUNC)
        """,
        '1\n'
    ], 'stop_repeat' : [
        r"""
            TO FUNC
                REPEAT 4 [PR 1 STOP]
            END

            (FUNC)
        """,
        '1\n'
    ], 'stop_while' : [
        r"""
            TO FUNC
                MAKE "N 4
                WHILE :N > 0 [
                    MAKE "N :N - 1
                    PR 1 
                    STOP
                ]
            END

            (FUNC)
        """,
        '1\n'
    ], 'output_repeat' : [
        r"""
            TO FUNC
                REPEAT 4 [PR 1 OUTPUT 2]
            END

            (FUNC)
        """,
        '1\n'
    ], 'OUTPUT_while' : [
        r"""
            TO FUNC
                MAKE "N 4
                WHILE :N > 0 [
                    MAKE "N :N - 1
                    PR 1 
                    OUTPUT 2
                ]
            END

            (FUNC)
        """,
        '1\n'
    ], 'output' : [
        r"""
            TO FUNC
                PR 1
                OUTPUT 2
                PR 3
            END

            (FUNC)
        """,
        '1\n'
    ], 'factorial' : [
        r"""
            TO FACTORIAL :N
                IF :N = 0 [OUTPUT 1]
                OUTPUT :N * FACTORIAL :N - 1
            END
            PR (FACTORIAL 6)
        """,
        '720\n'
    ], 'fibonacci' : [
        r"""
            TO FIBONACCI :N
                IF :N <= 1 [OUTPUT :N]
                OUTPUT (FIBONACCI :N - 2) + (FIBONACCI :N - 1)
            END
            PR (FIBONACCI 7)
        """,
        '13\n'
    ]
}

#############################################################################

# Il codice da questo commento in poi non deve essere modificato.

import unittest
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO

class TestParser(unittest.TestCase):
    pass

def add_parser_tests():
    def _make_test(source):
        def _test(self):
            try:
                with redirect_stdout(StringIO()): parse(source)
            except Exception as e:
                self.fail('Exception: {}'.format(e))
        return _test
    for name, source in PARSER_TESTS.items():
        setattr(TestParser, 'test_{0}'.format(name), _make_test(source))

class TestInterpreter(unittest.TestCase):
    pass

def add_interpreter_tests():
    def _make_test(source, expected):
        def _test(self):
            actual = StringIO()
            try:
                with redirect_stdout(actual): run(source)
            except Exception as e:
                self.fail('Exception: {}'.format(e))
            self.assertEqual(expected, actual.getvalue())
        return _test
    for name, (source, expected) in INTERPRETER_TESTS.items():
        setattr(TestInterpreter, 'test_{0}'.format(name), _make_test(source, expected))     

if __name__ == '__main__': 
    add_parser_tests()
    add_interpreter_tests()
    unittest.main(exit = False)