# CoDiNE

Questa directory contiene il **testo** del progetto *CoDiNE* (AA 2025/26):
un interprete per un linguaggio imperativo con **Controllo Dimensionale e
Normalizzazione di Espressioni**.

Per comodità di lettura è disponibile la
[versione HTML del testo](https://let-unimi.github.io/progetti/07-CoDiNE/).

## Test di integrazione

La directory `tests/` contiene una batteria di test nella forma:

```
tests/<nome>/sorgente.codine   # programma CoDiNE
tests/<nome>/input-N.txt       # parametri di main (frazioni P/Q, uno per riga)
tests/<nome>/expected-N.txt    # output atteso (una frazione P/Q)
```
