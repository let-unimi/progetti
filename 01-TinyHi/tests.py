# Test per il progetto "Tiny Hi"

# I test contenuti in questo file operano sotto l'assunzione che esistano due funzioni
# di nome parse e run dal seguente comportamento:
#
# * parse: accetta in ingresso una stringa e ne effettua il parsing, se la stringa
#          rappresenta un programma sintatticamente corretto, la funzione non
#          solleva eccezioni (il suo valore di ritorno è ignorato).
# * run:   accetta in ingresso una stringa e, se la stringa rappresenta un programma
#          sintatticamente corretto lo esegue, se il programma non contiene errori
#          semantici la funzione non solleva eccezioni (il suo valore di ritorno è ignorato).
#          L'interprete è tale per cui le istruzioni che emettono output lo emettono nel
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
#   FAIL: test_vector (__main__.TestInterpreter)
#
# per rintracciare il sorgente del programma Logo (e l'eventuale output atteso) è sufficiente
# consultare i dizionari PARSER_TESTS e INTERPRETER_TESTS alla chiave corrispondente al
# nome del test fallito (omettendo il prefisso 'test_'); ad esempio nel caso precedente,
# trattandosi di un fail in 'TestInterpreter' sorgente e valore atteso saranno in
#
#   INTERPRETER_TESTS['vector']
#
# La parte finale di questo file contiene le funzioni che eseguono i test e non
# deve essere modificata.

# Test per il parser, l'unica cosa verificata è che non vengano sollevate eccezioni.

PARSER_TESTS = {
    'block_named': r"""
      BEGIN PROG
        1
      END
    """,
    'block_args1': r"""
      BEGIN MAIN
        BEGIN ARG(ONE)
          1
        END
        1
      END
    """,
    'block_args2': r"""
      BEGIN MAIN
        BEGIN ARG(ONE, TWO)
          1
        END
        1
      END
    """,
    'block_nested': r"""
      BEGIN OUTER
        BEGIN INNER
          1
        END
        1
      END
    """,
    'block_parallel': r"""
      BEGIN OUTER
        BEGIN ONE
          1
        END
        BEGIN TWO
          1
        END
        1
      END
    """,
    'assignement': r"""
      BEGIN PROG
        X <- 1
      END
    """,
    'empty_assignement': r"""
      BEGIN PROG
        X <-
      END
    """,
    'exprstm': r"""
      BEGIN PROG
        1 + 2
      END
    """,
    'if': r"""
      BEGIN PROG
        IF X < 1
          1
        END
      END
    """,
    'ifelse': r"""
      BEGIN PROG
        IF X < 1
          1
        ELSE
          2
        END
      END
    """,
    'while': r"""
      BEGIN PROG
        WHILE X < 1
          1
        END
      END
    """,
    'until': r"""
      BEGIN PROG
        UNTIL X < 1
          1
        END
      END
    """,
    'atoms': r"""
      BEGIN PROG
        X <- 1
        X <- "TEST"
        X <- A
        X <- .A
        X <- F(1)
        X <- F("ONE")
        X <- F(1, 2)
        X <- F("ONE", "TWO")
      END
    """,
    'unary': r"""
      BEGIN PROG
        X <- -1
        X <- ~ 1
        X <- ~1
        X <- # 1
        X <- #1
      END
    """,
    'binops': r"""
      BEGIN PROG
        X <- 1 + 2
        X <- 1 - 2
        X <- 1 / 2
        X <- 1 * 2
      END
    """,
    'conds': r"""
      BEGIN PROG
        IF X < 1
          1
        END
        IF X <= 1
          1
        END
        IF X = 1
          1
        END
        IF X <> 1
          1
        END
        IF X >= 1
          1
        END
        IF X > 1
          1
        END
      END
    """,
    'list': r"""
      BEGIN PROG
        X <- 1 2 3
        X <- "ONE" "TWO" "THREE"
        X <- 1 A F(1)
        X <- "ONE" A F("ONE")
      END
    """,
    'expr_list': r"""
      BEGIN PROG
        X <- 1 2 + 3 4
        X <- 1 + # 2 3
        X <- 2 + ~ 1
      END
    """,
    'expr_func': r"""
      BEGIN PROG
        X <- F(1 2)
        X <- 1 F(1) G (2)
      END
    """,
    'expr_prec': r"""
      BEGIN PROG
        X <- 1 + 2 * 3
        X <- 1 ~ 2 * 3
        X <- 1 # 2 * 3
      END
    """,
    'block_args0_call': r"""
      BEGIN PROG
        BEGIN ZERO
        1
        END
        ZERO()
      END
    """
}

# Test per l'interprete, viene verificato che non vengano sollevate eccezioni
# e cbe per il dato input, l'output sia uguale a quello atteso.

INTERPRETER_TESTS = {
    'fact': [r"""
      BEGIN TEST
        BEGIN DOIT(N)
            BEGIN FACT(N)
                IF N = 0
                    FACT <- 1
                ELSE
                    FACT <- N * FACT(N - 1)
                END
            END
            DOIT <- FACT(2 * N)
        END
        DOIT(3)
      END
    """, '720'],
    'bagl': [r"""
      BEGIN PROG
        A <- "ALGEBRA"
        A[5 1 3 2]
      END
    """, 'BAGL'],
    'gcf': [r"""
      BEGIN MAIN
          BEGIN MOD(A, B)
              MOD <- A-B*(A/B)
          END
          BEGIN GCF(XD, YD)
              X <- XD
              Y <- YD
              IF X < Y
                  T <- X
                  X <- Y
                  Y <- T
                  T <-
              END
              R <- Y
              WHILE R > 0
                  R <- MOD(X, Y)
                  X <- Y
                  Y <- R
              END
              GCF <- X
          END
          GCF(2*3*5*5*7,2*2*3*5)
      END
    """, '30'],
    'no_args': [r"""
      BEGIN PROG
        BEGIN NOARG
          1
          NOARG <- -1
        END
        TEMP <- NOARG()
      END
    """, '1'],
    'inner_call' : [ r"""
      BEGIN PROG
        BEGIN FUNC(X)
          BEGIN CALL(Y)
            0
            CALL <- "CALL"
          END
          TEMP <- CALL(0)
          1
          FUNC <- "FUNC"
        END
        TEMP <- FUNC(0)
        2
      END
    """, '0\n1\n2'
    ],
    'no_inner_call' : [ r"""
      BEGIN PROG
        BEGIN FUNC(X)
          BEGIN NEVER(Y)
            0
            NEVER <- "NEVER"
          END
          1
          FUNC <- "FUNC"
        END
        TEMP <- FUNC(0)
        2
      END
    """, '1\n2'
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
            self.assertEqual(expected, actual.getvalue().strip())
        return _test
    for name, (source, expected) in INTERPRETER_TESTS.items():
        setattr(TestInterpreter, 'test_{0}'.format(name), _make_test(source, expected))

add_parser_tests()
add_interpreter_tests()

if __name__ == '__main__':
    unittest.main(exit = False)