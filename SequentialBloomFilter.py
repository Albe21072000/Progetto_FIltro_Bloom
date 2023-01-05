import time
from BloomFilter import *


class SequentialBloomFilter(BloomFilter):
    # non ridefinisco il costruttore
    def inizializzaFiltro(self, array):  # metodo per inizializzare il filtro
        risHash = []  # lista delle posizioni "sicure" del filtro calcolate dalle funzioni hash
        for j in range(0, self.numFunzHash):
            risHash.extend(
                applicahash(array[i], self.size, j) for i in range(0, len(array)))  # Calcolo per ogni funzione
            # il risultato della sua applicazione a ogni indirizzo e appendo il risultato alla lista
        for i in range(0, len(risHash)):  # pongo a uno il valore delle posizioni calcolate in precedenza
            self.filter[risHash[i]] = 1

    def controllaIndirizzo(self, address) -> bool:  # metodo per verificare se un indirizzo è considerato sicuro
        risultati = []  # lista delle posizioni del filtro da controllare
        risultati.extend(applicahash(address, self.size, i) for i in range(0, self.numFunzHash))
        for i in range(0, self.numFunzHash):
            if self.filter[risultati[i]] == 0:
                return False
        return True


if __name__ == '__main__':
    bfs = SequentialBloomFilter(800, 10)  # Instanzio un nuovo filtro di Bloom sequenziale
    print("Probabilità di incontrare falsi positivi inizializzando il filtro con una lista di " +
          str(len(indirizziSicuri)) + " parole che non si ripetono: " +
          str(bfs.probFalsiPositivi(indirizziSicuri) * 100) + '%')
    tempo_inizio = time.time()
    bfs.inizializzaFiltro(indirizziSicuri)  # inizializzo il filtro con la lista d'indirizzi giudicati sicuri
    tempo_fine = time.time()
    print('Tempo di inizializzazione del filtro sequenziale: ' + str(tempo_fine - tempo_inizio) + ' secondi')
    tempo_inizio = time.time()
    print('Risultato dei controlli: ')
    # Testo il controllo con alcuni indirizzi sicuri e non
    print(bfs.controllaIndirizzo("spam.scam@fraud.com"))
    print(bfs.controllaIndirizzo("alberto.biliotti@stud.unifi.it"))  # indirizzo sicuro
    print(bfs.controllaIndirizzo("albe.biliotti@gmail.com"))
    print(bfs.controllaIndirizzo("sam.scam@fraud.com"))
    print(bfs.controllaIndirizzo("albrto.biliotti@stud.unifi.it"))
    print(bfs.controllaIndirizzo("ale.biliott@gmail.com"))
    print(bfs.controllaIndirizzo("thomasj@icloud.com"))  # indirizzo sicuro
    print(bfs.controllaIndirizzo("boh"))
    print(bfs.controllaIndirizzo("prova"))
    tempo_fine = time.time()
    print('Tempo di controllo degli indirizzi del filtro sequenziale: ' + str(tempo_fine - tempo_inizio) + ' secondi')
