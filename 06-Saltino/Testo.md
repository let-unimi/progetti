---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.17.1
kernelspec:
  display_name: named-let-saltino
  language: python
  name: python3
---

# Saltino

```{code-cell} ipython3
:tags: [remove-cell]

from railroad import *

RAILROAD_CSS = """
svg.railroad-diagram path {
  stroke-width:3;
  stroke:black;
  fill:rgba(0,0,0,0);
}
svg.railroad-diagram text {
  font:bold 14px monospace;
  font-family: "Fira Code";
  text-anchor:middle;
}
svg.railroad-diagram text.label{
  text-anchor:start;
}
svg.railroad-diagram text.comment{
  font:italic 12px monospace;
}
svg.railroad-diagram rect{
  stroke-width:3;
  stroke:black;
  fill:hsl(30,20%,95%);
}
svg.railroad-diagram rect.group-box {
  stroke: gray;
  stroke-dasharray: 10 5;
  fill: none;
}
"""

def show_diagram(d):
  result = []
  d.writeStandalone(result.append, css = RAILROAD_CSS)
  return '\n'.join(result)

Diagram._repr_svg_ = show_diagram
```

## Scopo del progetto

Scopo del progetto è implementare un **interprete** o **compilatore** per un
semplice linguaggio a carattere funzionale, denominato **Saltino**.

+++

```{warning}
Questa è la **versione @@** del progetto, pubblicata per consentire un  approfondimento preliminare degli aspetti legati all'ottimizzazione della ricorsione di coda e alla tecnica del trampolino.

Prima di iniziare lo sviluppo del progetto *attendente che venga pubblicata la  versione definitiva* e di esservi *accordati col docente* sugli aspetti legati al contenuto dell'insegnamento.
```

+++

## Il linguaggio Saltino

Saltino è un linguaggio funzionale molto semplice con alcune caratteristiche:

* i programmi sono una sequenza di definizioni di **funzioni** ciascuna delle
  quali è una sequenza di **istruzioni** che possono contenere **espressioni** o
  **condizioni**,
* l'unica struttura di controllo (oltre la *sequenza*) è la **selezione**, 
* è **fortemente tipizzato** in modo **dinamico**, i **tipi** del linguaggio
  sono: *interi*, *booleani*, *liste di interi* e *funzioni*.

Un esempio di programma è:

```python

def min2(x, y) {
  if x < y {
    return x
  } else {
    return y
  }
}

def main(a, b, c) {
  return min2(min2(a, b), c)
}
```

+++

### Sintassi

Questa sezione presenta formalmente la sintassi del linguaggio facendo uso dei
[diagrammi sintattici](https://en.wikipedia.org/wiki/Syntax_diagram) per non
influenzare la progettazione della grammatica formale.

Un **programma** è dato da una sequenza non vuota di definizioni di funzioni

```{code-cell} ipython3
:tags: [remove-input]

Diagram(OneOrMore(NonTerminal('funzione')))
```

Ciascuna **(definizione di) funzione** è data dal terminale `def` seguito
dall'identificatore che corrisponde al suo *nome*, seguito dall'elenco
(eventualmente vuoto) degli identificatori che corrispondono ai suoi *parametri
formali* racchiuso tra parentesi tonde e quindi da un blocco

```{code-cell} ipython3
:tags: [remove-input]

Diagram('def', 'ID', '(', ZeroOrMore('ID', ','), ')', NonTerminal('blocco'))
```

Le funzioni devono avere nomi distinti e deve esistere una funzione di nome
`main`; l'ordine in cui sono presenti le funzioni è irrilevante.

Un **identificatore** (denotato con `ID` nei diagrammi) è un *token* definito dall'*espressione regolare* `[_a-zA-Z][_a-zA-Z0-9]*`.

Un **blocco** è una sequenza, possibilmente vuota, di *istruzioni*, o *blocchi* annidati

```{code-cell} ipython3
:tags: [remove-input]

Diagram('{', ZeroOrMore(HorizontalChoice(NonTerminal('istruzione'), NonTerminal('blocco'))), '}')
```

Una **istruzione** è definita da una serie di alternative

```{code-cell} ipython3
:tags: [remove-input]

assignement_stm = Sequence('ID', '=', HorizontalChoice(NonTerminal('espressione'), NonTerminal('condizione')))
if_stm = Sequence('if', NonTerminal('condizione'), NonTerminal('blocco'), Optional(Sequence('else', NonTerminal('blocco'))))
return_stm = Sequence('return', HorizontalChoice(NonTerminal('espressione'), NonTerminal('condizione')))
Diagram(Choice(1, assignement_stm, if_stm, return_stm))
```

Le istruzioni sono costituite da *parole riservate* (`else`, `if`, `return`),
espressioni, condizioni e blocchi. Come si nota e sarà chiarito in seguito, il
linguaggio **non comprende istruzioni di iterazione**.

Una **espressione** (che come vedremo può valere un intero, una lista di interi
o una funzione) è

```{code-cell} ipython3
:tags: [remove-input]

expr = NonTerminal('espressione')
Diagram(Choice(1,
  Sequence(HorizontalChoice('+', '-'), expr),
  Sequence(expr, HorizontalChoice('+', '-', '*', '/', '%', '^', '::'), expr),
  HorizontalChoice('[]', 'INT', 'ID', NonTerminal('chiamata')),
  Sequence(Optional(HorizontalChoice('head', 'tail')), '(', expr, ')'),
))
```

La lista vuota `[]` rappresenta l'unico **letterale lista**, il **letterale
intero** (denotato con `INT` nei diagrammi) è un *token* costituito da uno o più
caratteri corrispondenti ad una cifra decimale. Nel contesto delle espressioni
gli identificatori rappresentano (come sarà chiarito in seguito), dei
*riferimenti a variabile*. I nomi riservati `head` e `tail` e l'operatore
binario `::` sono illustrati in seguito.

+++

Una **condizione** (a valore *booleano*) è

```{code-cell} ipython3
:tags: [remove-input]

cond = NonTerminal('condizione')
expr = NonTerminal('espressione')
Diagram(Choice(2,
  Sequence(expr, HorizontalChoice('<=', '<', '==', '>', '>='), expr),
  Sequence('!', cond),
  Sequence(cond, HorizontalChoice('and', 'or'), cond),
  HorizontalChoice('true', 'false'),
  Sequence('(', cond, ')'),
))
```

dove `true` e `false` sono gli unici **letterali booleani** (dall'ovvio significato).

La **chiamata** di funzione è

```{code-cell} ipython3
:tags: [remove-input]

expr = NonTerminal('espressione')
Diagram(expr, '(', ZeroOrMore(HorizontalChoice(expr, 'condizione'), ',' ), ')')
```

dove la prima espressione determina la funzione da chiamare e le espressioni, o
condizioni, costituiscono i *parametri concreti* della chiamata.

+++

#### Precedenza e associatività

I diagrammi sintattici non specificano la precedenza degli operatori, pertanto
per poter giungere alla formulazione di una grammatica *non ambigua* essa è
precisata come segue:

* le `(` e `)` hanno la precedenza su tutti gli operatori,
* `^` ha la precedenza su tutti gli operatori aritmetici e di lista, binari e
  unari,
* il `+` e `-` unari hanno precedenza su `+` e `-` binari,
* `*` e `/` e `%` hanno precedenza su `+` e `-` unari e binari e su `::`,
* gli operatori binari di comparazione hanno la precedenza su `and` e `or`,
* il `!` unario ha precedenza su `and` e `or`,
* l'`and` ha precedenza sull'`or`,
* `^` e `::` siano *associativi a destra*, mentre tutti gli altri operatori
  aritmetici binari siano *associativi a sinistra*, gli operatori binari di
  comparazione *non sono associativi*.

#### Le chiamate di funzione

Le chiamate meritano una nota a parte, dato Saltino è un linguaggio funzionale
possono esserci espressioni il cui valore è una funzione. Le chiamate hanno
precedenza più bassa rispetto agli altri operatori e sono associative a destra.
L'espressione `f(x, y)(z)` è pertanto da intendersi come la chiamata `g(z)` dove
`g` è la funzione restituita da `f(x, y)`.

#### Le liste

La struttura dati delle liste di interi possono essere definite e manipolate
in modo ricorsivo:

* la lista vuota `[]` è una lista,
* se `i` è una espressione intera e `l` una espressione lista, allora `i :: l` è
  una lista;
* `head(i::l)` vale `i` mentre `tail(i::l)` vale `l`.

L'associatività a destra dell'operatore `::` implica che `1 :: 2 :: 3 :: []` sia
equivalente a `1 :: (2 :: (3 :: []))`, che corrisponde alla lista avente 1, 2, 3 come
elementi.

#### Il controllo dei tipi

Sebbene Saltino non preveda la dichiarazione esplicita del tipo delle variabili
e dei parametri formali, fatto che impedisce un controllo statico dei tipi, è
fortemente tipizzato e i controlli sui tipi sono effettuati a tempo di
esecuzione:

* gli operatori aritmetici possono operare solo tra *interi*;
* l'operatore `::` può operare solo tra un *intero* e una *lista di interi*;
* gli operatori di confronto possono operare solo su *interi*, ad eccezione di
  `==` che può operare anche tra liste di interi, una delle quali deve però
  essere tassativamente il letterale `[]`;
* i connettivi logici possono operare solo tra valori *booleani*.

Ogni violazione di queste regole genera un errore a tempo d'esecuzione.

+++

### Semantica

Il comportamento di un programma in Saltino è definito in modo molto naturale a
partire dall'usuale semantica dei programmi imperativi e corrisponde in buona
sostanza al valore restituito dall'esecuzione della funzione `main` dato il
valore dei suoi parametri (che per semplicità assumeremo siano sempre interi).

In modo più formale, si può definire la **valutazione** in modo induttivo
secondo quanto stabilito dal resto di questa sezione.

La *valutazione* di una **espressione** o **condizione** consiste nel sostituire

* al posto delle variabili, l'ultimo valore che gli è stato assegnato
  *all'interno del blocco* e 
* al posto delle chiamate di funzione, la valutazione delle medesime;

si osservi che l'unico operatore di confronto che può essere usato tra liste è
`==`, solo nel caso in cui una delle due liste sia il letterale `[]`.

Le condizioni possono risultare vere, o false e pertanto il loro valore può
essere assegnato ad una variabile, o restituito dalla valutazione di una
chiamata di funzione. 

Si osservi che la **visibilità delle variabili è limitata al blocco** in cui
sono definite: una variabile definita in un blocco non è visibile al di fuori
del blocco, se un blocco contiene una variabile con lo stesso nome di una
variabile definita in un blocco esterno, la variabile del blocco interno
"nasconde" quella del blocco esterno.

La *valutazione* di una **chiamata** di funzione consiste nel

* valutare l'espressione che determina la funzione da chiamare,
* valutare le espressioni che compaiono tra parentesi nella sua chiamata,
* assegnare ai parametri formali le espressioni algebriche così ottenute,
* trasferire il controllo al *corpo* della funzione da chiamare, ossia al blocco
  di istruzioni che compaiono nella sua definizione, valutandone le istruzioni.

Il risultato della valutazione corrisponde al valore dell'espressione, o
condizione, riportata nella prima istruzione `return` incontrata durante
l'esecuzione (che si arresta dopo la valutazione dell'espressione); si osservi
che le funzioni *devono* terminare a causa di una istruzione `return`, se una
funzione raggiunge l'ultima istruzione senza aver incontrato un `return` deve
essere segnalato un errore. 

Si osservi che una funzione potrebbe contenere una chiamata a se stessa, ragion
per cui la sua *valutazione* darà luogo a una [pila di
chiamate](https://en.wikipedia.org/wiki/Call_stack?oldformat=true). 

La *valutazione* delle **istruzioni** dipende dall'istruzione nel caso di 

* un **assegnamento** corrisponde all'assegnare alla variabile il valore della
  valutazione dell'espressione o condizione;
* un **if-else** corrisponde a valutare l'espressione ed eseguire il primo
  blocco se vera, oppure il secondo blocco (se presente).

In conclusione, possiamo finalmente definire la *valutazione* di un
**programma** dato un numero di interi pari al numero dei suoi parametri formali
come la valutazione della funzione `main` su tali valori.

+++

## Iterazione e ricorsione

Nel contesto della teoria della computabilità (come avrete visto
nell'insegnamento di "Informatica teorica", o come potete trovare in classici
come "*Theory of Recursive Functions and Effective Computability*" di Hartley
Rogers, o "*Introduction to the Theory of Computation*" di Michael Sipser),
l'importanza della **ricorsione** emerge sin dalle fondamenta: la classe delle
*funzioni primitive ricorsive*, costruita tramite composizione e ricorsione
primitiva, rappresenta un insieme di funzioni *totali*. Tuttavia, per descrivere
tutte le funzioni calcolabili è necessario estendere questo linguaggio
introducendo l'operatore di *minimizzazione*
([μ-operator](https://en.wikipedia.org/wiki/%CE%9C_operator)), che consente di
definire funzioni *parziali*. Questo passaggio consente di raggiungere la piena
espressività delle [*funzioni ricorsive
parziali*](https://en.wikipedia.org/wiki/General_recursive_function), che come è
ben noto coincidono con quelle *calcolabili da una macchina di Turing*.

Molti linguaggi di programmazione funzionale adottano la ricorsione come
meccanismo primario per l'espressione di algoritmi iterativi, spesso escludendo
del tutto (come nel caso di Saltino), i costrutti iterativi espliciti (come
`while` o `for`). Questo approccio ha radici storiche profonde: dal [*lambda
calcolo*](https://en.wikipedia.org/wiki/Lambda_calculus) di Alonzo Church,
passando per linguaggi pionieristici come *LISP*, fino a sistemi didattici e
accademici come *Scheme* e *Haskell*, la ricorsione è diventata lo strumento
privilegiato per descrivere la ripetizione in ambienti che enfatizzano
l’immutabilità, la composizione funzionale e la semantica denotazionale.

L'iterazione può essere sempre facilmente sostituita dalla ricorsione, ad
esempio si consideri la funzione (in Python):

```python
def sum(lst) {
  tot = 0
  for i in lst: tot = tot + i
  return tot
}
```

che calcola la somma degli elementi di una lista di interi; essa può facilmente
essere tradotta in Saltino nella funzione ricorsiva:

```python
def sum(lst) {
  if lst == [] {
    return 0
  } else {
    return head(lst) + sum(tail(lst))
  }
} 
```

+++

### Ottimizzare la ricorsione

L’uso della ricorsione come meccanismo di iterazione è tipico nei linguaggi
funzionali, ma può comportare un costo elevato in termini di esecuzione, in
particolare per quanto riguarda l’utilizzo della pila delle chiamate. In
presenza di invocazioni ricorsive profonde, questa pila può crescere fino a
causare errori di *stack overflow*.

Tuttavia, esiste una classe particolare di ricorsione — detta **ricorsione di
coda** (tail recursion) — che consente **ottimizzazioni** significative. 

Il precedente esempio contiene una chiamata ricorsiva ma *non* di coda: dopo
aver calcolato `sum(tail(lst))` il blocco deve valutare la somma con `head(lst)`
prima di restituire il valore al chiamante. Non è difficile trasformare la
precedente funzione in una che abbia solo chiamate ricorsive di coda:

```python
def sum_tr(lst, acc) {
  if lst == [] {
    return acc
  } else {
    return sum_tr(tail(lst), head(lst) + acc)
  }
} 

def sum(lst) {
  return sum_tr(lst, 0)
}
```

Ora è possibile cercare di ottimizzare l'esecuzione del codice per evitare la
crescita della pila dei record di attivazione, questo può essere fatto evitando
di fatto la chiamata, ad esempio nei due modi seguenti.

#### Trasformazione iterativa

Se la chiamata è l'ultima valutazione, il blocco può essere sostituito da un
"ciclo infinito", che chiameremo `forever` in una ipotetica estensione di
Saltino (che potremmo chiamare Saltone). 

Questo consente di tradurre `sum` in versione iterativa come segue:

```python
def sum_tr(lst, acc) {
  forever {
    if lst == [] {
      return acc
    } else {
      lst = tail(lst)
      acc = head(lst) + acc
    }
  }
} 
```

In questa versione, invece di creare un nuovo record di attivazione e trasferire
nuovamente il controllo alla funzione stessa, vengono semplicemente assegnati ai
parametri formali le valutazioni delle corrispondenti espressioni e il controllo
torna all'inizio della funzione.

Attenzione però che `return` potrebbe non essere l'ultima istruzione del blocco,
per cui è necessaria anche una istruzione `continue` che passi all'iterato
successivo!

Ad esempio, la funzione seguente (che restituisce la somma dei primi `n` numeri
interi):

```python
def f(n, acc) {
  if n > 0 {
    return f(n - 1, acc + n)
  }
  return acc
} 
```

si traduce nella seguente versione iterativa: 

```python
def f(n, acc) {
  forever {
    if n > 0 {
      next_n = n - 1
      next_acc = acc + n
      n = next_n
      acc = next_acc
      continue
    }  
    return acc
  }
} 
```

Occorre fare attenzione anche agli effetti collaterali: assegnando diretamente
`x = x -1` la successiva espressione `acc = acc + x` utilizzerebbe il valore di
`x` già modificato. Per questa ragione è sempre più saggio calcolare il prossimo
valore del parametro formale `p` in `next_p` e, solo dopo aver calcolato i
valori di tutti i parametri, passare all'assegnamento `p = next_p`.

Si osservi che è sufficiente un "semplice" `continue` perché gli unici programmi
di Saltone a cui siamo interessati hanno un solo `forever` che racchiude tutto
il corpo della funzione e non ci sono mai altri `forever` annidati (altrimenti
sarebbe necessario un meccanismo di salto più esteso, per poter tornare
all'inizo della funzione in caso di chiamata ricorsiva di coda).

#### Trampolino

Una alternativa è costituita dall'uso di un **trampolino** che è una tecnica
grazie alla quale vengono eseguite in modo iterativo una serie di chiamate di
funzione ciascuna delle quali può restituire a sua volta una funzione, o un
altro tipo di valore.

Per essere implementata, tale tecnica richiede l'uso delle
[*chiusure*](https://en.wikipedia.org/wiki/Closure_(computer_programming)) o
delle [*funzioni anonime*](https://en.wikipedia.org/wiki/Anonymous_function),
che non sono previste in Saltino (e sarebbero complesse da realizzare in una sua
estensione). Per questa ragione, per illustrare l'uso della tecnica del
trampolino useremo Python, invece di procedere, come in precedenza, con una
trasformazione da Saltino a Saltone.

Per prima cosa, occorre definire la valutazione iterativa di un trampolino:

```{code-cell} ipython3
def valuta_trampolino(trampolino):
  while callable(trampolino):
    trampolino = trampolino()
  return trampolino
```

Il trampolino si ottiene a partire da una funzione ricorsiva di coda; come
esempio prendiamo quella per il calcolo del fattoriale:

```{code-cell} ipython3
def fattoriale_tr(n, acc):
  if n == 0:
    return acc
  return fattoriale_tr(n - 1, n * acc)

def fattoriale(n):
  return fattoriale_tr(n, 1)
```

Il trampolino sostituisce la chiamata ricorsiva nel `return`  con una chiusura
(senza argomenti) che verrà poi chiamata da `valuta_trampolino`:

```{code-cell} ipython3
def fattoriale_trampolino(n, acc):
  def next():
    return fattoriale_tr(n - 1, n * acc)
  if n == 0:
    return acc
  return next

def fattoriale(n):
  return valuta_trampolino(fattoriale_trampolino(n, 1))
```

## Dettagli progettuali e implementativi

Obiettivo del progetto è scrivere un interprete, o un compilatore, per Saltino.

Per svolgere il progetto sarà necessario:

1. Specificare una **grammatica** che determini quali programmi rappresentano
   codice sintatticamente valido in Saltino. Tale grammatica dovrà essere
   progettata in modo da rendere praticabile la ricostruzione della *struttura
   astratta* del programma.

2. Implementare un **parser** (e un eventuale ulteriore processo di
   raffinamento) in grado di ricostruire la suddetta struttura. 
   
3. Implementare un **interprete** (*ricorsivo* o *iterativo*, ma non un
   transpilatore) o un **compilatore** in grado di eseguire un programma in
   Saltino.

### Modulazione del progetto

Lo studente deve accordarsi con il docente prima dello svolgimento del progetto
per scegliere tra le diverse alternative presentate di seguito che consentono di
modulare la complessità del lavoro.

È possibile fare alcune scelte riguardo all'**implementazione**:

* Si può scegliere il linguaggio di programmazione tra: Python, Java e
  Javascript (o un eventuale altro), così come si può scegliere se usare
  `liblet`, o meno.
* Riguardo al punto 2 si può scegliere se implementare il parser in modo
  "diretto" o usare un generatore di parser (come ANTLR, o eventualmente un
  altro). In ogni caso, *la grammatica di cui al punto precedente andrà comunque
  scritta in modo esplicito*.
* Riguardo al punto 3. si può scegliere, nel caso del compilatore, quali
  strumenti di supporto adottare (come LLVM, o eventualmente un altro).

Riguardo alla ricorsione di coda e all'**ottimizzazione** è possibile:

+ non procedere con alcuna ottimizzazione,
+ procedere all'ottimizzazione con la traduzione in forma iterativa (in Saltone),
+ procedere all'ottimizzazione mediante la tecnica del trmapolino.

L'interprete/compilatore può incontrare diverse circostanze di **errore** in cui
non è possibile procedere:

* la stringa in ingresso contiene *token* inattesi;
* la stringa in ingresso non rispetta la *grammatica*;
* l'esecuzione incontra errori a tempo d'esecuzione, ad esempio:

    * nelle espressioni compaiono variabili non definite,
    * vengono invocate funzioni non definite, o che terminano senza `return`,
    * si presentano errori di *tipo* nelle espressioni, o condizioni.

È possibile scegliere come reagire a tali circostanze dalla soluzione più
elementare, che consiste nel catturare le eventuali eccezioni sollevate
nell'ambito del linguaggio in cui è scritto l'interprete/compilatore riportando
solo un messaggio d'arresto generico, fino a una gestione avanzata, in cui
ciascuna circostanza sia segnalata nel modo opportuno (eventualmente indicando
la posizione del testo sorgente che ha causato l'errore).

A seconda delle scelte, il docente suggerirà un probabile voto limite (se, ad
esempio, per ciascuna possibilità si sceglie l'alternativa più elementare è
difficile poter adire al massimo voto).

### Organizzazione del codice, documentazione e testing

Al fine di formulare la sua valutazione, il docente deve non solo accertare il
corretto funzionamento dell'interprete/compilatore, ma essere in grado di
comprendere il codice che lo realizza, con particolare riferimento alle scelte
progettuali, le strutture dati e la sua organizzazione.

Sebbene non sia richiesta una documentazione formale, si suggerisce di
realizzare il codice in modo modularizzato, provvedendo un minimo di commenti
(nel codice stesso) che ne chiariscano la struttura ed il comportamento.
Sopratutto nelle parti in cui è stata effettuata una scelta progettuale, o
adottata una soluzione non ovvia.

Il codice deve essere strutturato in modo tale che sia possibile eseguire
diversi programmi ciascuno su diversi input, raccogliendone in modo semplice
l'output. La valutazione sarà basata (tra l'altro) su una batteria di test che
sarà parzialmente messa a disposizione degli studenti prima della consegna della
versione finale del progetto.
