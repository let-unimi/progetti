---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Luppolo

```{code-cell} ipython3
:tags: [remove-cell]
from railroad import *

from liblet import side_by_side, Tree
from luppolo.expr import *
from luppolo.interp import interp

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

Obiettivo del progetto è costruire un sistema per [computer
algebra](https://en.wikipedia.org/wiki/Computer_algebra) primitivo basato su un
semplice [linguaggio di programmazione
imperativo](https://en.wikipedia.org/wiki/Imperative_programming) (denominato
**Luppolo**) in grado di manipolare [espressioni
algebriche](https://en.wikipedia.org/wiki/Algebraic_espressione), che
costituiscono di fatto l'unico [tipo di
dato](https://www.wikiwand.com/en/Data_type) del linguaggio.

Il seguito di questo documento descrive:

* il tipo di dato **espressione algebrica**,
* gli aspetti *sintattici* e *semantici* del linguaggio,
* le *specifiche progettuali e implementative* del progetto e una breve
  discussione sui *criteri di valutazione* del medesimo.

```{warning}
Questa è una **versione preliminare** del progetto, pubblicata per consentire un 
approfondimento preliminare degli aspetti legati alla manipolazione di espressioni.

Prima di iniziare lo sviluppo del progetto *attendente che venga pubblicata la 
versione definitiva* e di esservi *accordati col docente* sugli aspetti legati
al contenuto dell'insegnamento.
```

## Le espressioni algebriche

Per **espressione algebrica non semplificata** si intende un [*albero* $n$-ario
ordinato](https://en.wikipedia.org/wiki/Ordered_tree) i cui nodi sono definiti
induttivamente come segue, le **foglie** sono di due *tipi*

  * numeri **razionali** $q$ con $q\in \mathbf{Q}$, oppure 
  * **simboli** $x$ con $x\in\{\text{a}, \text{b}, \ldots, \text{z}\}$;

mentre i **nodi interni** sono di tre *tipi*

  * **addizioni** con figli $e_1, e_2, \ldots e_n$ denominati *addendi*,
  * **moltiplicazioni** con figli $e_1, e_2, \ldots e_n$ denominati *fattori*,
  * **potenze** con figli $e_1, e_2$ corrispondenti rispettivamente alla *base*
    ed *esponente* della potenza.

dove $e_1, e_2, \ldots e_n$ sono espressioni e $n > 1$.

Tra i nodi vige un **ordine totale** $\preceq$ definito a partire dall'ordine
tra i tipi di nodo (foglia, o interno) per cui 

$$
\text{addizioni} \preceq \text{simboli} \preceq \text{potenze} \preceq 
  \text{moltiplicazioni} \preceq \text{razionali}
$$

e tale che, a parità di tipo, viga l'ordine derivato da quello lessicografico
tra i figli dei due nodi. Si osservi che l'ordine influisce sull'ordine dei
figli dei nodi *addizione* e *moltiplicazione*, ma non sulle *potenze*. 

```{warning}
L'ordine potrebbe cambiare nella versione definitiva, pertanto è importante
che sia possibile modificare facilmente il codice per adattarsi a tale cambiamento.
```

Due espressioni sono **uguali** se e solo se i loro alberi sono identici,
tenendo anche conto dell'ordine dei nodi. 

Per **sotto-espressione** di una espressione si intende un suo sotto-albero
(compresa l'espressione stessa).

### Rappresentazione

Una *espressione* può avere diverse **rappresentazioni**. La più diretta è
quella data da un disegno dell'albero stesso:

```{code-cell} ipython3
:tags: [remove-input]
a = 'x * y + 1'
b = '2^(x-1)'
c = '3/4 * x * (y + k)'
side_by_side(
  visit_expr(a).tree(),
  visit_expr(b).tree(),
  visit_expr(c).tree()
)
```

Dall'albero è immediato costruire una rappresentazione **linearizzata** definita
induttivamente come segue:

* razionali e simboli sono rappresentati dal proprio valore;
* ogni nodo interno è rappresentato nella forma `O(E1, E2, ..., En)` dove `O` è
  il tipo del nodo e `E1, E2, ..., En` sono le rappresentazioni dei figli;

data la definizione induttiva, è immediato osservare che tale rappresentazione
si può ottenere semplicemente tramite una visita dell'albero dell'espressione
stessa.

Ad esempio, le espressioni precedenti possono essere rappresentate come

```{code-cell} ipython3
:tags: [remove-input]
print(visit_expr(a))
print(visit_expr(b))
print(visit_expr(c))
```

Una rappresentazione più suggestiva è quella usuale dell'algebra, che può essere
prodotta facendo uso di [LaTeX](https://www.latex-project.org/); ad esempio, le
espressioni precedenti possono essere rappresentate come

```{code-cell} ipython3
:tags: [remove-input]
display(
  visit_expr(a),
  visit_expr(b),
  visit_expr(c)
)
```
Si noti che in questa rappresentazione compaiono sia gli operatori binari $-$,
$/$ che le parentesi (solo laddove opportune) che non sono direttamente presenti
nell'albero. Ciò significa che questa rappresentazione è decisamente meno banale
da produrre di quella linearizzata!

### Semplificazione

Sebbene in questo progetto non si tratterà mai esplicitamente del *valore* di
una espressione, è necessario definire formalmente cosa si intenda con tale
termine per poter introdurre la definizione di espressioni *equivalenti*. 

Il **valore** di una espressione per un certo *assegnamento* di valori razionali
ai suoi simboli è (in modo molto naturale) definito induttivamente come segue

* i simboli hanno il valore assegnato,
* il valore dei nodi interni si ottiene interpretando le operazioni come
  usualmente si fa con i numeri razionali,
* il *valore* dell'espressione è il valore della radice.

Due espressioni sono **equivalenti** quando il loro valore è identico qualunque
sia l'assegnamento scelto. Ovviamente due espressioni uguali sono anche
equivalenti, ma non necessariamente vero il contrario.

A titolo di esempio, le due espressioni 

```{code-cell} ipython3
:tags: [remove-input]
side_by_side(
  Tree('Add', [Tree('x'), Tree('x')]),
  visit_expr('2*x').tree()
)
```

sono evidentemente diverse, ma altrettanto evidentemente equivalenti.

Per via del [teorema di
Richardson](https://en.wikipedia.org/wiki/Richardson's_theorem) in generale *non
è decidibile determinare se due espressioni siano equivalenti*, purtuttavia,
data una espressione non semplificata, è sempre possibile ottenere una
**espressione algebrica** ad essa equivalente, attraverso diverse manipolazioni
dell'albero, dette **semplificazioni**, che hanno in genere per obiettivo
ridurre il numero di nodi, definite induttivamente come segue.

* Ogni sotto-espressione le cui foglie sono tutte **razionali** può essere
  rimpiazzata con il razionale dato dal suo valore (nel senso ovvio del termine)
  ridotto ai minimi termini: ad esempio $x \cdot (1 + 4^{1/2})$ può essere
  semplificata in $3\cdot x$.

* Per i nodi **potenza**, se l'esponente è 0 il nodo può essere rimpiazzato con
  1, se viceversa è 1 con la base; similmente se la base è 0 può essere
  sostituito da 0 (qualunque sia l'esponente, se diverso dal razionale 0).

* I nodi **moltiplicazione** vengono semplificati attraverso varie
  trasformazioni: 

  * tutti i fattori che sono a loro volta moltiplicazioni sono sostituiti dai
    propri fattori: ad esempio $x \cdot (y^2 \cdot z)$ viene semplificato in $x
    \cdot z \cdot y^2$;
    
  * si raccolgono i fattori razionali in un unico fattore razionale (che può
    essere omesso se pari a 1, o che può ridurre a 0 tutta la moltiplicazione se
    vale 0): ad esempio $3 \cdot x^2 \cdot 2 \cdot y$ viene semplificato in $6
    \cdot y\cdot x^2$;

  * si raccolgono i fattori non razionali identici sostituendoli con la potenza
    data dalla somma dei loro esponenti: ad esempio $x^{-1} \cdot (1 + y^2)
    \cdot x^4 \cdot (1 +y^2)$ viene semplificato in $\left(1+ y^2\right)^2\cdot
    x^3$;

  * a questo punto, se restano due fattori di cui uno è razionale e l'altro è
    una somma, si distribuisce il prodotto su tutti i termini della somma: ad
    esempio $3 \cdot x \cdot (y + 1)$ viene semplificato in $(3 + 3\cdot y)\cdot
    x$. 
  
* I nodi **addizione** vengono analogamente semplificati attraverso altre
  trasformazioni: 

  * tutti i termini che sono a loro volta addizioni vengono sostituiti dai
    propri addendi: ad esempio $x + (y^2 + z)$ viene semplificato in $x + z +
    y^2$;

  * si raccolgono i termini razionali in un unico termine razionale (che può
    essere omesso se pari a 0): ad esempio $3 + x^2 + 2 + y$ viene semplificato
    in $5 + y + x^2$;
  
  * si raccolgono i termini non razionali identici (a meno di un fattore
    moltiplicativo razionale) sostituendoli con il prodotto dato dalla somma dei
    fattori moltiplicativi: ad esempio $3 \cdot x + (1 + y^2)^{-1} + 2 \cdot x +
    3 \cdot (1 +y^2)^{-1}$ viene semplificato in $4\cdot \left(1+
    y^{2}\right)^{-1}+ 5\cdot x$.

In Luppolo le espressioni algebriche saranno **sempre in forma semplificata**,
sia per ridurre il consumo di memoria, che perché in questo modo è più semplice
ragionare sulla loro manipolazione.

### Espansione

Esiste un'altra importante manipolazione dell'albero di una espressione basata
sulla *proprietà algebriche* di somme, prodotti e potenze.

Tale manipolazione prende il nome di **espansione** e si ottiene applicando le
seguenti trasformazioni definite induttivamente.

* I nodi **potenza** con *esponente* razionale $\frac p q$ vengono espansi come
  il prodotto della *base* per se stessa $|p|$ volte, elevato a $\frac {p/|p|}
  q$: ad esempio $(x+1)^{-3/2} = \left( (x+1)\cdot (x+1) \cdot (x+1)
  \right)^{-1/2}$; se l'esponente non è razionale, l'espansione si limita
  all'esponente: per esempio $(x+1)^{(x+1)\cdot x} = (x+1)^{x^2 + x}$.

* I nodi **moltiplicazione** sono espansi come prodotto (associativo a sinistra)
  dell'espansione dei propri fattori. L'espansione del prodotto di due fattori
  costituiti è ottenuto usando le *proprietà distributive* del prodotto e della
  somma: ad esempio $x \cdot (y + 2) \cdot (z + 3) = (x\cdot y + 2\cdot x)\cdot
  (z+3) = x\cdot y\cdot z+ 3\cdot x\cdot y+ 2\cdot x\cdot z+ 6\cdot x$
  
* I nodi **addizione** sono espansi come somma dell'espansione dei propri
  addendi.

 L'espansione è una operazione molto importante perché, in assenza di potenze
 con esponente non naturale, consente di trasformare una qualunque espressione
 in un [polinomio](https://en.wikipedia.org/wiki/Polynomial) (eventualmente
 multivariato, se sono presenti più simboli diversi tra loro).


### Sostituzione

L'ultima manipolazione dell'albero prende il nome di **sostituzione** e può
essere espressa a partire da tre espressioni: l'espressione $E$ a cui viene
applicata, l'espressione $M$ da sostituire e l'espressione $S$ con cui
sostituirla e può essere definita induttivamente come segue, a seconda che $E$
sia:

* una **foglia**, allora $E$ è rimpiazzata con $S$ se e solo se $E$ è uguale a
  $M$;
* un **nodo interno**, allora dapprima è effettuata la sostituzione di $M$ con
  $S$ in tutti i nodi figli di $E$, a questo punto tutti i figli di $E'$
  uguale a $M$ sono rimpiazzati d $S$.

Si ricorda che in Luppolo l'uguaglianza è data dall'identità tra alberi, non è
la più comune equivalenza tra espressioni.

Ad esempio, la sostituzione dell'espressione $x + 1$ con $y$ in $2 \cdot (x + 1)
\cdot a ^ {x+1}$ è

```{code-cell} ipython3
:tags: [remove-input]
visit_expr('2 * (x + 1) * a^(x+1)').subst(visit_expr('x + 1'), visit_expr('y'))
```

Si ricordi che le espressioni in Luppolo sono sempre semplificate, pertanto la
sostituzione di $x$ con $y$ in $x + 2 \cdot y$ è

```{code-cell} ipython3
:tags: [remove-input]
visit_expr('x + 2 * y').subst(visit_expr('x'), visit_expr('y'))
```


## Il linguaggio Luppolo

Il linguaggio Luppolo è un semplice *linguaggio imperativo* con gli usuali
costrutti di *selezione* ed *iterazione* in cui è possibile definire *variabili*
(aventi per *tipo* le espressioni algebriche come definite nella precedente
sezione) e *funzioni* (che restituiscono espressioni algebriche). 

Un esempio di programma in Luppolo è

```{code-cell} ipython3
:tags: [remove-input]
SOURCE = """
SquareTerms(Sum) {
  Result = 0
  foreach Term in Sum {
    Result = Result + Term ^ 2
  }
  return Result
}

Main(N) {
  Result = 1 + x
  repeat N {
    Result = Result + SquareTerms(Result)
  }
  return Expand(Result)
}
"""
print(SOURCE)
```

Se eseguito su input da 0 a 4 restituirà rispettivamente:

```{code-cell} ipython3
:tags: [remove-input]
for n in range(5):
  display(interp(SOURCE, n))
```

Di seguito viene presentata la sintassi del linguaggio e data una breve
presentazione della sua semantica.

### La sintassi

Questa sezione presenta formalmente la sintassi del linguaggio facendo uso dei
[diagrammi sintattici](https://en.wikipedia.org/wiki/Syntax_diagram) per non
influenzare la progettazione della grammatica formale.

Un **programma** in Luppolo è dato da una sequenza non vuota di funzioni

```{code-cell} ipython3
:tags: [remove-input]
Diagram(OneOrMore(NonTerminal("funzione")))
```

Ciascuna **funzione** è data dall'identificatore che corrisponde al suo *nome*,
seguito dall'elenco degli identificatori che corrispondono ai suoi *parametri
formali* e quindi da un blocco

```{code-cell} ipython3
:tags: [remove-input]
Diagram(NonTerminal("ID"), "(", ZeroOrMore(NonTerminal("ID"), ","), ")", NonTerminal("blocco"))
```

Le funzioni devono avere nomi distinti e deve esistere una funzione di nome
`Main`; l'ordine in cui sono presenti le funzioni è irrilevante.


Un **identificatore** (denotato con `ID` nei diagrammi) è un *token* costituito
da un carattere alfabetico maiuscolo seguito da zero o più caratteri alfabetici
(maiuscoli o minuscoli).

Un **blocco** è una sequenza, possibilmente vuota, di *istruzioni*

```{code-cell} ipython3
:tags: [remove-input]
Diagram("{", ZeroOrMore(NonTerminal("istruzione")), "}")
```

Una **istruzione** è definita da una serie di alternative 

```{code-cell} ipython3
:tags: [remove-input]
assignement_stm = Sequence(NonTerminal("ID"), "=", NonTerminal("espressione"))
if_stm = Sequence("if", NonTerminal("condizione"), NonTerminal("blocco"), Optional(Sequence("else", NonTerminal("blocco"))))
foreach_stm = Sequence("foreach", NonTerminal("ID"), "in", NonTerminal("espressione"), NonTerminal("blocco"))
repeat_stm = Sequence("repeat", NonTerminal("espressione"), NonTerminal("blocco"))
return_stm = Sequence("return", NonTerminal("espressione"))
while_stm = Sequence("while", NonTerminal("condizione"), NonTerminal("blocco"))
Diagram(Choice(2, assignement_stm, foreach_stm, if_stm, repeat_stm, return_stm, while_stm))
```

Le istruzioni sono costituite da *parole riservate* (`else`, `foreach`, `if`,
`in`, `repeat`, `return`, `while`), espressioni, condizioni e blocchi.

Una **espressione** (intesa come elemento lessicali del linguaggio) è

```{code-cell} ipython3
:tags: [remove-input]
expr = NonTerminal("espressione")
Diagram(Choice(0,
  Sequence(Choice(1, '+', '-'), expr),
  Sequence(expr, HorizontalChoice('+', '-', '*', '/', '^'), expr),
  HorizontalChoice(NonTerminal("NAT"), NonTerminal("SYM"), NonTerminal("ID"), NonTerminal('chiamata')),
  Sequence("(", expr, ")"),
))
```

Un **simbolo** (denotato con `SYM` nei diagrammi) è un *token* costituito da un
singolo carattere alfabetico minuscolo, un **naturale** (denotato con `NAT` nei
diagrammi) è un *token* costituito da uno o più caratteri corrispondenti ad una
cifra decimale. Ne contesto delle espressioni gli identificatori rappresentano
(come sarà chiarito in seguito), dei *riferimenti a variabile*. 

Una **condizione** (a valore *booleano*) è

```{code-cell} ipython3
:tags: [remove-input]
cond = NonTerminal("condizione")
expr = NonTerminal("espressione")
Diagram(Choice(0,
  Sequence(expr, HorizontalChoice('<=', '<', '==', '>', '>='), expr),
  Sequence("!", cond),
  Sequence(cond, HorizontalChoice('and', 'or'), cond),
  HorizontalChoice('true', 'false'),
  Sequence("(", cond, ")"),
))
```
La **chiamata** di funzione è

```{code-cell} ipython3
:tags: [remove-input]
Diagram(NonTerminal("ID"), "(", ZeroOrMore(NonTerminal("espressione"), "," ), ")")
```

dove l'identificatore sta per il *nome* della funzione e le espressioni
costituiscono i *parametri concreti* della chiamata.

#### Una nota sulle espressioni e condizioni

Le *espressioni intese come elemento lessicale* del linguaggio Luppolo **non
coincidono** con le *espressioni algebriche* definite nella sezione precedente;
ad esempio, in Luppolo sono presenti la divisione, il meno unario e le parentesi
che non corrispondono *direttamente* ad alcun nodo di una espressione algebrica.
Inoltre i diagrammi sintattici sono fortemente *ambigui* (nello stesso senso che
si attribuisce al termine nel contesto delle grammatiche formali), 

Purtuttavia, è possibile ricavare una grammatica libera da contesto non ambigua
tale per cui ad ogni *espressione di Luppolo* si può associare un unico albero
di parsing dal quale è semplice ottenere in modo non ambiguo una sola
*espressione algebrica semplificata* a patto che:

* le `(` e `)` abbiano la precedenza su tutti gli operatori,
* `^` abbia la precedenza su tutti gli operatori binari e unari,
* `*` e `/` abbiano precedenza su `+` e `-` unari e binari,
* l'`and` abbia precedenza sull'`or`,
* il `+` e `-` unari hanno precedenza su `+` e `-` binari,
* é il `!` unario abbia precedenza su `and` e `or`,
* `^` sia associativo a destra, mentre tutti gli altri operatori binari siano
  associativi a sinistra.

La traduzione dall'albero di parsing alla corrispondente espressione algebrica
semplificata è possibile a patto di convertire $-x$ (il `-` unario) in $-1 \cdot
x$ (ossia, una moltiplicazione per $-1$) e $x / y$ (il `/` binario) in $x \cdot
y^{-1}$ (ossia, una moltiplicazione per la potenza di base $y$ e esponente
$-1$).

### La semantica

Il comportamento di un programma in Luppolo è definito in modo molto naturale a
partire dall'usuale semantica dei programmi imperativi e corrisponde in buona
sostanza al valore restituito dall'esecuzione della funzione `Main` dato il
valore dei suoi parametri.

In modo più formale, si può definire la **valutazione** in modo induttivo
secondo quanto stabilito dal resto di questa sezione.

La *valutazione* di una **espressioni** consiste nel sostituire

* al posto delle variabili, l'ultima espressione che gli è stata assegnata e 
* al posto delle chiamate di funzione, la valutazione delle medesime;

queste sostituzioni, dopo opportune semplificazioni, produrranno una espressione
algebrica. Se in una espressione (intesa come elemento lessicale) compaiono
variabili o funzioni non definite, deve essere segnalato uno specifico errore.

La *valutazione* di una **condizione** consiste nel valutare

* le espressioni algebriche,
* gli operatori di confronto tra espressioni algebriche (dove l'ordine e
  l'uguaglianza sono quelle definite per le espressioni algebriche),
* gli operatori e le costanti logiche (nel modo ovvio);

le condizioni possono pertanto risultare vere, o false, ma si ricorda che tali
valori non sono tipi del linguaggio (pertanto, ad esempio, non possono essere
assegnati ad una variabile, o restituiti dalla valutazione di una chiamata di
funzione).

La *valutazione* di una **chiamata** di funzione consiste nel

* valutare le espressioni che compaiono tra parentesi nella sua chiamata,
* assegnare ai parametri formali le espressioni algebriche così ottenute,
* trasferire il controllo al *corpo* della funzione, ossia al blocco di
  istruzioni che compaiono nella sua definizione, valutandone le istruzioni.

Il risultato della valutazione corrisponde al valore dell'espressione riportata
nella prima istruzione `return` incontrata durante l'esecuzione (che si arresta
dopo la valutazione dell'espressione); si osservi che le funzioni *devono*
terminare a causa di una istruzione `return`, se una funzione raggiunge l'ultima
istruzione senza aver incontrato un `return` deve essere segnalato un errore. 

Si osservi che una funzione potrebbe contenere una chiamata a se stessa, ragion
per cui la sua *valutazione* darà luogo a una [pila di
chiamate](https://en.wikipedia.org/wiki/Call_stack?oldformat=true). 

La *valutazione* delle **istruzioni** dipende dall'istruzione nel caso di 

* un **assegnamento** corrisponde all'assegnare alla variabile il valore della
  valutazione dell'espressione;
* un **foreach** corrisponde a valutare l'espressione ed eseguire un iterato del
  ciclo per ciascun figlio dell'nodo radice dell'espressione, assegnando alla
  variabile di ciclo la sotto-espressione corrispondente;
* un **if-else** corrisponde a valutare l'espressione ed eseguire il primo
  blocco se vera, oppure il secondo blocco (se presente);
* un **repeat** corrisponde a valutare l'espressione e, qualora il risultato sia
  un numero naturale, eseguire il blocco tante volte quante indicate dal numero
  naturale (o segnalare un errore nel casco in cui la valutazione
  dell'espressione non conduca ad un numero naturale);
* un **while** corrisponde a valutare la condizione, se essa è vera
  nell'eseguire il blocco e tornare a valutare l'espressione;

si noti che nel caso del `repeat` la valutazione avviene solo all'inizio
dell'iterazione, mentre nel caso del `while` l'espressione va valutata
all'inizio di ogni iterato (perché potrebbe, ad esempio, contenere una
variabile, o chiamata, il cui valore cambia durante il ciclo).

In conclusione, possiamo finalmente definire la *valutazione* di un
**programma** dato un numero di espressioni pari al numero dei suoi parametri
formali come la valutazione della funzione `Main` su tali espressioni.

### Funzioni di libreria

Il linguaggio Luppolo prevede alcune funzioni di libreria che possono essere
invocate anche se non sono state definite esplicitamente. Tali funzioni sono:

* `Expand(expr)`, che restituisce l'espressione algebrica ottenuta
  dall'espansione di quella passata come argomento;
* `Substitute(expr, match, subst)`, che restituisce l'espressione algebrica
  ottenuta sostituendo tutte le sue sotto-espressioni uguali a `match` con
  l'espressione algebrica `subst`.
* `Eval(expr, rat)`, che restituisce l'espressione algebrica ottenuta dalla
  valutazione dell'espressione algebrica passata come primo argomento
  sostituendo il suo unico simbolo con il numero razionale dato dall'espressione
  algebrica passata come secondo argomento; se la seconda espressione algebrica
  non è un numero razionale, o se nella prima espressione compare più di un
  simbolo, la funzione emette un errore;
* `SimpleDerive(expr, sym)`, che restituisce l'espressione algebrica ottenuta
  dalla [derivata](https://en.wikipedia.org/wiki/Derivative) dell'espressione
  algebrica passata come primo argomento rispetto al simbolo specificato
  dall'espressione algebrica passata come secondo argomento; se la prima
  espressione algebrica contiene potenze con esponente non razionale, o se la
  seconda espressione algebrica non è un simbolo, la funzione emette un errore;
* `DerivePolynomial(poly, symbol)`, che restituisce l'espressione algebrica
  ottenuta dalla derivata del polinomio equivalente all'espressione algebrica
  passata come primo argomento rispetto al simbolo specificato dall'espressione
  algebrica passata come secondo argomento; se la seconda espressione algebrica
  non è un simbolo, o se la prima (una volta espansa) non è un [polinomio
  univariato](https://en.wikipedia.org/wiki/Polynomial) in tale simbolo, la
  funzione emette un errore.

Si osservi che sebbene `DerivePolynomial` possa banalmente essere ottenuta da
`SimpleDerive` potrebbe risultare più semplice implementarla direttamente (ad
esempio, nel caso in cui si decidesse di non implementare `SimpleDerive`).

#### Input e output

Secondo le specifiche date sin qui, un programma in Luppolo riceve "input" solo
 attraverso i parametri formali della funzione `Main` e produce "output" solo
 attraverso l'istruzione `return` della stessa funzione.

Se lo si ritiene utile, è possibile aggiungere delle *funzioni di libreria* per
consentire la gestione di forme più "tradizionali" di *input* e *output*.

#### Ripasso delle derivate

Ai fini del progetto, è possibile pensare alle *derivate* come ad una semplice
manipolazione formale dell'espressione (prescindendo dal loro significato
analitico ) secondo le usuali [regole di
derivazione](https://en.wikipedia.org/wiki/Differentiation_rules) che sono di
seguito richiamate per i casi inerenti al progetto.

La derivata dei razionali è $0$, quella dei simboli è $1$, nel caso delle
potenze con esponente razionale $q\in \mathbf{Q}$ vale

$$
\frac{d}{dx} f(x)^q = q\cdot f(x)^{q-1} \cdot \frac{d}{dx} f(x)
$$


mentre per le somme vale che

$$
\frac{d}{dx} \left[\sum_{i=1}^n f_i(x)\right] = 
\sum_{i=1}^n \frac{d}{dx} f_i(x)
$$

e per i prodotti

$$
\frac{d}{dx} \left[\prod_{i=1}^n f_i(x)\right] = 
\sum_{i=1}^n \left(\left(\frac{d}{dx} f_i(x)\right) \prod_{j=1, j\neq i}^n f_j(x)\right)
$$


## Dettagli progettuali e implementativi

Obiettivo del progetto è scrivere un interprete o un compilatore per Luppolo.

Per svolgere il progetto sarà necessario:

1. Specificare una **grammatica** che determini quali programmi rappresentano
   codice sintatticamente valido in Luppolo. Tale grammatica dovrà essere
   progettata in modo da rendere praticabile la ricostruzione della *struttura
   astratta* del programma.

2. Implementare un **parser** (e un eventuale ulteriore processo di
   raffinamento) in grado di ricostruire la suddetta struttura. 
   
3. Implementare un **interprete** (*ricorsivo* o *iterativo*, ma non un
   transpilatore) o un **compilatore** in grado di eseguire un programma in
   Luppolo.

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
  altro). In ogni caso, andrà comunque scritta in modo esplicito la grammatica
  di cui al punto precedente.
* Riguardo al punto 3. si può scegliere, nel caso del compilatore, quali
  strumenti di supporto adottare (come LLVM, o eventualmente un altro).

Rispetto all'insieme di **funzionalità** del linguaggio, si può scegliere di
implementare un numero ristretto (o nessuna) tra le funzioni di libreria.

L'interprete/compilatore può incontrare diverse circostanze di **errore** in cui
non è possibile procedere:

* la stringa in ingresso contiene *token* inattesi;
* la stringa in ingresso non rispetta la *grammatica*;
* l'esecuzione incontra errori a tempo d'esecuzione, ad esempio:

    * nelle espressioni compaiono variabili non definite,
    * vengono invocate funzioni non definite, o che terminano senza `return`,
    * la valutazione dell'espressione in una istruzione `repeat` non è un
      naturale.

e tante altre. È possibile scegliere come reagire a tali circostanze dalla
soluzione più elementare, che consiste nel catturare le eventuali eccezioni
sollevate nell'ambito del linguaggio in cui è scritto l'interprete/compilatore
riportando solo un messaggio d'arresto generico, fino a una gestione avanzata,
in cui ciascuna circostanza sia segnalata nel modo opportuno (eventualmente
indicando la posizione del testo sorgente che ha causato l'errore).

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
