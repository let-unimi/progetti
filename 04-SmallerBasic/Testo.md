# Smaller Basic

**Questa è una versione preliminare, potrebbe subire piccoli cambiamenti; 
la versione definitiva sarà stabilita entro la fine del corso.**

Scopo del progetto è implementare un semplice *interprete* o *compilatore* per
una versione semplificata del linguaggio **Small Basic** di **Microsoft** che
chiameremo "Smaller Basic".

Con il termine **Basic** (acronimo per "Beginners' All-purpose Symbolic
Instruction Code") usualmente si denota una [famiglia di linguaggi di
programmazione](https://en.wikipedia.org/wiki/BASIC) general-purpose ad alto
livello, caratterizzati da notevole semplicità d'uso; il primo esempio di
linguaggi di tale famiglia è stato introdotto da John G. Kemeny e Thomas E.
Kurtz, presso il Dartmouth College nel 1963.

Per gli scopi del corrente progetto faremo riferimento ad un esempio più
recente, denominato "Small Basic", prodotto da Microsoft e descritto nel
documento [The Developer's Reference Guide to Small Basic](https://social.technet.microsoft.com/wiki/contents/articles/16767.the-developers-reference-guide-to-small-basic.aspx).

Di seguito, nella sezione "Il linguaggio", sarà data una descrizione accurata
del linguaggio da implementare e, nella sezione "Modulazione del progetto",
saranno descritte in dettaglio le specifiche del progetto.

# Il linguaggio

Per una prima introduzione alla sintassi e semantica di "Small Basic", nonché
per qualche esempio di programma potete far riferimento alla documentazione
Microsoft.

Le sezioni che seguono definiscono in modo più formale la struttura lessicale e
grammaticale del linguaggio "Smaller Basic".


## Struttura lessicale

Un programma "Smaller Basic" è una stringa ASCII, i *token* sono sequenze
massimali di caratteri separata da *white-space* (orizzontale e verticale) che
non è altrimenti significativo.

Gli **identificatori** sono sequenze di al più 40 caratteri a scelta tra quelli
alfabetici, numerici e il carattere *underscore* (`_`) che non iniziano per
numero, escluse le **parole riservate** che saranno elencate nella sezione sul
"Controllo del flusso". Ci sono diversi tipi di **costanti letterali** che
saranno descritte nella sezione sui "Tipi di dato", così come vari **operatori**
e simboli che saranno descritti nella sezione sulle "Espressioni". Sono inoltre
token il punto `.` e le parentesi quadre `[` e `]`.

## Espressioni e Istruzioni

### Variabili e visibilità

Le variabili sono denotate dagli *identificatori* e hanno **visibilità
globale**. 

Non esiste una nozione di "dichiarazione" di variabile: le variabili vengo
dichiarate e definite allo stesso tempo la prima volta in cui viene loro
assegnato un valore; questo vale anche per gli *array* (introdotti di seguito),
per cui ad esempio l'espressione `a[3][4][5] = 6` corrisponde alla dichiarazione
implicita del fatto che `a` è un array tridimensionale (e che la sua prima
dimensione ha taglia almeno 4, la seconda almeno 5 e la terza almeno 6).

L'**assegnamento** tra variabili avviene per copia (sia per i tipi primitivi che
derivati); le variabili possono contenere valori di tipo diverso (in momenti
diversi dell'esecuzione).

### Tipi di dato

#### Primitivi

I tipi di dato primitivi sono **numeri**, **stringhe** e **booleani**. 

I numeri possono essere interi o reali; le costanti letterali numeriche
appartengono al linguaggio definito dall'espressione regolare Python
`[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?`.

Le stringhe sono sequenze di caratteri appartenenti al segmento "stampabile"
della codifica ASCII (ossia con codifica da 32 a 126, estremi compresi, ma
escluso il 22); le costanti letterali stringa sono date alla sequenze di
caratteri della stringa racchiusi tra `"`. Non sono previsti caratteri di
*escape* per tanto, ad esempio, la stringa "\n" corrisponde ai due caratteri "\"
e "n".

I booleani possono avere valore *vero* (corrispondente al letterale `"true"`) o
*falso* (corrispondente al letterale `"false"`).

#### Derivati

L'unico tipo derivato è l'**array**, dato un tipo primitivo o derivato `T`, un
**array** è un elenco numerato (a partire da 0) di elementi di tipo omogeneo
`T`; questo significa tra l'altro che si possono avere array di array, o array
"bidimensionali" (o in genere n-dimensionali). 

Una espressione con valore intero $i$ racchiusa tra parentesi quadre `[`, `]`
dopo un array ne denota l'$i$-esimo elemento.

Ad esempio, se `v` è un array di "righe" ciascuna delle quali è un array di
"colonne", l'espressione `v[r][c]` denota l'elemento nella colonna (di posto)
`c` della riga (di posto) `r`. 

Non è consentito indicizzare un array $n$-dimensionale di tipo `T` con meno di
$n$ espressioni, detto altrimenti se `v` è un array $n$-dimensionale esso può
comparire in una espressione (o assegnamento) come `v`, da intendersi di tipo
array $n$-dimensionale, oppure come `v[e1][e2]…[en]` (dove `e1`, …, `en` sono
$n$ espressioni a valore intero), da intendersi di tipo `T`.

### Espressioni

Le espressioni sono costituite da una serie di *atomi* che sono *costanti
letterali*, *variabili* e *invocazioni* di *funzioni di libreria* (illustrate
più avanti), o da espressioni combinate tra loro tramite opportuni
**operatori**.

Le **espressioni aritmetiche** combinano tra loro espressioni di tipo numerico
producendo una espressione di tipo numerico tramite gli operatori aritmetici
`*`, `/`, `+` e `-` (anche unario), che sono da intendere secondo l'usuale
semantica, precedenza e associatività.

Le **espressioni stringa** combinano tra loro espressioni di tipo stringa
producendo una espressione di tipo stringa tramite l'operatore `+` di
concatenazione.

Le **espressioni relazionali** combinano tra loro espressioni di tipo omogeneo,
numerico o stringa, producendo una espressione di tipo booleano tramite gli
operatori `<`, `<=`, `=`, `<>`, `>`, `>=` che sono da intendere secondo l'usuale
semantica. Gli operatori relazionali hanno precedenza più bassa rispetto a
quelli aritmetici.

Le **espressioni logiche** combinano tra loro espressioni di tipo booleano
restituendo una espressione di tipo booleano tramite gli operatori `And` e `Or`
che sono da intendere secondo l'usuale semantica. Gli operatori logici hanno
precedenza più bassa rispetto a quelli relazionali.

In ogni genere di espressioni, le parentesi `(` e `)` possono essere usate per
alterare la precedenza e l'associatività sopra definite.

Ad esempio, secondo le regole di precedenza e l'associatività stabilite in
questa sezione, l'espressione 

```
1 + 2 * 3 < 5 Or a = 1 + b + 2
```

è equivalente a

```
((1 + (2 * 3) < 5) Or (a = ((1 + b) + 2)).
```

### Istruzioni

Le possibili **istruzioni** di un programma sono:

* assegnamenti,
* etichette,
* istruzioni di controllo del flusso,
* invocazioni di subroutine,
* invocazioni di funzioni del modulo di libreria `IO`.

L'**assegnamento** corrisponde ad una istruzione della forma `V = E` dove `V` è
un qualunque identificatore e `E` una qualunque espressione.

Una **etichetta** è un identificatore seguito da `:`, ciascun identificatore può
essere usato una sola volta all'interno del programma.

Le *subroutine* o *funzioni di libreria* saranno introdotte nelle sezioni
seguenti, una **invocazione** di una subroutine, o funzione, è data dal suo nome
seguito da una coppia di `(` `)` (tra le quali, nel caso di funzioni, potrebbe
trovarsi un elenco di espressioni).

Le istruzioni di controllo del flusso sono descritte di seguito.

#### Sequenza

Una **sequenza** di istruzioni è data da zero o più istruzioni elencate una di
seguito all'altra; tali istruzioni sono eseguite in sequenza una dopo l'altra
nell'ordine in cui compaiono, fatto salvo il caso dei *salti incondizionati*
(illustrati nell'ultima parte di questa sezione).

#### Selezione

La **selezione** è realizzata tramite le istruzioni 

```If (C) Then … EndIf``` 

o 

```If (C) Then … Else … EndIf``` 

in ciascuna delle quali `C` è una qualunque espressione booleana e `…` una
qualunqu sequenza di istruzioni.

#### Iterazione

L'**iterazione** è realizzata attraverso:

* cicli con un numero di iterati non noto a priori, tramite l'istruzione
  
  ```While (C) … EndWhile``` 
  
  in cui `C` è una qualunque espressione booleana e `…` una qualunque sequenza
  di istruzioni, 

* cicli con un numero di iterati prestabiliti, tramite le istruzioni 

  ```For V = F To T … EndFor```
  
  o 
  
  ```For V = F To T Step S … EndFor``` 
  
  in cui `V` è una variabile, `F`, `T` e `S` (se presente) sono una qualunque
  espressione aritmetica (in cui non compare `V`) e `…` una qualunque sequenza
  di istruzioni che non comprenda assegnamenti alla variabile `V`.

La semantica dei cicli è quella usuale; in particolare, nel caso del numero
prestabilito di iterati, le espressioni possono avere valore sia intero che
reale, la variabile sarà inizializzata al valore di `S` e ad ogni `EndFor` sarà
incrementata del valore pari a `S` (valutato una sola volta all'inizio del
ciclo) e il ciclo proseguirà finché la variabile ha valore minore o uguale a
`T`.

#### Salti incondizionati

Il linguaggio BASIC contiene l'istruzione di salto incondizionato `Goto` che è
stata storicamente abbandonata per varie [buone
ragioni](https://homepages.cwi.nl/~storm/teaching/reader/Dijkstra68.pdf).

Se l'istruzione di una sequenza è un `Goto` l'esecuzione della sequenza (e di
tutti i cicli annidati, o subroutine in cui essa si trova) termina
immediatamente e l'esecuzione prosegue dal punto del codice identificato
dall'etichetta avente lo stesso nome di quella che segue l'istruzione `Goto`che
ha prodotto il salto.

Ad esempio, nel codice

```
For A = 1 To 10
  For B = 1 To 10
    A = 3 * 4
    Goto fine
  EndFor
EndFor
B = 1 + 2
fine:
C = 4
```

la sequenza di esecuzione è data dall'assegnamento ad `A` (eseguito una sola
volta) e poi a `C`.

Ragionare sulla semantica del codice in presenza di salti incondizionati è
affatto non banale, per questa ragione prestate molta attenzione a come
intendete realizzarla e ai test offerti dal docente per valutare la vostra
implementazione.

### Subroutine

È possibile *definire* delle **subroutine** come 

```Sub N … EndSub``` 

dove `N` è un qualunque identificatore (non ancora utilizzato nella definizione
di subroutine) e `…` una qualunque sequenza (eventualmente vuota) di istruzioni.

La visibilità delle variabili resta globale anche nel caso delle subroutine, per
questa ragione in una subroutine è possibile accedere a tutte le variabili
definite in qualunque altro punto del programma e viceversa. 

L'invocazione di una subroutine produce il trasferimento dell'esecuzione alla
prima istruzione della subroutine, dalla quale l'esecuzione procederà fino al
raggiungimento dell'istruzione `EndSub` dopo la quale riprenderà da quella
successiva all'invocazione della subroutine.


### Funzioni di libreria

Le funzioni di libreria sono raccolte in *moduli* il cui nome è un qualunque
identificatore valido e hanno per nome un qualunque identificatore valido, il
nome del modulo è separato con un `.` dal nome della funzione; possono essere
invocate sia come istruzioni che nelle espressioni (se restituiscono un valore).

#### Input / Output

Per consentire al programma di ricevere **input** e di produrre **output** sono
previste due funzioni di libreria:

* `IO.ReadLine()`, che non ha argomenti e restituisce una riga letta dal *flusso
  di ingresso standard*; se la riga contiene solo un valore che può essere
  convertito ad un valore numerico, la conversione avviene automaticamente,
  viceversa viene restituita una stringa;

* `IO.WriteLine()` che ha un solo argomento, di qualunque tipo, che emetterà nel
  *flusso di uscita standard* (seguito da *a-capo*).
  
#### Matematica e altro

Al fine di consentire l'esecuzione di programmi con comportamenti non del tutto
banali è consigliabile dotare l'ambiente di esecuzione di alcune funzioni:

* una serie di funzioni "matematiche" di nome `Math.X` dove `X` sia il nome di
  alcune funzioni a valore numerico, come ad esempio `Math.Sin`, `Math.Cos`,
  `Math.Sqrt` e così via;
* alcune funzioni per la "randomizzazione", come ad esempio
  `Random.GetRandomNumber`;
* alcune funzioni per la manipolazione delle stringhe, come ad esempio
  `String.Length`, `String.ToUpper`, o `String.Split`.

Non c'è particolare vincolo sul numero e sul comportamento di tali funzioni; è
però necessario che la grammatica e il compilatore/interprete siano realizzati
in modo da consentire, alla bisogna, di aggiungere in modo conveniente altre
funzioni.

## Differenze con Small Basic

Il linguaggio qui descritto è molto semplificato (e più formalmente specificato)
rispetto a quanto illustrato nel  nel documento [The Developer's Reference Guide
to Small Basic](https://social.technet.microsoft.com/wiki/contents/articles/16767.the-developers-reference-guide-to-small-basic.aspx).

In particolare non è stata considerata tutta la parte riguardante gli
**oggetti** (con *metodi* ed *eventi*) e conseguentemente non è richiesta
l'implementazione degli oggetti `Program`, `TextWindow` e `GraphicWindow` per la
realizzazione di *user interface*

# Dettagli progettuali e implementativi

Obiettivo del progetto è scrivere un interprete o un compilatore per il
linguaggio "Smaller Basic".

Per svolgere il progetto sarà necessario:

1. Specificare una **grammatica** che determini quali programmi rappresentano
   codice sintatticamente valido in "Smaller Basic". Tale grammatica dovrà
   essere progettata in modo da rendere praticabile la ricostruzione della
   *struttura astratta* del programma.

2. Implementare un **parser** (e un eventuale ulteriore processo di
   raffinamento) in grado di ricostruire la suddetta struttura.
   
3. Implementare un **interprete** (*ricorsivo*, o *iterativo*, ma non un
   transpilatore) o un **compilatore** in grado di eseguire un programma in
   "Smaller Basic"; in questa fase può essere opportuno, tra l'altro,
   raccogliere informazioni sui tipi delle espressioni.

## Modulazione del progetto

Lo studente deve accordarsi con il docente prima dello svolgimento del progetto
per scegliere tra le diverse alternative presentate di seguito che consentono di
modulare la complessità del lavoro.

È possibile fare alcune scelte riguardo all'**implementazione**:

* Si può scegliere il linguaggio di programmazione tra: Python, Java e
  Javascript (o un eventuale altro, da concordare col docente), così come si può
  scegliere se usare `liblet`, o meno.
* Riguardo a "Smaller Basic" si può scegliere se trattare, o meno, i salti
  incondizionati (`Goto` e etichette); così come si può scegliere se trattare, o
  meno, il caso degli array multidimensionali.
* Riguardo al punto 1. si raccomanda di non utilizzare in modo acritico una
  delle grammatiche per il linguaggio Basic tra quelle disponibili per ANTLR
  perché potrebbero contenere difetti (magari nascosti) che le rendono inadatte
  a rappresentare programmi in "Smaller Basic".
* Riguardo al punto 2. , si può scegliere se implementare il parser in modo
  "diretto" o usare un generatore di parser (come ANTLR, o eventualmente un
  altro, da concordare col docente).
* Riguardo al punto 3. si può scegliere, nel caso del compilatore, quali
  strumenti di supporto adottare (come LLVM, o eventualmente un altro, da
  concordare col docente).

L'interprete/compilatore può incontrare diverse circostanze di **errore** in cui
non è possibile procedere:

* la stringa in ingresso contiene *token* inattesi;
* la stringa in ingresso non rispetta la *grammatica*;
* l'esecuzione incontra errori a tempo d'esecuzione, ad esempio:

    * nelle espressioni compaiono variabili non definite,
    * vengono invocate funzioni non esistenti,
    * nei `Goto` compaiono etichette non definite,
    * vengono ridefinite etichette, o subroutine,
    * non sono rispettati i tipi (per gli operatori, o le invocazioni di
      funzione).

e tante altre. È possibile scegliere come reagire a tali circostanze dalla
soluzione più elementare, che consiste nel catturare le eventuali eccezioni
sollevate nell'ambito del linguaggio in cui è scritto l'interprete/compilatore
riportando solo un messaggio d'arresto generico, fino a una gestione avanzata,
in cui ciascuna circostanza sia segnalata nel modo opportuno (eventualmente
indicando la posizione del testo sorgente che ha causato l'errore).

A seconda delle scelte, il docente suggerirà un probabile voto limite (se, ad
esempio, per ciascuna possibilità si sceglie l'alternativa più elementare è
difficile poter adire al massimo voto).

### L'istruzione `Goto`

La realizzazione dei salti incondizionati determinati dall'istruzione `Goto` può
richiedere uno sforzo aggiuntivo nel caso si scelga di implementare un
interprete *ricorsivo*: salti non condizionali ricorsione non convivono
facilmente! Molto più semplice è il caso di un interprete *iterativo* o di un
compilatore (in cui la nozione di *program counter* può agevolare immensamente
l'implementazione dei salti incondizionati).

Chi volesse tentare la strada dell'interprete *ricorsivo* può usare questa
strategia: 

* quando l'interprete incontra un `Goto` solleva una eccezione e interrompe la
  visita "normale" tenendo traccia dell'etichetta dalla quale dovrà proseguire
  l'esecuzione;
  
* l'eccezione è gestita riprendendo la visita dal nodo radice, ma in modalità
  "salto";

* nell'implementazione di `visit` si dovrà tener conto della "natura" delle
  visite: nel caso "normale" si agirà come di consueto interpretando i vari
  statement, nel caso di "salto" si procederà esclusivamente alla visita dei
  sotto-alberi al solo scopo di raggiungere l'etichetta cercata;
  
* trovata l'etichetta, la natura delle visite tornerà "normale".

Questo approccio è senz'altro poco efficiente, ma assumendo che l'uso del `Goto`
sia sporadico, ne consente una implementazione abbastanza semplice.

## Organizzazione del codice, documentazione e testing

Al fine di formulare la sua valutazione, il docente deve non solo accertare il
corretto funzionamento dell'interprete/compilatore, ma essere in grado di
comprendere il codice che lo realizza, con particolare riferimento alle scelte
progettuali, le strutture dati e la sua organizzazione.

Sebbene non è richiesta una documentazione formale, si suggerisce di realizzare
il codice in modo modularizzato, provvedendo un minimo di commenti (nel codice
stesso) che ne chiariscano la struttura ed il comportamento. Sopratutto nelle
parti in cui è stata effettuata una scelta progettuale, o adottata una soluzione
non ovvia.

Il codice deve essere strutturato in modo tale che sia possibile eseguire
diversi programmi ciascuno su diversi input, raccogliendone in modo semplice
l'output. La valutazione sarà basata (tra l'altro) su una batteria di test che
sarà parzialmente messa a disposizione degli studenti prima della consegna della
versione finale del progetto.
