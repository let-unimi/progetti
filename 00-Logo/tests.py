from textwrap import dedent

try:
    from parser import parse

    def test(source, start = 'program', show_pt = False):
        if source in TESTS: source = TESTS[source]
        ast = parse(source)
        print(dedent(source).strip('\n'))
        return ast

except (ModuleNotFoundError, ImportError):

    def test(*args, **kwargs):
        raise NotImplementedError('No parser available')

TESTS = {
    
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
            READWORD 1
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
         ifelse :count = 1 [fw :length] [
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
        setxy  45 370
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
