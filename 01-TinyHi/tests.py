# Test per il progetto "Tiny Hi"

# I test contenuti in questo file operano sotto l'assunzione che esistano due funzioni
# di nome parse e run dal seguente comportamento:
#
# * parse: accetta in ingresso una stringa e ne effettua il parsing, se la stringa
#          rappresenta un programma sintatticamente corretto, la funzione non
#          solleva eccezioni (il suo valore di ritorno è ignorato).
# * run:   accetta in ingresso una stringa e due funzioni, rispettivamente per l'input
#          e l'output; se la stringa rappresenta un programma sintatticamente corretto
#          lo esegue, se il programma non contiene errori semantici la funzione non
#          solleva eccezioni (il suo valore di ritorno è ignorato).
#          Per ogni istruzione `? VAR` l'interprete invoca la funzione di input e
#          assegna a `VAR` il valore che essa restituisce, similmente, per ogni
#          istruzione che produce output, interprete invoca la funzione di output
#          passando per argomento il valore (o vettore di valori) da emettere.
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

    'block_unnamed': r"""
      BEGIN
        1
      END
    """,
    'block_named': r"""
      BEGIN TEST
        1
      END
    """,
    'block_args1': r"""
      BEGIN ARG(ONE)
        1
      END
    """,
    'block_args2': r"""
      BEGIN ARG(ONE, TWO)
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
      BEGIN
        X <- 1
      END
    """,
    'empty_assignement': r"""
      BEGIN
        X <-
      END
    """,
    'exprstm': r"""
      BEGIN
        1 + 2
      END
    """,
    'if': r"""
      BEGIN
        IF X < 1
          1
        END
      END
    """,
    'ifelse': r"""
      BEGIN
        IF X < 1
          1
        ELSE
          2
        END
      END
    """,
    'while': r"""
      BEGIN
        WHILE X < 1
          1
        END
      END
    """,
    'until': r"""
      BEGIN
        UNTIL X < 1
          1
        END
      END
    """,
    'atoms': r"""
      BEGIN
        X <- 1
        X <- "TEST"
        X <- A
        X <- F(1)
        X <- F("ONE")
        X <- F(1, 2)
        X <- F("ONE", "TWO")
      END
    """,
    'unary': r"""
      BEGIN
        X <- -1
        X <- ~ 1
        X <- ~1
        X <- # 1
        X <- #1
      END
    """,
    'binops': r"""
      BEGIN
        X <- 1 + 2
        X <- 1 - 2
        X <- 1 / 2
        X <- 1 * 2
      END
    """,
    'conds': r"""
      BEGIN
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
      BEGIN
        X <- 1 2 3
        X <- "ONE" "TWO" "THREE"
        X <- 1 A F(1)
        X <- "ONE" A F("ONE")
      END
    """,
    'expr_list': r"""
      BEGIN
        X <- 1 2 + 3 4
        X <- 1 + # 2 3
        X <- 2 + ~ 1
      END
    """,
    'expr_func': r"""
      BEGIN
        X <- F(1 2)
        X <- 1 F(1) G (2)
      END
    """,
    'expr_prec': r"""
      BEGIN
        X <- 1 + 2 * 3
        X <- 1 ~ 2 * 3
        X <- 1 # 2 * 3
      END
    """,
}

# Test per l'interprete, viene verificato che non vengano sollevate eccezioni
# e cbe per il dato input, l'output sia uguale a quello atteso.

INTERPRETER_TESTS = {

    'vector': [r"""""", [1, 2], [(2,), (1,)]]

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
    def _make_test(source, inputs, expected):
        outputs= []
        iterinputs = iter(inputs)
        def _input():
            return next(iterinputs)
        def _output(*args):
            print(args)
            outputs.append(args)
        def _test(self):
            actual = StringIO()
            try:
                with redirect_stdout(actual): run(source, _input, _output)
            except Exception as e:
                self.fail('Exception: {}'.format(e))
            self.assertEqual(expected, outputs)
        return _test
    for name, (source, inputs, expected) in INTERPRETER_TESTS.items():
        setattr(TestInterpreter, 'test_{0}'.format(name), _make_test(source, inputs, expected))

if __name__ == '__main__':
    add_parser_tests()
    add_interpreter_tests()
    unittest.main(exit = False)