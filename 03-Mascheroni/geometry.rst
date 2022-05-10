Modulo di supporto per la geometria
===================================

.. module:: geometry

Questo documento descrive le classi e le funzioni provviste dal modulo Python
`geometry` che possono essere liberamente utilizzate nello sviluppo
dell'interprete per il linguaggio Mascheroni.

Il modulo dipende dalle librerie `SymPy <https://www.sympy.org/>`_ (per le
primitive geometriche) e `drawSvg <https://github.com/cduck/drawSvg>`_ (per la
parte di rappresentazione grafica) che devono essere installate come illustrato
nella relativa documentazione.

Tra le classi proviste da SymPy, per la realizzazione del progetto sono
particolarmente rilevanti :obj:`~sympy.geometry.point.Point`,
:obj:`~sympy.geometry.line.Segment`, :obj:`~sympy.geometry.line.Ray` e
:obj:`~sympy.geometry.line.Line`, che rispecchiano gli enti di Mascheroni; manca
però una classe che rappresenti una circonferenza data dal suo centro e da un
punto su di essa, a tale scopo la libreria di supporto definisce la seguente

.. autoclass:: CirclePoint

Dal momento che i tipi di Mascheroni possono essere convenientemente
rappresentati dal valore dei token che li descrivono (ossia da delle stringhe),
sono provviste due funzioni, la prima per costruire un ente da un nome di tipo

.. autofunction:: make_entity

e la seconda per determinare se un certo oggetto è di uno (o di una famiglia) di
tali tipi

.. autofunction:: isnamedinstance

L'operazione di intersezione "ordinata" necessaria a definire la semantica delle
ocmputazioni in Mascheroni non è di banale implementazione, per questa ragione
il modulo ne fornisce una versione attraverso la funzione

.. autofunction:: intersection

Per finire, il modulo consente di ottenere una rappresentazione grafica in
formato `SVG <https://developer.mozilla.org/en-US/docs/Web/SVG>`_ grazie alla
funzione

.. autofunction:: to_svg
