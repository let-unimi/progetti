# LeT@UniMI Progetti

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-blue.svg)](http://creativecommons.org/licenses/by-sa/4.0/)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/let-unimi/handouts/master?filepath=Handouts.ipynb)

Questo repository contiene i testi dei *progetti d'esame* (e le relative informazioni accessorie) dell'insegnamento di [Linguaggi e
traduttori](https://let.di.unimi.it/) dell'[Università degli Studi di
Milano](http://www.unimi.it/).

Di seguito trovate i progetti, elencati per anno accademico; le informazioni circa le [modalità d'esame](https://let.di.unimi.it/info.html#modalita-di-valutazione) sono disponibili sul [sito del corso](https://let.di.unimi.it/).

## Modalità di sviluppo e consegna

Il codice deve essere consegnato tramite un **apposito repository** su GitHub
*creato dal docente a seguito dell'incontro in cui viene concordato il progetto* .
Gli studenti sono incoraggiati ad effettuare frequenti **commit** periodici per
testimoniare il processo di sviluppo e sono altresì incoraggiati ad effettuare
(anche con una frequenza ridotta rispetto ai *commit*) dei **push** periodici al
fine di informare il docente dello stato di avanzamento del progetto (cosa che
rende possibili, anche se non garantite, delle eventuali *code review* del
codice da parte del docente).

Al termine del lavoro, *con congruo anticipo rispetto alla data del colloquio*,
lo studente effettua un commit con messaggio `CONSEGNA FINALE` che segna il
termine del processo di sviluppo e l'inizio della valutazione definitiva da
parte del docente.

Chi non conosce o non è in grado di usare `git` e/o GitHub può *documentarsi per
tempo* in rete, ad esempio seguendo la guida [Git
Handbook](https://guides.github.com/introduction/git-handbook/) ed usando un
client grafico come [GitHub Desktop](https://desktop.github.com/). In nessun
caso sono previste altre modalità di consegna.

### Documentazione e test

Non è richiesta la stesura di una *relazione*; per questa ragione è caldamente
suggerito che il codice contenga un **minimo di documentazione** atta a guidare
il docente nella comprensione della sua architettura, delle scelte progettuali
ed implementative e del comportamento delle sue varie parti. Si consiglia di
redigere tale documentazione sotto forma di **commenti nel codice**, usando
eventualmente (solo se si è in grado e senza perdere tempo) uno degli strumenti
di documentazione automatica disponibili per il linguaggio scelto.

Il codice deve consentire un minimo di **testing**, se non altro sotto forma di test unitari e di accettazione; qualora il testo del progetto indichi esplicitamente alcuni test, è comunque *necessario che lo studente sviluppi ulteriori test* secondo le tecniche e usando gli strumenti che gli sono più familiari.

## Progetti per l'anno accademico 2019/20

#### Tipo A

* Un interprete per il linguaggio "Tiny HI" (maggiori dettagli verranno resi noti circa un mese prima del termine del semestre).

#### Tipo B

Un elenco di possibili argomenti per esami di questo tipo è:

* Implementare l'algoritmo di Earley (rif. [Marpa](https://docs.google.com/file/d/0B9_mR_M2zOc4Ni1zSW5IYzk3TGc/edit) e PT),
* Implementare gli algoritmi LR(1), SLR(1) e LALR(1) (rif. PT),
* Implementare gli algoritmi descritti in: "[Parsing Expressions by Recursive Descent](http://www.engr.mun.ca/~theo/Misc/exp_parsing.htm)",
* Implementare gli algoritmi descritti in: "[Regular Expression Matching Can Be Simple And Fast (but is slow in Java, Perl, PHP, Python, Ruby, ...)](https://swtch.com/~rsc/regexp/regexp1.html)"