import time
from BloomFilter import *


class SequentialBloomFilter(BloomFilter):
    # non ridefinisco il costruttore
    def inizializzaFiltro(self, indirizzisicuri):  # metodo per inizializzare il filtro
        risHash = []  # lista delle posizioni "sicure" del filtro calcolate dalle funzioni hash
        for j in range(0, self.numFunzHash):
            risHash.extend(
                applicahash(indirizzisicuri[i], self.size, j) for i in
                range(0, len(indirizzisicuri)))  # Calcolo per ogni funzione
            # il risultato della sua applicazione a ogni indirizzo e appendo il risultato alla lista
        for i in range(0, len(risHash)):  # pongo a uno il valore delle posizioni calcolate in precedenza
            self.filter[risHash[i]] = 1

    def controllaIndirizzi(self, indirizzi):
        ris = []
        ris.extend(self.controllaIndirizzo(indirizzi[i]) for i in range(0, len(indirizzi)))
        return ris


if __name__ == '__main__':  # non necessario, lo uso per tenere in ordine il codice
    bfs = SequentialBloomFilter(800, 7)  # Instanzio un nuovo filtro di Bloom sequenziale
    print("Probabilità di incontrare falsi positivi inizializzando il filtro con una lista di " +
          str(len(indirizziSicuri)) + " parole che non si ripetono: " +
          str(bfs.probFalsiPositivi(indirizziSicuri) * 100) + '%')
    tempo_inizio = time.time()
    bfs.inizializzaFiltro(indirizziSicuri)  # inizializzo il filtro con la lista d'indirizzi giudicati sicuri
    tempo_fine = time.time()
    print('Tempo di inizializzazione del filtro sequenziale: ' + str(tempo_fine - tempo_inizio) + ' secondi')
    print('Risultato dei controlli: ')
    # Testo il controllo con una lista d'indirizzi sicuri e non
    tempo_inizio = time.time()
    print(bfs.controllaIndirizzi(indirizziTest))
    tempo_fine = time.time()
    print('Tempo di controllo: ' + str(tempo_fine - tempo_inizio) + ' secondi')
